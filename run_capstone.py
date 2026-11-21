#!/usr/bin/env python3
"""Run the five capstone criteria against the local queue, three times each."""

import argparse
import json
import statistics
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import audit
import config
import database
import detector
import worker
from app import app


SAMPLE_TEXT = (
    "A small river crossed the park behind the library. On clear mornings, "
    "neighbors stopped on the footbridge to watch ducks move through the reeds. "
    "The scene changed with the weather, but the path remained busy all year."
)
RUN_LOG = config.LOG_DIR / "run_records.jsonl"
REQUIRED_RESULT_FIELDS = {
    "model_score", "style_score", "confidence", "guess", "label"
}


def _read_run_records() -> list[dict]:
    if not RUN_LOG.exists():
        return []
    records = []
    for line in RUN_LOG.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def _cleanup(job_ids: list[str]) -> None:
    if not job_ids:
        return
    with database._connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM analysis_jobs WHERE job_id = ANY(%s::uuid[])",
                (job_ids,),
            )


def _criterion_1(trial: int, job_ids: list[str]) -> dict:
    accepted = 0
    durations = []
    evidence = []
    with app.test_client() as client:
        for item in range(5):
            creator = f"capstone-c1-{trial}-{item}-{uuid4()}"
            started = time.perf_counter()
            response = client.post(
                "/jobs", json={"creator_id": creator, "text": SAMPLE_TEXT}
            )
            duration_ms = (time.perf_counter() - started) * 1000
            body = response.get_json() or {}
            if body.get("job_id"):
                job_ids.append(body["job_id"])
            status_response = (
                client.get(body["status_url"])
                if body.get("status_url")
                else None
            )
            valid = (
                response.status_code == 202
                and duration_ms < 500
                and bool(body.get("job_id"))
                and body.get("status") == "queued"
                and status_response is not None
                and status_response.status_code == 200
                and status_response.get_json().get("job_id") == body.get("job_id")
            )
            accepted += int(valid)
            durations.append(round(duration_ms, 2))
            evidence.append({
                "http": response.status_code,
                "job_id": body.get("job_id"),
                "duration_ms": round(duration_ms, 2),
                "status_get": status_response.status_code if status_response else None,
            })
    return {
        "summary": f"{accepted}/5; max {max(durations):.2f} ms",
        "met": accepted == 5,
        "evidence": evidence,
    }


def _criterion_2(trial: int, job_ids: list[str]) -> dict:
    created = database.create_job(
        creator_id=f"capstone-c2-{trial}-{uuid4()}", text=SAMPLE_TEXT
    )
    job_ids.append(created["job_id"])
    started = time.perf_counter()
    claimed = database.claim_job(worker_id=f"capstone-c2-worker-{trial}")
    processed = worker.process_job(claimed, worker_id=f"capstone-c2-worker-{trial}")
    elapsed = time.perf_counter() - started
    result = database.get_job(created["job_id"])
    numeric_scores_valid = all(
        isinstance(result.get(field), (int, float))
        and 0.0 <= result[field] <= 1.0
        for field in ("model_score", "style_score", "confidence")
    )
    met = (
        processed
        and result.get("status") == "completed"
        and elapsed < 60
        and REQUIRED_RESULT_FIELDS <= result.keys()
        and numeric_scores_valid
    )
    return {
        "summary": f"{result.get('status')} in {elapsed:.3f} s",
        "met": bool(met),
        "evidence": {
            "job_id": created["job_id"],
            "duration_seconds": round(elapsed, 3),
            "status": result.get("status"),
            "confidence": result.get("confidence"),
            "guess": result.get("guess"),
        },
    }


