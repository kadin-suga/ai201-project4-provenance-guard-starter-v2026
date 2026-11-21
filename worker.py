#!/usr/bin/env python3
"""Polling worker for queued Provenance Guard analysis jobs."""

import argparse
import logging
import os
import signal
import socket
import time
from uuid import uuid4

import config
import audit
import database
import detector
import scoring
import stylometry


LOGGER = logging.getLogger("provenance-worker")
_stop_requested = False


def _request_stop(signum, _frame) -> None:
    """Finish the current operation, then stop before claiming another job."""
    global _stop_requested
    _stop_requested = True
    LOGGER.info("received signal %s; stopping after the current operation", signum)


def default_worker_id() -> str:
    """Build an identifier unique across hosts and processes."""
    return f"{socket.gethostname()}-{os.getpid()}-{uuid4().hex[:8]}"


def process_job(job: dict, *, worker_id: str) -> bool:
    """Analyze one claimed job and store either its result or its failure."""
    job_id = job["job_id"]
    started = time.perf_counter()
    LOGGER.info("processing job=%s attempt=%s", job_id, job["attempts"])
    try:
        model_score = detector.model_signal(job["input_text"])
        style_score = stylometry.style_signal(job["input_text"])
        confidence = scoring.combine_signals(model_score, style_score)
        guess, label = scoring.score_to_label(confidence)
        completed = database.complete_job(
            job_id=job_id,
            worker_id=worker_id,
            model_score=model_score,
            style_score=style_score,
            confidence=confidence,
            guess=guess,
            label=label,
        )
    except database.JobStateConflict as exc:
        LOGGER.warning("discarded stale result for job=%s: %s", job_id, exc)
        return False
    except Exception as exc:  # noqa: BLE001 - every job failure must be persisted
        LOGGER.exception("analysis failed for job=%s", job_id)
        try:
            failed = database.fail_job(
                job_id=job_id,
                worker_id=worker_id,
                error=f"{type(exc).__name__}: {exc}",
            )
            audit.log_run(
                job_id=job_id,
                creator_id=job["creator_id"],
                attempt=job["attempts"],
                input_text=job["input_text"],
                output={
                    "status": failed["status"],
                    "error": f"{type(exc).__name__}: {exc}",
                },
                duration_ms=(time.perf_counter() - started) * 1000,
                worker_id=worker_id,
            )
            LOGGER.info(
                "job=%s moved to status=%s after attempt=%s",
                job_id,
                failed["status"],
                failed["attempts"],
            )
        except database.JobStateConflict:
            LOGGER.warning("job=%s was already recovered by another worker", job_id)
        return False

    audit.log_run(
        job_id=job_id,
        creator_id=job["creator_id"],
        attempt=job["attempts"],
        input_text=job["input_text"],
        output={
            "status": completed["status"],
            "model_score": model_score,
            "style_score": style_score,
            "confidence": confidence,
            "guess": guess,
            "label": label,
        },
        duration_ms=(time.perf_counter() - started) * 1000,
        worker_id=worker_id,
    )

    LOGGER.info(
        "completed job=%s guess=%s confidence=%.4f",
        job_id,
        guess,
        confidence,
    )
    return True


def run(*, worker_id: str, once: bool = False) -> int:
    """Warm the model once, then claim and process jobs until stopped."""
    LOGGER.info("starting worker=%s", worker_id)
    try:
        LOGGER.info(detector.warm_up())
    except detector.DetectorUnavailable:
        LOGGER.exception("detector model could not be loaded")
        return 1

    next_recovery = 0.0
    while not _stop_requested:
        try:
            now = time.monotonic()
            if now >= next_recovery:
                recovered = database.recover_expired_jobs()
                if recovered:
                    LOGGER.warning("recovered %s expired job lease(s)", len(recovered))
                next_recovery = now + config.JOB_RECOVERY_INTERVAL_SECONDS

            job = database.claim_job(worker_id=worker_id)
            if job is not None:
                process_job(job, worker_id=worker_id)
            elif once:
                LOGGER.info("no queued jobs are currently available")
                return 0
            else:
                time.sleep(config.JOB_POLL_SECONDS)
        except database.DatabaseUnavailable as exc:
            LOGGER.error("database unavailable: %s", exc)
            if once:
                return 1
            time.sleep(config.JOB_DATABASE_RETRY_SECONDS)

        if once:
            return 0

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--worker-id",
        default=default_worker_id(),
        help="identifier recorded on claims and events",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="process at most one available job, then exit",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    signal.signal(signal.SIGINT, _request_stop)
    signal.signal(signal.SIGTERM, _request_stop)
    try:
        return run(worker_id=args.worker_id, once=args.once)
    finally:
        database.close_pool()


if __name__ == "__main__":
    raise SystemExit(main())
