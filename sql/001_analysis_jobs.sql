BEGIN;

CREATE TABLE IF NOT EXISTS analysis_jobs (
    job_id UUID PRIMARY KEY,
    creator_id TEXT NOT NULL CHECK (BTRIM(creator_id) <> ''),
    input_text TEXT NOT NULL CHECK (BTRIM(input_text) <> ''),

    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'completed', 'failed')),
    attempts INTEGER NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    max_attempts INTEGER NOT NULL DEFAULT 3 CHECK (max_attempts > 0),
    available_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    worker_id TEXT,
    lease_expires_at TIMESTAMPTZ,

    model_score DOUBLE PRECISION
        CHECK (model_score IS NULL OR model_score BETWEEN 0.0 AND 1.0),
    style_score DOUBLE PRECISION
        CHECK (style_score IS NULL OR style_score BETWEEN 0.0 AND 1.0),
    confidence DOUBLE PRECISION
        CHECK (confidence IS NULL OR confidence BETWEEN 0.0 AND 1.0),
    guess TEXT CHECK (guess IS NULL OR guess IN ('human', 'ai', 'unsure')),
    label TEXT,
    error TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS analysis_jobs_queue_idx
    ON analysis_jobs (available_at, created_at)
    WHERE status = 'queued';

CREATE INDEX IF NOT EXISTS analysis_jobs_creator_idx
    ON analysis_jobs (creator_id, created_at DESC);

CREATE INDEX IF NOT EXISTS analysis_jobs_lease_idx
    ON analysis_jobs (lease_expires_at)
    WHERE status = 'running';

CREATE TABLE IF NOT EXISTS job_events (
    event_id BIGSERIAL PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES analysis_jobs(job_id) ON DELETE CASCADE,
    event_type TEXT NOT NULL
        CHECK (event_type IN ('queued', 'started', 'completed', 'failed', 'retried')),
    worker_id TEXT,
    details JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS job_events_job_idx
    ON job_events (job_id, created_at);

COMMIT;