def _criterion_3(trial: int, job_ids: list[str]) -> dict:
    created = [
        database.create_job(
            creator_id=f"capstone-c3-{trial}-{index}-{uuid4()}", text=SAMPLE_TEXT
        )
        for index in range(2)
    ]
    job_ids.extend(job["job_id"] for job in created)
    barrier = threading.Barrier(2)
    claims = []
    errors = []
    claim_lock = threading.Lock()

    def claim(worker_id: str) -> None:
        try:
            barrier.wait()
            claimed = database.claim_job(worker_id=worker_id)
            with claim_lock:
                claims.append((worker_id, claimed))
        except BaseException as exc:  # thread failures must become evidence
            with claim_lock:
                errors.append(f"{type(exc).__name__}: {exc}")

    threads = [
        threading.Thread(target=claim, args=(f"capstone-c3-worker-{trial}-{i}",))
        for i in range(2)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    claimed_ids = [job["job_id"] for _, job in claims if job]
    expected_ids = {job["job_id"] for job in created}
    met = not errors and len(claimed_ids) == 2 and set(claimed_ids) == expected_ids
    for worker_id, job in claims:
        if job:
            database.complete_job(
                job_id=job["job_id"], worker_id=worker_id,
                model_score=0.2, style_score=0.4, confidence=0.3,
                guess="human", label="Capstone concurrency test result.",
            )
    return {
        "summary": f"{len(set(claimed_ids))}/2 unique claims",
        "met": met,
        "evidence": {"expected": sorted(expected_ids), "claimed": claimed_ids, "errors": errors},
    }


def _criterion_4(trial: int, job_ids: list[str]) -> dict:
    created = database.create_job(
        creator_id=f"capstone-c4-{trial}-{uuid4()}", text=SAMPLE_TEXT
    )
    job_ids.append(created["job_id"])
    old_retry_base = config.JOB_RETRY_BASE_SECONDS
    config.JOB_RETRY_BASE_SECONDS = 0
    try:
        with patch("worker.detector.model_signal", side_effect=RuntimeError("forced failure")):
            for attempt in range(3):
                worker_id = f"capstone-c4-worker-{trial}-{attempt}"
                claimed = database.claim_job(worker_id=worker_id)
                worker.process_job(claimed, worker_id=worker_id)
    finally:
        config.JOB_RETRY_BASE_SECONDS = old_retry_base

    result = database.get_job(created["job_id"])
    records = [
        row for row in _read_run_records()
        if row.get("job_id") == created["job_id"]
    ]
    required = {"timestamp", "input", "output", "duration_ms"}
    fields_valid = len(records) == 3 and all(required <= row.keys() for row in records)
    with app.test_client() as client:
        public = client.get(f"/jobs/{created['job_id']}").get_json()
    raw_error_hidden = "error" not in public and "forced failure" not in json.dumps(public)
    met = (
        result.get("status") == "failed"
        and result.get("attempts") == 3
        and raw_error_hidden
        and fields_valid
    )
    return {
        "summary": f"failed after {result.get('attempts')} attempts; {len(records)}/3 run logs",
        "met": met,
        "evidence": {
            "job_id": created["job_id"],
            "stored_status": result.get("status"),
            "attempts": result.get("attempts"),
            "public_response": public,
            "run_records": records,
        },
    }


def _criterion_5(trial: int) -> dict:
    creator = f"capstone-c5-{trial}-{uuid4()}"
    with app.test_client() as client:
        response = client.post(
            "/submit", json={"creator_id": creator, "text": SAMPLE_TEXT}
        )
    body = response.get_json() or {}
    entries = audit.entries_for(body.get("content_id", ""))
    required = {
        "content_id", "model_score", "style_score", "confidence", "guess", "label"
    }
    met = response.status_code == 200 and required <= body.keys() and len(entries) == 1
    return {
        "summary": f"HTTP {response.status_code}; {len(entries)} audit decision",
        "met": met,
        "evidence": {"response": body, "audit_entries": entries},
    }


def _measure_cost(runs: int, job_ids: list[str]) -> dict:
    durations = []
    for index in range(runs):
        created = database.create_job(
            creator_id=f"capstone-cost-{index}-{uuid4()}", text=SAMPLE_TEXT
        )
        job_ids.append(created["job_id"])
        worker_id = f"capstone-cost-worker-{index}"
        claimed = database.claim_job(worker_id=worker_id)
        started = time.perf_counter()
        worker.process_job(claimed, worker_id=worker_id)
        durations.append(time.perf_counter() - started)
    return {
        "unit": "seconds of local compute per completed analysis",
        "runs": runs,
        "durations_seconds": [round(value, 4) for value in durations],
        "mean_seconds": round(statistics.mean(durations), 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True, choices=("before", "after"))
    parser.add_argument("--cost-runs", type=int, default=0)
    args = parser.parse_args()
    if not config.DATABASE_URL:
        parser.error("DATABASE_URL is not configured; load .env first")

    detector.warm_up()
    results = {
        "label": args.label,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "criteria": {str(index): [] for index in range(1, 6)},
    }
    job_ids = []
    try:
        for trial in range(1, 4):
            results["criteria"]["1"].append(_criterion_1(trial, job_ids))
            _cleanup(job_ids)
            job_ids.clear()
            results["criteria"]["2"].append(_criterion_2(trial, job_ids))
            _cleanup(job_ids)
            job_ids.clear()
            results["criteria"]["3"].append(_criterion_3(trial, job_ids))
            _cleanup(job_ids)
            job_ids.clear()
            results["criteria"]["4"].append(_criterion_4(trial, job_ids))
            _cleanup(job_ids)
            job_ids.clear()
            results["criteria"]["5"].append(_criterion_5(trial))
        if args.cost_runs:
            results["cost"] = _measure_cost(args.cost_runs, job_ids)
    finally:
        _cleanup(job_ids)
        database.close_pool()

    destination = config.RESULTS_DIR / f"capstone_{args.label}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "result_file": str(destination),
        "verdicts": {
            number: "MET" if all(trial["met"] for trial in trials) else "MISSED"
            for number, trials in results["criteria"].items()
        },
        "runs": {
            number: [trial["summary"] for trial in trials]
            for number, trials in results["criteria"].items()
        },
        "cost": results.get("cost"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
