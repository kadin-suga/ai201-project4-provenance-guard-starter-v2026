"""PostgreSQL access for asynchronous analysis jobs."""

import atexit
from contextlib import contextmanager
from datetime import date, datetime
from threading import Lock
from uuid import UUID, uuid4

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool, PoolTimeout

import config


class DatabaseUnavailable(RuntimeError):
    """The job database is missing or cannot be reached."""


class JobStateConflict(RuntimeError):
    """A worker tried to change a job it no longer owns."""


_pool: ConnectionPool | None = None
_pool_lock = Lock()


def _get_pool() -> ConnectionPool:
    """Create one process-local connection pool on first database use."""
    global _pool

    if not config.DATABASE_URL:
        raise DatabaseUnavailable(
            "DATABASE_URL is not configured. Load .env before starting the service."
        )

    if _pool is None:
        with _pool_lock:
            if _pool is None:
                try:
                    pool = ConnectionPool(
                        conninfo=config.DATABASE_URL,
                        min_size=config.DATABASE_POOL_MIN,
                        max_size=config.DATABASE_POOL_MAX,
                        timeout=5,
                        kwargs={"connect_timeout": 5, "row_factory": dict_row},
                        open=False,
                    )
                    pool.open(wait=True, timeout=5)
                    _pool = pool
                except (psycopg.Error, PoolTimeout) as exc:
                    raise DatabaseUnavailable(
                        "The job database is unavailable."
                    ) from exc

    return _pool


@contextmanager
def _connect():
    """Borrow a connection and return it to the process pool afterwards."""
    try:
        with _get_pool().connection(timeout=5) as connection:
            yield connection
    except DatabaseUnavailable:
        raise
    except (psycopg.Error, PoolTimeout) as exc:
        raise DatabaseUnavailable("The job database is unavailable.") from exc


def close_pool() -> None:
    """Close pooled connections, primarily for graceful process shutdown."""
    global _pool
    with _pool_lock:
        if _pool is not None:
            _pool.close()
            _pool = None


atexit.register(close_pool)


def _json_ready(row: dict | None) -> dict | None:
    """Convert database-native values into predictable JSON values."""
    if row is None:
        return None

    result = dict(row)
    for key, value in result.items():
        if isinstance(value, UUID):
            result[key] = str(value)
        elif isinstance(value, (datetime, date)):
            result[key] = value.isoformat()
    return result


def create_job(*, creator_id: str, text: str) -> dict:
    """Insert a queued job and its first audit event in one transaction."""
    job_id = uuid4()
    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO analysis_jobs (job_id, creator_id, input_text)
                    VALUES (%s, %s, %s)
                    RETURNING job_id, creator_id, status, created_at
                    """,
                    (job_id, creator_id, text),
                )
                job = cursor.fetchone()
                cursor.execute(
                    """
                    INSERT INTO job_events (job_id, event_type)
                    VALUES (%s, 'queued')
                    """,
                    (job_id,),
                )
    except DatabaseUnavailable:
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable("The job could not be stored.") from exc
    return _json_ready(job)


def get_job(job_id: str | UUID) -> dict | None:
    """Return public status and result fields for one job."""
    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        job_id, creator_id, status, attempts,
                        model_score, style_score, confidence, guess, label, error,
                        created_at, started_at, completed_at
                    FROM analysis_jobs
                    WHERE job_id = %s
                    """,
                    (job_id,),
                )
                job = cursor.fetchone()
    except DatabaseUnavailable:
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable("The job could not be read.") from exc
    return _json_ready(job)


def claim_job(*, worker_id: str) -> dict | None:
    """Atomically claim the oldest available queued job."""
    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    WITH next_job AS (
                        SELECT job_id
                        FROM analysis_jobs
                        WHERE status = 'queued' AND available_at <= NOW()
                        ORDER BY available_at, created_at
                        FOR UPDATE SKIP LOCKED
                        LIMIT 1
                    )
                    UPDATE analysis_jobs AS job
                    SET
                        status = 'running',
                        attempts = job.attempts + 1,
                        worker_id = %s,
                        started_at = NOW(),
                        lease_expires_at = NOW() + (%s * INTERVAL '1 second'),
                        error = NULL
                    FROM next_job
                    WHERE job.job_id = next_job.job_id
                    RETURNING
                        job.job_id, job.creator_id, job.input_text, job.status,
                        job.attempts, job.max_attempts, job.started_at,
                        job.lease_expires_at
                    """,
                    (worker_id, config.JOB_LEASE_SECONDS),
                )
                job = cursor.fetchone()
                if job is not None:
                    cursor.execute(
                        """
                        INSERT INTO job_events (
                            job_id, event_type, worker_id, details
                        )
                        VALUES (
                            %s, 'started', %s,
                            jsonb_build_object('attempt', %s)
                        )
                        """,
                        (job["job_id"], worker_id, job["attempts"]),
                    )
    except DatabaseUnavailable:
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable("A queued job could not be claimed.") from exc
    return _json_ready(job)


def complete_job(
    *,
    job_id: str | UUID,
    worker_id: str,
    model_score: float,
    style_score: float,
    confidence: float,
    guess: str,
    label: str,
) -> dict:
    """Save a result, but only while the caller still owns the running job."""
    scores = (model_score, style_score, confidence)
    if any(not 0.0 <= score <= 1.0 for score in scores):
        raise ValueError("All job scores must be between 0.0 and 1.0.")
    if guess not in {"human", "ai", "unsure"}:
        raise ValueError("guess must be 'human', 'ai', or 'unsure'.")

    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE analysis_jobs
                    SET
                        status = 'completed', model_score = %s, style_score = %s,
                        confidence = %s, guess = %s, label = %s, error = NULL,
                        completed_at = NOW(), lease_expires_at = NULL
                    WHERE job_id = %s
                        AND status = 'running'
                        AND worker_id = %s
                        AND lease_expires_at > NOW()
                    RETURNING
                        job_id, creator_id, status, attempts, model_score,
                        style_score, confidence, guess, label, started_at, completed_at
                    """,
                    (
                        model_score, style_score, confidence, guess, label,
                        job_id, worker_id,
                    ),
                )
                job = cursor.fetchone()
                if job is None:
                    raise JobStateConflict(
                        "The job is no longer running with a valid lease for this worker."
                    )
                cursor.execute(
                    """
                    INSERT INTO job_events (
                        job_id, event_type, worker_id, details
                    )
                    VALUES (%s, 'completed', %s, %s)
                    """,
                    (
                        job["job_id"],
                        worker_id,
                        Jsonb({
                            "attempt": job["attempts"],
                            "confidence": confidence,
                            "guess": guess,
                        }),
                    ),
                )
    except (DatabaseUnavailable, JobStateConflict):
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable("The completed job could not be stored.") from exc
    return _json_ready(job)


