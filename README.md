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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

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
