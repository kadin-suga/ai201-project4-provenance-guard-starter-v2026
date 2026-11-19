"""Live PostgreSQL integration tests for the asynchronous worker lifecycle."""

import threading
import unittest
from unittest.mock import patch
from uuid import uuid4

import config
import database
from app import app


@unittest.skipUnless(config.DATABASE_URL, "DATABASE_URL is not configured")
class WorkerDatabaseTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        database.close_pool()

    def setUp(self):
        self.job_ids: list[str] = []

    def tearDown(self):
        if self.job_ids:
            with database._connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM analysis_jobs WHERE job_id = ANY(%s::uuid[])",
                        (self.job_ids,),
                    )

    def create_job(self, suffix: str) -> dict:
        job = database.create_job(
            creator_id=f"integration-test-{suffix}",
            text=(
                "This integration test creates enough ordinary text for the "
                "job queue, while database lifecycle tests use fixed scores."
            ),
        )
        self.job_ids.append(job["job_id"])
        return job

    @staticmethod
    def complete(job: dict, worker_id: str) -> dict:
        return database.complete_job(
            job_id=job["job_id"],
            worker_id=worker_id,
            model_score=0.2,
            style_score=0.4,
            confidence=0.3,
            guess="human",
            label="Integration test result.",
        )

    def test_claim_and_complete_lifecycle(self):
        created = self.create_job("lifecycle")
        claimed = database.claim_job(worker_id="lifecycle-worker")

        self.assertEqual(claimed["job_id"], created["job_id"])
        self.assertEqual(claimed["status"], "running")
        self.assertEqual(claimed["attempts"], 1)

        completed = self.complete(claimed, "lifecycle-worker")
        self.assertEqual(completed["status"], "completed")
        self.assertEqual(database.get_job(created["job_id"])["confidence"], 0.3)

    def test_simultaneous_workers_claim_different_jobs(self):
        expected = {
            self.create_job("concurrency-a")["job_id"],
            self.create_job("concurrency-b")["job_id"],
        }
        barrier = threading.Barrier(2)
        claimed: list[tuple[str, dict]] = []
        errors: list[BaseException] = []
        result_lock = threading.Lock()

        def claim(worker_id: str) -> None:
            try:
                barrier.wait()
                job = database.claim_job(worker_id=worker_id)
                with result_lock:
                    claimed.append((worker_id, job))
            except BaseException as exc:  # test threads must report failures
                with result_lock:
                    errors.append(exc)

        threads = [
            threading.Thread(target=claim, args=(f"concurrent-worker-{index}",))
            for index in range(2)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        self.assertFalse(errors)
        self.assertEqual(len(claimed), 2)
        self.assertEqual({job["job_id"] for _, job in claimed}, expected)
        for worker_id, job in claimed:
            self.complete(job, worker_id)

    def test_failure_retries_then_becomes_final(self):
        created = self.create_job("failure")
        old_base = config.JOB_RETRY_BASE_SECONDS
        config.JOB_RETRY_BASE_SECONDS = 0
        try:
            for attempt in range(1, 4):
                worker_id = f"failure-worker-{attempt}"
                claimed = database.claim_job(worker_id=worker_id)
                self.assertEqual(claimed["job_id"], created["job_id"])
                result = database.fail_job(
                    job_id=claimed["job_id"],
                    worker_id=worker_id,
                    error=f"test failure {attempt}",
                )
                expected_status = "queued" if attempt < 3 else "failed"
                self.assertEqual(result["status"], expected_status)
        finally:
            config.JOB_RETRY_BASE_SECONDS = old_base

    def test_expired_lease_is_recovered(self):
        created = self.create_job("recovery")
        claimed = database.claim_job(worker_id="crashed-worker")
        self.assertEqual(claimed["job_id"], created["job_id"])

        with database._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE analysis_jobs
                    SET lease_expires_at = NOW() - INTERVAL '1 second'
                    WHERE job_id = %s
                    """,
                    (created["job_id"],),
                )

        recovered = database.recover_expired_jobs()
        recovered_job = next(
            job for job in recovered if job["job_id"] == created["job_id"]
        )
        self.assertEqual(recovered_job["status"], "queued")

        replacement = database.claim_job(worker_id="replacement-worker")
        self.assertEqual(replacement["job_id"], created["job_id"])
        self.complete(replacement, "replacement-worker")

    def test_expired_final_lease_becomes_failed(self):
        created = self.create_job("final-lease")
        claimed = database.claim_job(worker_id="final-crashed-worker")
        self.assertEqual(claimed["job_id"], created["job_id"])

        with database._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE analysis_jobs
                    SET
                        attempts = max_attempts,
                        lease_expires_at = NOW() - INTERVAL '1 second'
                    WHERE job_id = %s
                    """,
                    (created["job_id"],),
                )

        recovered = database.recover_expired_jobs()
        recovered_job = next(
            job for job in recovered if job["job_id"] == created["job_id"]
        )
        self.assertEqual(recovered_job["status"], "failed")

    def test_rate_limits_are_stored_in_redis(self):
        creator_id = f"rate-limit-test-{uuid4()}"
        payload = {
            "creator_id": creator_id,
            "text": "A valid queued analysis request used to test shared limits.",
        }
        with patch("app.audit.log_rejection"), app.test_client() as client:
            responses = [client.post("/jobs", json=payload) for _ in range(6)]

        for response in responses[:5]:
            if response.status_code == 202:
                self.job_ids.append(response.get_json()["job_id"])
        self.assertEqual(
            [response.status_code for response in responses],
            [202, 202, 202, 202, 202, 429],
        )


if __name__ == "__main__":
    unittest.main()