def fail_job(*, job_id: str | UUID, worker_id: str, error: str) -> dict:
    """Record an error, requeue if attempts remain, otherwise fail permanently."""
    error = str(error).strip() or "Unknown worker error"
    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT job_id, attempts, max_attempts
                    FROM analysis_jobs
                    WHERE job_id = %s
                        AND status = 'running'
                        AND worker_id = %s
                        AND lease_expires_at > NOW()
                    FOR UPDATE
                    """,
                    (job_id, worker_id),
                )
                current = cursor.fetchone()
                if current is None:
                    raise JobStateConflict(
                        "The job is no longer running for this worker."
                    )

                will_retry = current["attempts"] < current["max_attempts"]
                if will_retry:
                    delay = min(
                        config.JOB_RETRY_BASE_SECONDS
                        * (2 ** (current["attempts"] - 1)),
                        config.JOB_RETRY_MAX_SECONDS,
                    )
                    cursor.execute(
                        """
                        UPDATE analysis_jobs
                        SET
                            status = 'queued',
                            available_at = NOW() + (%s * INTERVAL '1 second'),
                            worker_id = NULL, lease_expires_at = NULL,
                            started_at = NULL, error = %s
                        WHERE job_id = %s
                        RETURNING
                            job_id, status, attempts, max_attempts, available_at, error
                        """,
                        (delay, error, job_id),
                    )
                    event_type = "retried"
                    details = {
                        "attempt": current["attempts"],
                        "error": error,
                        "retry_delay_seconds": delay,
                    }
                else:
                    cursor.execute(
                        """
                        UPDATE analysis_jobs
                        SET
                            status = 'failed', lease_expires_at = NULL,
                            error = %s, completed_at = NOW()
                        WHERE job_id = %s
                        RETURNING
                            job_id, status, attempts, max_attempts, completed_at, error
                        """,
                        (error, job_id),
                    )
                    event_type = "failed"
                    details = {"attempt": current["attempts"], "error": error}

                job = cursor.fetchone()
                cursor.execute(
                    """
                    INSERT INTO job_events (job_id, event_type, worker_id, details)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (job_id, event_type, worker_id, Jsonb(details)),
                )
    except (DatabaseUnavailable, JobStateConflict):
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable("The job failure could not be stored.") from exc
    return _json_ready(job)


def recover_expired_jobs(*, limit: int | None = None) -> list[dict]:
    """Requeue expired leases, or fail them when no attempts remain."""
    batch_size = limit or config.JOB_RECOVERY_BATCH_SIZE
    recovered: list[dict] = []
    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT job_id, worker_id, attempts, max_attempts
                    FROM analysis_jobs
                    WHERE status = 'running' AND lease_expires_at <= NOW()
                    ORDER BY lease_expires_at
                    FOR UPDATE SKIP LOCKED
                    LIMIT %s
                    """,
                    (batch_size,),
                )
                for expired in cursor.fetchall():
                    will_retry = expired["attempts"] < expired["max_attempts"]
                    if will_retry:
                        cursor.execute(
                            """
                            UPDATE analysis_jobs
                            SET
                                status = 'queued', available_at = NOW(),
                                worker_id = NULL, lease_expires_at = NULL,
                                started_at = NULL, error = 'Worker lease expired.'
                            WHERE job_id = %s
                            RETURNING job_id, status, attempts, available_at, error
                            """,
                            (expired["job_id"],),
                        )
                        event_type = "retried"
                    else:
                        cursor.execute(
                            """
                            UPDATE analysis_jobs
                            SET
                                status = 'failed', lease_expires_at = NULL,
                                error = 'Worker lease expired after final attempt.',
                                completed_at = NOW()
                            WHERE job_id = %s
                            RETURNING job_id, status, attempts, completed_at, error
                            """,
                            (expired["job_id"],),
                        )
                        event_type = "failed"

                    job = cursor.fetchone()
                    recovered.append(_json_ready(job))
                    cursor.execute(
                        """
                        INSERT INTO job_events (
                            job_id, event_type, worker_id, details
                        )
                        VALUES (
                            %s, %s, %s,
                            jsonb_build_object(
                                'attempt', %s, 'reason', 'lease_expired'
                            )
                        )
                        """,
                        (
                            expired["job_id"], event_type,
                            expired["worker_id"], expired["attempts"],
                        ),
                    )
    except DatabaseUnavailable:
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable("Expired jobs could not be recovered.") from exc
    return recovered
