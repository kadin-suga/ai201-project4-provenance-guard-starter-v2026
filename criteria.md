# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->
Of 10 pieces of genuine human writing, no more than 1 will be labeled ai in each evaluation trial.


**Why this target:**
A false accusation can harm a real writer more than allowing one AI-generated  submission through. Ten samples provide a meaningful test without making the evaluation too large.


---

## 2.

<!-- Your criterion. -->
Across 5 clearly human and 5 clearly AI-generated samples, the AI samples’ average confidence score will be at least 0.25 higher than the human samples’ average in every trial.


**Why this target:**
The two groups should produce meaningfully different scores, not merely land on   opposite sides of a threshold by a tiny amount. A 0.25 gap leaves room for an unsure region.

Remember that this project’s confidence means the combined AI-likelihood score: higher is more AI-like.


---

## 3.

<!-- Your criterion. -->
A fixed calibration set of at least 6 submissions will produce at least one human, one unsure, and one ai result in every trial.


**Why this target:**
All three labels need to be reachable. If one never appears, the thresholds or scoring range are not functioning as intended.


---

## 4.

<!-- Your criterion. -->
All 5 valid appeals will return HTTP 200, report status under_review, and create an appeal log entry with the matching content_id.


**Why this target:**
An appeal is the writer’s protection against a false positive. It must work every time and leave auditable evidence.


---

## 5.

<!-- Your criterion. -->
All 5 invalid requests—missing text, blank text,non-string text, malformed JSON, and text longer than 10,000 characters—will return a documented 4xx JSON error, and none will produce a 500 response.


**Why this target:**
Bad input should be rejected predictably rather than crashing the service or   producing a meaningless detection result. The 10,000-character limit makes the handling of enormous submissions explicit.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
