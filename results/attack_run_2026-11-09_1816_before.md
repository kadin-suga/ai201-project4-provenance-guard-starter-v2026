# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 18:16
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d02aac49-9514-4045-9b89-313e02773ed3` | unsure | 0.357 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3c0260ff-cff3-4671-b9d0-eb4eb22e09b2` | unsure | 0.367 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d784dd53-6ad3-4638-8f01-a7f3b41f4d17` | unsure | 0.503 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `509aad63-9559-4737-8605-f5715af1bf9b` | unsure | 0.575 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `dea8b215-982c-4b75-bb69-b21c9230cbd2` | human | 0.258 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `b6bbc831-fc97-4989-915f-fd67e4b24b05` | unsure | 0.387 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `22f0cdda-6059-4985-8522-6229aa3bd241` | unsure | 0.614 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `20d7e500-c2ab-48f4-bbf6-4901da0dbc1f` | human | 0.340 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `316ad6cd-3118-4aa9-a7e9-10d28ebadcca` | unsure | 0.517 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `3a239526-2fa5-4684-8db5-14ee2fa1abf5` | ai | 0.852 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `1ae8571a-e5a7-4ce3-8711-432cd85fd2ec` | unsure | 0.513 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c561a276-58cc-4fd4-9eaf-6bd10d467e7a` | unsure | 0.648 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `64969972-02ce-46d2-9109-57b1f27f08e6` | unsure | 0.648 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d1fc52c6-5104-475a-8f2c-f0468ed3e194` | unsure | 0.619 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `4dcd2a07-2c86-4109-b7d7-5b1e8dcdb899` | ai | 0.701 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `77d4c085-4ad5-4d58-a028-7227e025a383` | unsure | 0.615 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `db582892-e571-47f6-9525-0b1c940dabfa` | unsure | 0.628 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `50c54901-e5fe-4142-8ff6-2baf5ee7531b` | human | 0.267 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4e966534-4007-43de-baf5-4ff790f5af5a` | human | 0.341 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a50c9b51-5e18-4440-a54e-1c7a483920d0` | human | 0.196 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `b314960f-21eb-47a5-bd3d-37f057179985` | unsure | 0.510 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `d9519bab-bfa1-428c-a7ed-5151c8fbec2d` | unsure | 0.390 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `39cef7d8-764f-4354-ab87-a5ac5cb42881` | unsure | 0.413 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `e9d9524e-3d38-4984-8620-989ee0421332` | unsure | 0.488 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `a24b1c4a-7135-4905-93a5-0d9a83199329` | human | 0.250 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `14b16b8b-0a7e-4286-ba5c-1840a127dc57` | unsure | 0.406 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `1ce920ad-eac6-465d-afa2-7b8b3d960dab` | ai | 0.849 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `cbb8461a-9c46-4329-a9ee-7219cabdfd4d` | ai | 0.898 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `19d897e0-1740-4155-8b31-73e081be9d82` | ai | 0.941 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `8a6706f8-663b-46ec-8899-3f8c9208580b` | ai | 0.827 | BROKE |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `849a4153-ab7b-4605-809d-e6689a616596` | human | 0.342 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9ea218f7-57fc-47e6-8613-877b37f88a1a` | human | 0.342 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `15d1619d-5495-43e2-9855-a723f9acd742` | human | 0.342 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `924b02b7-6529-433f-96fa-2963ee2083df` | human | 0.342 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `923e6fe2-23ea-4140-8e33-a1eb0f6165f1` | human | 0.342 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Judged totals:** 38 HELD, 18 BROKE. The flood family is judged as one
rate-limit attack: accepting the configured five-request allowance and rejecting
the following seven means every row in that family contributed to a held attack.

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "d02aac49-9514-4045-9b89-313e02773ed3",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3573,
  "model_score": 0.1635,
  "style_score": 0.5511,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "3c0260ff-cff3-4671-b9d0-eb4eb22e09b2",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3672,
  "model_score": 0.5943,
  "style_score": 0.14,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d784dd53-6ad3-4638-8f01-a7f3b41f4d17",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.503,
  "model_score": 0.6662,
  "style_score": 0.3399,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "509aad63-9559-4737-8605-f5715af1bf9b",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.575,
  "model_score": 0.6114,
  "style_score": 0.5385,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "dea8b215-982c-4b75-bb69-b21c9230cbd2",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2581,
  "model_score": 0.3212,
  "style_score": 0.1949,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "b6bbc831-fc97-4989-915f-fd67e4b24b05",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3874,
  "model_score": 0.5727,
  "style_score": 0.2021,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "22f0cdda-6059-4985-8522-6229aa3bd241",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6137,
  "model_score": 0.5862,
  "style_score": 0.6411,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "20d7e500-c2ab-48f4-bbf6-4901da0dbc1f",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3398,
  "model_score": 0.2452,
  "style_score": 0.4345,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "316ad6cd-3118-4aa9-a7e9-10d28ebadcca",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5168,
  "model_score": 0.7042,
  "style_score": 0.3293,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "3a239526-2fa5-4684-8db5-14ee2fa1abf5",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8515,
  "model_score": 0.9792,
  "style_score": 0.7237,
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "1ae8571a-e5a7-4ce3-8711-432cd85fd2ec",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5128,
  "model_score": 0.6175,
  "style_score": 0.4081,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c561a276-58cc-4fd4-9eaf-6bd10d467e7a",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6481,
  "model_score": 0.7387,
  "style_score": 0.5575,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "64969972-02ce-46d2-9109-57b1f27f08e6",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.648,
  "model_score": 0.8051,
  "style_score": 0.4909,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "d1fc52c6-5104-475a-8f2c-f0468ed3e194",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6189,
  "model_score": 0.8329,
  "style_score": 0.4048,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "4dcd2a07-2c86-4109-b7d7-5b1e8dcdb899",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7007,
  "model_score": 0.8005,
  "style_score": 0.601,
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "77d4c085-4ad5-4d58-a028-7227e025a383",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6148,
  "model_score": 0.8814,
  "style_score": 0.3481,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "db582892-e571-47f6-9525-0b1c940dabfa",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6277,
  "model_score": 0.8816,
  "style_score": 0.3737,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "50c54901-e5fe-4142-8ff6-2baf5ee7531b",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2668,
  "model_score": 0.3223,
  "style_score": 0.2113,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "4e966534-4007-43de-baf5-4ff790f5af5a",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3408,
  "model_score": 0.4625,
  "style_score": 0.2192,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "a50c9b51-5e18-4440-a54e-1c7a483920d0",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1961,
  "model_score": 0.2044,
  "style_score": 0.1877,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "b314960f-21eb-47a5-bd3d-37f057179985",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5096,
  "model_score": 0.5943,
  "style_score": 0.4248,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "d9519bab-bfa1-428c-a7ed-5151c8fbec2d",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3904,
  "model_score": 0.4998,
  "style_score": 0.281,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "39cef7d8-764f-4354-ab87-a5ac5cb42881",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4129,
  "model_score": 0.6401,
  "style_score": 0.1857,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "e9d9524e-3d38-4984-8620-989ee0421332",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4883,
  "model_score": 0.5583,
  "style_score": 0.4182,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "a24b1c4a-7135-4905-93a5-0d9a83199329",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.25,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "14b16b8b-0a7e-4286-ba5c-1840a127dc57",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4056,
  "model_score": 0.0112,
  "style_score": 0.8,
  "label": "Our signals could not reliably determine how this text was written.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "1ce920ad-eac6-465d-afa2-7b8b3d960dab",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8488,
  "model_score": 0.9976,
  "style_score": 0.7,
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "cbb8461a-9c46-4329-a9ee-7219cabdfd4d",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8984,
  "model_score": 0.9969,
  "style_score": 0.8,
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "19d897e0-1740-4155-8b31-73e081be9d82",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9413,
  "model_score": 0.9064,
  "style_score": 0.9763,
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "8a6706f8-663b-46ec-8899-3f8c9208580b",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8272,
  "model_score": 0.9876,
  "style_score": 0.6668,
  "label": "Our signals found patterns associated with AI-generated text. This is not proof of authorship, and the writer may request a review.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "849a4153-ab7b-4605-809d-e6689a616596",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3416,
  "model_score": 0.0287,
  "style_score": 0.6545,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "9ea218f7-57fc-47e6-8613-877b37f88a1a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3416,
  "model_score": 0.0287,
  "style_score": 0.6545,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "15d1619d-5495-43e2-9855-a723f9acd742",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3416,
  "model_score": 0.0287,
  "style_score": 0.6545,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "924b02b7-6529-433f-96fa-2963ee2083df",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3416,
  "model_score": 0.0287,
  "style_score": 0.6545,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "923e6fe2-23ea-4140-8e33-a1eb0f6165f1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3416,
  "model_score": 0.0287,
  "style_score": 0.6545,
  "label": "Our signals suggest this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
