# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A client sends text and a creator_id to POST /submit.
2. app.py validates the request and creates a unique content_id.
3. detector.py measures how predictable the text is and produces model_score.
4. stylometry.py measures sentence, vocabulary, and punctuation patterns and produces style_score.
5. scoring.py combines both signals into one AI-likelihood score.
6. scoring.py converts that score into a guess and a reader-facing label.
7. audit.py records the decision, and the service returns the result as JSON.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
How predictable the text is to a local GPT-2 model. Lower perplexity becomes
a higher model score, where higher means more AI-like.

**Why that might differ between human and AI writing:**
AI-generated text often uses likely next words, making it easier for a language
model to predict. Human writing may contain more unexpected wording, details,
or transitions.

**What it can't see:**
It cannot determine authorship. Plain human writing can be predictable, while
AI writing with unusual or rare language can be unpredictable. It also reads
only the first 400 model tokens.

### Signal two — the style signal

**What it measures:**
It measures sentence-length variation, vocabulary diversity, and punctuation
density without interpreting meaning. Sentence-length variation contributes
50%, vocabulary diversity contributes 30%, and punctuation density contributes
20%.

**Why that might differ between human and AI writing:**
Generated writing often uses more regular sentence lengths, repeated
vocabulary, and predictable punctuation. Human writing may be structurally
less regular.

**What it can't see:**
It cannot understand meaning or determine authorship. Sentence splitting,
punctuation edits, typos, or quotations can change the score without changing
the underlying ideas. Vocabulary diversity also changes with text length.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**
The system takes an equal-weighted average of the model and style signals.
When they disagree, the average moves toward the unsure range instead of
allowing either signal to make the decision alone.

**The numbers:**
The model signal has weight 0.50 and the style signal has weight 0.50. Scores
at or below 0.35 are human, scores at or above 0.65 are AI, and scores between
those thresholds are unsure.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

