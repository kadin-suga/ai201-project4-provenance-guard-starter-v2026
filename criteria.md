# Capstone acceptance criteria — Provenance Guard job queue

These five criteria define the capstone target before the capstone trial runner
or its result files exist. Criteria 1–4 cover the new asynchronous queue and
worker extension. Criterion 5 checks that the original synchronous system still
works. Every criterion is evaluated in three independent trials.

## 1. Valid work is accepted without waiting for analysis

In each trial, all 5 valid `POST /jobs` requests must return HTTP 202 within
500 ms, with a nonblank `job_id`, `status: "queued"`, and a `status_url` that
retrieves that same job.

**Why this target:** The extension exists to move GPT-2 analysis out of the
request path. Five requests expose persistence or response-shape failures, and
500 ms is comfortably below the seconds-long model work while allowing local
database overhead.

## 2. A queued job reaches a usable result

In each trial, 1 valid queued job must reach `completed` within 60 seconds and
return `model_score`, `style_score`, `confidence`, `guess`, and `label`; all
three numeric scores must be between 0.0 and 1.0.

**Why this target:** A quick 202 is meaningless unless the worker finishes the
real analysis. Sixty seconds allows the local GPT-2 model to run on CPU but is
short enough that a caller can reasonably poll for a result.

## 3. Concurrent workers never process the same job

In each trial, 2 jobs claimed at the same instant by 2 worker threads must
produce 2 different nonblank job IDs, with each queued job claimed exactly
once.

**Why this target:** Duplicate processing wastes the system's main compute cost
and can produce conflicting events. Two simultaneous claimers exercise the
database lock boundary directly; any duplicate is unacceptable.

## 4. Failed analysis is bounded and observable

In each trial, a forced model exception must be attempted exactly 3 times,
finish with public status `failed`, expose no raw exception through
`GET /jobs/<job_id>`, and write 3 JSONL run records. Every record must contain
named `timestamp`, `input`, `output`, and `duration_ms` fields.

**Why this target:** A poison job must not retry forever or leak internals, and
each failed attempt must leave enough evidence to diagnose it. Three attempts
allow two transient retries and one final failure without silently losing work.

## 5. The original synchronous route does not regress

In each trial, 1 fixed valid `POST /submit` request must return HTTP 200 with
`content_id`, `model_score`, `style_score`, `confidence`, `guess`, and `label`,
and a matching decision must appear in the audit log.

**Why this target:** The queue is an extension, not a replacement. One fixed
sample per trial checks the original end-to-end contract and its audit trail
without turning this capstone into a second detector-accuracy project.
