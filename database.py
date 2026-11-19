"""PostgreSQL access for asynchronous analysis jobs."""

from datetime import date, datetime
from uuid import UUID, uuid4

import psycopg
from psycopg.rows import dict_row

import config


class DatabaseUnavailable(RuntimeError):
    """The job database is missing or cannot be reached."""


def _connect():
    if not config.DATABASE_URL:
        raise DatabaseUnavailable(
            "DATABASE_URL is not configured. Load .env before starting the service."
        )

    try:
        return psycopg.connect(
            config.DATABASE_URL,
            connect_timeout=5,
            row_factory=dict_row,
        )
    except psycopg.Error as exc:
        raise DatabaseUnavailable("The job database is unavailable.") from exc


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
                        job_id,
                        creator_id,
                        status,
                        attempts,
                        model_score,
                        style_score,
                        confidence,
                        guess,
                        label,
                        error,
                        created_at,
                        started_at,
                        completed_at
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

def claim_job(*, work_id: str) -> dict | None:
    """Atomincally claim the oldest available queued job"""
    try:
        with _connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    WITH next_job AS (
                        SELECT job_id
                        FROM analysis_jobs
                        WHERE status ='queued'
                            AND available_at <= NOW()
                        ORDER BY available_at, created_at
                        FOR UPDATE SKIP LOCKED 
                        LIMIT 1
                        )
                    )
                    UPDATE analysis_jobs AS job 
                    SET 
                        status = 'running',
                        attempts = job.attempts +1,
                        worker_id = %s,
                        started_at = NOW(),
                        lease_expires_at = 
                            NOW() + (%s +INTERVAL '1 second'),
                        error = NULL
                    FROM next_job
                    WHERE job.job_id = next_job.job_id
                    RETURNING
                        job.job_id,
                        job.creator_id,
                        job.input_text,
                        job.status,
                        job.attempts,
                        job.max_attempts,
                        job.started_at,
                        job.lease_expires_at
                    """,
                    (worker_id, config.JOB_LEASE_SECONDS),
                )
                job = cursor.fetchone()
                if job is not None:
                    cursor.execute(
                        """
                        INSERT INTO job_events(
                            job_id,
                            event_type,
                            worker_id,
                            details
                        )
                        VALUES (
                            %s,
                            'started',
                            %s,
                            jsonb_build_object('attempt', %s)
                        )
                        """,
                        (
                            job["job_id"],
                            work_id,
                            job["attempts"],
                        ),
                    )
    except DatabaseUnavailable:
        raise
    except psycopg.Error as exc:
        raise DatabaseUnavailable(
            "A queued job could not be claimed."
        ) from exc
    return _json_ready(job)