My formal-human sample received a model score of 0.2749 and a style score of
0.5899. The combined score was 0.4324. Because the signals disagreed, the
equal-weighted average placed it in the unsure range.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35, inclusive | Our signals suggest this was probably written by a person. |
| unsure | above 0.35 and below 0.65 | Our signals could not reliably determine how this text was written. |
| high-confidence AI | 0.65–1.00, inclusive | Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->
I worded the unsure label around the limits of the automated checks rather than
suggesting that the writer did something wrong. It admits that the result is
inconclusive without making an accusation.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5010/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"The system provides useful results for users. The system processes each request in a consistent manner. The system records each result for future reference. The system also provides clear feedback to users. These features help the system operate effectively and reliably.","creator_id":"sample-writer"}'
```

```json
{
  "confidence": 0.6606,
  "content_id": "46194169-7131-4d9c-9e00-f26d96234d0b",
  "guess": "ai",
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "model_score": 0.6737,
  "style_score": 0.6475
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5010/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"46194169-7131-4d9c-9e00-f26d96234d0b","reasoning":"I wrote this text myself and would like the result reviewed."}'
```

```json
{
  "content_id": "46194169-7131-4d9c-9e00-f26d96234d0b",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5010/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.6606,
      "content_id": "46194169-7131-4d9c-9e00-f26d96234d0b",
      "creator_id": "sample-writer",
      "guess": "ai",
      "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
      "model_score": 0.6737,
      "status": "decided",
      "style_score": 0.6475,
      "timestamp": "2026-11-03T03:58:25+00:00"
    },
    {
      "content_id": "46194169-7131-4d9c-9e00-f26d96234d0b",
      "creator_id": "sample-writer",
      "event": "appeal",
      "reasoning": "I wrote this text myself and would like the result reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-03T03:58:28+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked why `/submit` rejected a multiline curl request
  and requested a review of the route.
- *What came back:* AI identified literal newlines inside the JSON string and
  suggested distinguishing malformed JSON, non-object JSON, and incorrect
  content types.
- *What I changed:* I kept strict JSON parsing, added specific error responses,
  and used escaped newlines instead of silently rewriting malformed input.

**Moment 2**

- *What I asked for:* I asked how `scoring.py::combine_signals` should be built
  and integrated into the submission pipeline.
- *What came back:* AI explained the file-and-function notation and proposed a
  weighted-average path from both signals to the label and audit log.
- *What I changed:* I chose equal model and style weights, recorded both signal
  scores and their combined score, and connected the combined score to the
  reader-facing label.

**Moment 3**

- *What I asked for:* I asked AI to run the supplied attack set, turn my five
  criteria into reproducible scenarios, and help trace each failure to a stage
  and mechanism.
- *What came back:* AI organized the evidence, calculated the three-trial
  verdicts, and identified an undefined-variable block in the appeal route as
  the cause of every appeal failure.
- *What I changed:* I reviewed the recorded responses, chose the appeal failure
  as my one improvement, removed only the bad block, and kept the unchanged
  attack results and remaining misses in this write-up.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

Rate-limit counters are stored in Redis rather than process memory, so API
processes share one limit and restarting the API does not erase the counters.

**Why those numbers and not others:** Five submissions per minute permits a
writer to correct and retry several times, but stops a rapid script after a
small sample. Fifty per day permits normal class use while making large-scale
threshold probing slow.

**What a caller counts as:** Each nonblank `creator_id` is a caller. Malformed
requests without one fall back to the network address. A script can still evade
this by rotating creator IDs; the benefit is that unrelated users behind one
shared address do not consume one another's quota.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

The full 56-row result, including status code, score, content ID, and a manual
HELD/BROKE mark for every input, is in
[`results/attack_run_2026-11-09_1816_before.md`](results/attack_run_2026-11-09_1816_before.md).

| Family | HELD | BROKE | Broken IDs |
|---|---:|---:|---|
| evasion | 1 | 9 | EV01–EV09 |
| false positive | 7 | 1 | FP05 |
| prompt injection | 4 | 2 | PI01, PI02 |
| malformed | 14 | 6 | MF03–MF08 |
| flood, judged as one rate-limit attempt | 12 | 0 | none; five allowed, then seven rejected |
| **Total** | **38** | **18** | |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {"timestamp":"2026-11-10T00:16:12+00:00","content_id":"d02aac49-9514-4045-9b89-313e02773ed3","creator_id":"attacker_EV01","guess":"unsure","model_score":0.1635,"style_score":0.5511,"combined_score":0.3573,"label":"Our signals could not reliably determine how this text was written.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:12+00:00","content_id":"3c0260ff-cff3-4671-b9d0-eb4eb22e09b2","creator_id":"attacker_EV02","guess":"unsure","model_score":0.5943,"style_score":0.14,"combined_score":0.3672,"label":"Our signals could not reliably determine how this text was written.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:13+00:00","content_id":"dea8b215-982c-4b75-bb69-b21c9230cbd2","creator_id":"attacker_EV05","guess":"human","model_score":0.3212,"style_score":0.1949,"combined_score":0.2581,"label":"Our signals suggest this was probably written by a person.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:13+00:00","content_id":"3a239526-2fa5-4684-8db5-14ee2fa1abf5","creator_id":"attacker_EV10","guess":"ai","model_score":0.9792,"style_score":0.7237,"combined_score":0.8515,"label":"Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:13+00:00","content_id":"c561a276-58cc-4fd4-9eaf-6bd10d467e7a","creator_id":"attacker_FP02","guess":"unsure","model_score":0.7387,"style_score":0.5575,"combined_score":0.6481,"label":"Our signals could not reliably determine how this text was written.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:13+00:00","content_id":"4dcd2a07-2c86-4109-b7d7-5b1e8dcdb899","creator_id":"attacker_FP05","guess":"ai","model_score":0.8005,"style_score":0.601,"combined_score":0.7007,"label":"Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:14+00:00","content_id":"d9519bab-bfa1-428c-a7ed-5151c8fbec2d","creator_id":"attacker_PI04","guess":"unsure","model_score":0.4998,"style_score":0.281,"combined_score":0.3904,"label":"Our signals could not reliably determine how this text was written.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:14+00:00","content_id":"a24b1c4a-7135-4905-93a5-0d9a83199329","creator_id":"attacker_MF03","guess":"human","model_score":0.0,"style_score":0.5,"combined_score":0.25,"label":"Our signals suggest this was probably written by a person.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:15+00:00","content_id":"8a6706f8-663b-46ec-8899-3f8c9208580b","creator_id":"attacker_MF08","guess":"ai","model_score":0.9876,"style_score":0.6668,"combined_score":0.8272,"label":"Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.","status":"decided"},
  {"timestamp":"2026-11-10T00:16:15+00:00","creator_id":"attacker_flood","event":"rejected","status":"rejected","reason":"rate_limited","limit":"5 per 1 minute"}
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it: FP05, human-written technical documentation, was
labeled AI at 0.7007. Both signals agreed enough to cross the AI threshold, and
at this point the appeal endpoint also returned a 500, leaving the writer with
an accusation and no working review path.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labeled AI | no more than 1/10 | 0/10 | 0/10 | 0/10 | MET |
| 2. AI-human average score gap | at least 0.25 | 0.333 | 0.333 | 0.333 | MET |
| 3. All labels reachable in calibration set | 3/3 | 2/3 | 2/3 | 2/3 | MISSED |
| 4. Valid appeals succeed and log | 5/5 | 0/5 | 0/5 | 0/5 | MISSED |
| 5. Invalid requests return 4xx JSON | 5/5 | 4/5 | 4/5 | 4/5 | MISSED |

**Real output from trial 1.** Produced by `run_eval.py::main`; the full raw
responses are in
[`results/run_2026-11-09_1817_before.md`](results/run_2026-11-09_1817_before.md).

```json
{
  "criterion_1": {
    "guesses": ["human","human","human","unsure","human","human","human","human","human","unsure"],
    "confidences": [0.2866,0.2729,0.2941,0.3524,0.241,0.3105,0.287,0.2437,0.1318,0.409]
  },
  "criterion_2": {
    "human_confidences": [0.2866,0.2729,0.2941,0.3524,0.241],
    "ai_confidences": [0.5505,0.6114,0.7171,0.5715,0.6632],
    "human_average": 0.2894,
    "ai_average": 0.6227,
    "gap": 0.3333
  },
  "criterion_3": {
    "guesses": ["human","human","human","unsure","unsure","unsure"]
  },
  "criterion_4": [
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"},
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"},
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"},
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"},
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"}
  ],
  "criterion_5": [
    {"sent":"missing text","status":400},
    {"sent":"blank text","status":400},
    {"sent":"non-string text","status":400},
    {"sent":"malformed JSON","status":400},
    {"sent":"text longer than 10,000 characters","status":200,"guess":"ai","confidence":0.9986}
  ]
}
```

**Verdicts and diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->
- Criterion 1 was MET because no trial labeled any of the ten samples AI.
- Criterion 2 was MET because every trial's AI mean (0.6227) exceeded its
  human mean (0.2894) by 0.3333, above the 0.25 target.
- Criterion 3 was MISSED: the calibration set reached human and unsure but not
  AI. The stage is label mapping; the mechanism is that its strongest AI-like
  calibration text scored only 0.6114, below the 0.65 AI boundary.
- Criterion 4 was MISSED: all 15 appeal attempts returned an HTML 500, which
  `run_eval.py` reported as `JSONDecodeError`. The stage is the route; the
  mechanism was an undefined `creator_id` reference in `app.py::appeal` before
  it could call `audit.log_appeal`.
- Criterion 5 was MISSED: four cases returned JSON 400s, but the 10,000+
  character input was scored and returned 200 in all trials. The stage is the
  route; the mechanism is that `/submit` checked type and blankness but had no
  maximum-length validation.

The 18 broken attacks form five mechanisms:

- EV01, EV02, EV03, EV06, and EV07 broke at signal two. Typos, sentence
  splitting, quotations, uneven lengths, and punctuation changed the surface
  statistics enough to pull AI text below the AI boundary.
- EV04 and EV08 broke at signal one. Rare wording increased perplexity and the
  400-token window ignored the later evidence, reducing the model score.
- EV05 and EV09 broke across both signals and the combining rule. A heavy edit
  or human opening lowered one or both inputs, and the equal average converted
  disagreement into human/unsure.
- FP05 broke across both signals and the label mapping: predictable technical
  prose scored 0.8005 on the model and 0.6010 on style; their 0.7007 average
  crossed the 0.65 AI boundary despite genuine human authorship.
- PI01 and PI02 broke at the signal stages. The service did not execute their
  instructions, but the instruction-shaped wording itself scored 0.3408 and
  0.1961, so both achieved a human label anyway.
- MF03–MF08 broke at the route. Nonblank control characters, punctuation,
  single-token, emoji, right-to-left, and 60,000-character text passed type
  validation, so signals designed for English prose produced meaningless
  decisions rather than 4xx errors.

Across the failures, the main pattern is insufficient input validation plus
signals that measure easily manipulated surface predictability and shape.

---

## The Improvement

**What I changed:** I removed one erroneous block in `app.py::appeal` that
replaced the submitted content ID and referenced undefined `creator_id` and
`model_score` variables. No scoring, threshold, validation, or rate-limit
setting changed.

**Which diagnosis pointed at it:** Criterion 4 failed 0/5 in every trial and
the Flask traceback named the undefined variable on the appeal route. This was
also the most urgent protection after FP05 falsely accused a human writer.

### Attack Run — After

The full after result is
[`results/attack_run_2026-11-09_1821_after.md`](results/attack_run_2026-11-09_1821_after.md),
and the after criteria are in
[`results/run_2026-11-09_1821_after.md`](results/run_2026-11-09_1821_after.md).

| Measure | Before | After |
|---|---:|---:|
| Attack set held | 38/56 | 38/56 |
| Attack set broke | 18/56 | 18/56 |
| Criterion 1 | MET, 0/10 AI | MET, 0/10 AI |
| Criterion 2 | MET, 0.333 gap | MET, 0.333 gap |
| Criterion 3 | MISSED, 2/3 labels | MISSED, 2/3 labels |
| Criterion 4 | MISSED, 0/5 | MET, 5/5 |
| Criterion 5 | MISSED, 4/5 | MISSED, 4/5 |

Every after-run attack received the same score and verdict because the one
change touched only `/appeal`: BROKE were EV01–EV09, FP05, PI01, PI02, and
MF03–MF08; all other IDs were HELD.

**Did it help, and how do I know:** Yes, for the diagnosed problem. Appeal
success moved from 0/5 to 5/5 in all three trials; every after appeal returned
200 with `status: "under_review"` and `logged: true`. The attack result stayed
38 held and 18 broken, which is expected because the improvement did not alter
`/submit`.

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

- EV01–EV09 still evade the detector. I would test stronger semantic and
  document-level signals, but stopped because this milestone permits one
  isolated change and combining more changes would hide which one helped.
- FP05 still falsely accuses human technical prose. I would raise the AI
  threshold or require manual review for every AI-band result, then measure the
  added false negatives.
- PI01 and PI02 still get human labels. I would treat imperative/system-message
  patterns as a reason for review, not as proof of AI, because blocking prompt
  language would also catch legitimate writing about prompts.
- MF03–MF08 still accept unsupported or enormous inputs. I would add a 10,000
  character ceiling plus a minimum usable-word check before either signal.
- Criterion 3 still misses because its fixed set reaches only two labels. I
  would recalibrate the samples and thresholds without changing the original
  target. Criterion 5 still misses because oversized input returns 200; the
  route validation above would address it.

**The trade I'd make if this ran for real:** I would bias toward fewer wrong
accusations by widening the unsure band and requiring human review before any
adverse action. More AI-written text would pass initially, so the site would
pay through extra moderation, while genuine writers would be less likely to
pay through an automated accusation.

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

## Capstone

**What This Extends**

This extends Provenance Guard, the system that scores submitted writing with a
local model signal and a stylometry signal, maps the combined score to a
human/unsure/AI label, supports appeals, and records an audit trail. The new
capability is a durable asynchronous analysis path: `POST /jobs` stores work in
PostgreSQL, returns a pollable job ID immediately, and a separate worker claims,
scores, retries, and completes that work. The original synchronous `/submit`
path remains available and is included in the regression criteria.

**The Shape**

I chose **Shape C — operational scaffolding**. The extension moves slow model
work out of the request, uses PostgreSQL row locking so concurrent workers do
not claim the same job, retries failed jobs with bounded backoff, recovers
expired worker leases, and uses Redis for shared rate-limit counters.

Out of scope: I did not add a second detector or change the model/stylometry
scoring, did not rebuild the interface, and did not deploy a hosted copy. Those
would each add a second project and make it harder to isolate whether the queue
itself works.

**Running It**

This is **Path B — local with logs**. From a configured checkout, the complete
start command is `./run_local.sh`; the service is then at
`http://127.0.0.1:5000`. [RUNNING.md](RUNNING.md) gives the environment,
one-time setup, verification request, polling step, and manual multi-terminal
alternative.

**Instrumentation**

Every worker attempt appends one JSON object to `logs/run_records.jsonl` through
`audit.py::log_run`. Each record names the UTC timestamp, job/creator/worker,
attempt number, input, output (result or error/status), and measured
`duration_ms`. Failures are records, not missing rows. PostgreSQL separately
stores durable job state and lifecycle events; `logs/audit.jsonl` remains the
original synchronous decision/appeal log.

Ten entries from the measured after run are pasted below as text. Entries 2–4,
6–8, and 10 show the deliberately failed path, including its final transition
to `failed`.

```jsonl
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"1f435e8b-47a4-4e67-b34b-5ae757169c36","creator_id":"capstone-c2-1-f14e38f3-6b5a-4881-b577-260165b333ac","worker_id":"capstone-c2-worker-1","attempt":1,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"completed","model_score":0.3839,"style_score":0.4774,"confidence":0.4306,"guess":"unsure","label":"Our signals could not reliably determine how this text was written."},"duration_ms":1103.46}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"e1b4dce0-0c4b-4db9-878b-90b653aaa17f","creator_id":"capstone-c4-1-6f867f22-a289-43f1-8b55-c7bd6f170859","worker_id":"capstone-c4-worker-1-0","attempt":1,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"queued","error":"RuntimeError: forced failure"},"duration_ms":6.77}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"e1b4dce0-0c4b-4db9-878b-90b653aaa17f","creator_id":"capstone-c4-1-6f867f22-a289-43f1-8b55-c7bd6f170859","worker_id":"capstone-c4-worker-1-1","attempt":2,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"queued","error":"RuntimeError: forced failure"},"duration_ms":2.88}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"e1b4dce0-0c4b-4db9-878b-90b653aaa17f","creator_id":"capstone-c4-1-6f867f22-a289-43f1-8b55-c7bd6f170859","worker_id":"capstone-c4-worker-1-2","attempt":3,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"failed","error":"RuntimeError: forced failure"},"duration_ms":3.34}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"a9b28b7f-c245-40a4-92bc-2a17883b208b","creator_id":"capstone-c2-2-dcce83c6-6565-4d64-b5a7-084530dfd4e5","worker_id":"capstone-c2-worker-2","attempt":1,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"completed","model_score":0.3839,"style_score":0.4774,"confidence":0.4306,"guess":"unsure","label":"Our signals could not reliably determine how this text was written."},"duration_ms":35.77}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"92aae0d3-e7c5-40b2-8755-6a7ccae8cbbe","creator_id":"capstone-c4-2-6cad1c4b-a944-4efb-a7bb-c1faddf65f14","worker_id":"capstone-c4-worker-2-0","attempt":1,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"queued","error":"RuntimeError: forced failure"},"duration_ms":2.24}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"92aae0d3-e7c5-40b2-8755-6a7ccae8cbbe","creator_id":"capstone-c4-2-6cad1c4b-a944-4efb-a7bb-c1faddf65f14","worker_id":"capstone-c4-worker-2-1","attempt":2,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"queued","error":"RuntimeError: forced failure"},"duration_ms":2.25}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"92aae0d3-e7c5-40b2-8755-6a7ccae8cbbe","creator_id":"capstone-c4-2-6cad1c4b-a944-4efb-a7bb-c1faddf65f14","worker_id":"capstone-c4-worker-2-2","attempt":3,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"failed","error":"RuntimeError: forced failure"},"duration_ms":1.83}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"c9dc445a-9f70-48f3-861d-4d1c245f45ab","creator_id":"capstone-c2-3-1228403d-66aa-4383-a2e0-ec4631d78e1d","worker_id":"capstone-c2-worker-3","attempt":1,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"completed","model_score":0.3839,"style_score":0.4774,"confidence":0.4306,"guess":"unsure","label":"Our signals could not reliably determine how this text was written."},"duration_ms":41.2}
{"timestamp":"2026-11-21T19:12:10+00:00","job_id":"8908d0c9-8b0a-4fd7-8054-3778e22396f0","creator_id":"capstone-c4-3-06090d83-50cf-443b-af24-107d29f16c55","worker_id":"capstone-c4-worker-3-0","attempt":1,"input":{"text":"A small river crossed the park behind the library. On clear mornings, neighbors stopped on the footbridge to watch ducks move through the reeds. The scene changed with the weather, but the path remained busy all year."},"output":{"status":"queued","error":"RuntimeError: forced failure"},"duration_ms":1.92}
```

The complete 22-entry evidence file is
[`logs/run_records.jsonl`](logs/run_records.jsonl).

**What It Costs**

There is no per-request API spend: GPT-2 runs locally. I measured seconds of
compute by warming the model once, then timing `worker.py::process_job` around
the real model signal, style signal, database completion, and structured log
write for ten separate jobs. The measured times were 0.0473, 0.0410, 0.0446,
0.0401, 0.0458, 0.0393, 0.0447, 0.0424, 0.0341, and 0.0370 seconds. Their mean
was **0.0416 seconds of warm local compute per run**. Model loading is a startup
cost and is deliberately outside this steady-state per-run number; the first
criterion-2 analysis after loading took 1.117 seconds end to end.

At one run each for 100 people per day: `0.0416 seconds/run × 100 runs = 4.16
seconds of local compute per day`, plus one model load whenever the worker
restarts. The raw measurements are in `results/capstone_after.json` under
`cost`.

**Run Log and Verdicts**

The before run used commit `a06a611`'s isolated runner against the system before
structured worker logging. No settings changed between the three trials.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Valid work accepted promptly | 5/5 HTTP 202, complete handles, each under 500 ms | 5/5; max 243.80 ms | 5/5; max 2.99 ms | 5/5; max 2.56 ms | MET |
| 2. Queued job completes | completed with all result fields under 60 s | completed, 1.147 s | completed, 0.038 s | completed, 0.042 s | MET |
| 3. Concurrent claims are unique | 2/2 distinct jobs | 2/2 unique | 2/2 unique | 2/2 unique | MET |
| 4. Failure is bounded and observable | failed after 3 attempts, generic public error, 3/3 structured logs | failed after 3; 0/3 logs | failed after 3; 0/3 logs | failed after 3; 0/3 logs | MISSED |
| 5. Original `/submit` still works | HTTP 200, six response fields, matching audit row | 200; 1 audit row | 200; 1 audit row | 200; 1 audit row | MET |

Verdict and diagnosis by criterion:

1. **MET.** The route/database stage persisted all 15 requests and returned
   pollable handles. The high first value is connection-pool startup, still
   below the 500 ms target.
2. **MET.** The worker stage completed all three real GPT-2 analyses with every
   required result field and valid 0–1 scores.
3. **MET.** PostgreSQL's `FOR UPDATE SKIP LOCKED` claim stage gave the two
   simultaneous threads different jobs in every trial.
4. **MISSED.** The retry stage correctly stopped at three attempts and hid the
   raw exception, but the observability half was 0/3 in every trial. The cause
   was `worker.py::process_job`: it only sent messages to the console and job
   lifecycle fields to PostgreSQL. Neither path wrote the named input, output,
   and elapsed duration required for a run record.
5. **MET.** The original route, scoring, labeling, response, and audit path
   remained intact in all three trials.

Real trial-1 output below was produced by the named functions in
`run_capstone.py`; the unabridged output is in
[`results/capstone_before.json`](results/capstone_before.json).

```json
{"criterion_1":{"producer":"run_capstone.py::_criterion_1","http":202,"job_id":"6ab67976-d47f-4b0c-9e32-11c3c00d40ca","duration_ms":243.8,"status_get":200}}
{"criterion_2":{"producer":"run_capstone.py::_criterion_2","status":"completed","duration_seconds":1.147,"confidence":0.4306,"guess":"unsure"}}
{"criterion_3":{"producer":"run_capstone.py::_criterion_3","expected":["507ef68a-6145-4313-aef9-9d4a4b594885","eadb40e6-6e2f-4817-921b-b080dfa3979e"],"claimed":["eadb40e6-6e2f-4817-921b-b080dfa3979e","507ef68a-6145-4313-aef9-9d4a4b594885"],"errors":[]}}
{"criterion_4":{"producer":"run_capstone.py::_criterion_4","status":"failed","attempts":3,"public_message":"Analysis could not be completed.","run_records":[]}}
{"criterion_5":{"producer":"run_capstone.py::_criterion_5","http":200,"content_id":"664d93ab-dbd2-491f-b4cf-2721ea4a909f","confidence":0.4306,"guess":"unsure","audit_entries":1}}
```

**The Improvement**

I made one change: each worker attempt now times itself and calls
`audit.py::log_run` with its input and either its completed result or persisted
failure. The diagnosis pointed directly at the worker because retries and the
public failure response already behaved correctly; only durable attempt-level
observability was absent.

I reran all five criteria without changing their targets:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Valid work accepted promptly | 5/5 HTTP 202, complete handles, each under 500 ms | 5/5; max 292.12 ms | 5/5; max 3.99 ms | 5/5; max 4.03 ms | MET |
| 2. Queued job completes | completed with all result fields under 60 s | completed, 1.117 s | completed, 0.038 s | completed, 0.043 s | MET |
| 3. Concurrent claims are unique | 2/2 distinct jobs | 2/2 unique | 2/2 unique | 2/2 unique | MET |
| 4. Failure is bounded and observable | failed after 3 attempts, generic public error, 3/3 structured logs | failed after 3; 3/3 logs | failed after 3; 3/3 logs | failed after 3; 3/3 logs | MET |
| 5. Original `/submit` still works | HTTP 200, six response fields, matching audit row | 200; 1 audit row | 200; 1 audit row | 200; 1 audit row | MET |

| Measure | Before | After |
|---|---:|---:|
| Criteria met | 4/5 | 5/5 |
| Failed attempts with complete structured records | 0/9 | 9/9 |
| Criterion 4 | MISSED in 3/3 trials | MET in 3/3 trials |

The change helped exactly the diagnosed issue: criterion 4 moved from 0/3 to
3/3 logged attempts in every trial while the other four verdicts stayed MET.
The full after evidence is in
[`results/capstone_after.json`](results/capstone_after.json).

**What's Still Broken**

All five criteria are met after the improvement, but criterion 2's 60-second
target was too loose for this machine: the slowest measured completion was
1.147 seconds. I would tighten it to **2 seconds for a warm local worker** and
separately track cold model-load time, rather than letting one target mix those
two very different states.

The structured log stores full submitted text because the required record must
show what came in. In a real writing service that creates a privacy and disk
retention risk; I would add access controls, a retention limit, and a documented
redaction policy before accepting private writing. I stopped because this
capstone scoped one measured improvement, and changing the evidence format in
the same comparison would make the before/after result harder to interpret.

If this were real and I had another unit, the first thing I would do is run
multiple full analysis workers under concurrent load, not just concurrent claim
threads. That would reveal whether CPU/model contention changes the completion
target or makes additional workers slower instead of increasing throughput.

**How I Used AI**

**Moment 1**

- *What I asked for:* I asked AI to update the existing repository against the
  complete capstone brief and keep the work to one extension.
- *What came back:* AI identified the already-built PostgreSQL queue, worker
  leases/retries, and Redis counters as Shape C, and drafted five capstone
  criteria around that boundary.
- *What changed:* The old seven-criterion file was replaced with five capstone
  criteria and committed before any capstone result file. The declared scope
  excludes another detector, an interface rebuild, and hosting.

**Moment 2**

- *What I asked for:* I asked AI to implement a repeatable before/after harness
  and ensure every conclusion was backed by saved real output.
- *What came back:* The first harness run exposed fixture contamination: queued
  jobs from criterion 1 were being claimed by later criteria. AI identified the
  mismatch between expected and claimed IDs.
- *What changed:* That invalid, uncommitted output was deleted; each criterion's
  fixtures were isolated and the baseline was rerun. The corrected evidence
  exposed one real miss—missing worker run records—which became the measured
  improvement.
