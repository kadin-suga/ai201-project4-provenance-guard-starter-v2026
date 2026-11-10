# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 18:21
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `12fa1bad-01e7-48a1-8ac3-5a070cd3bcd8` | unsure | 0.357 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `8c8bd4ec-b67d-4f76-984a-e1ee02402d16` | unsure | 0.367 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `2d03e12f-f937-4dc6-9cb1-a72046f0aa80` | unsure | 0.503 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `52444a09-2a60-404a-ba8b-48d97d4e709a` | unsure | 0.575 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c5d9db57-58f4-4a67-9d0c-a996296a3971` | human | 0.258 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `8f1227aa-ff7f-4a9f-b407-c79cc72ca7d4` | unsure | 0.387 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `483808c9-cfc2-421c-a4a6-427ec5653628` | unsure | 0.614 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `f839c3cd-afd1-455f-ba1c-3fc6afdd1abd` | human | 0.340 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `d9cb7f84-b0ba-4b19-a39b-88f6cc5a1a00` | unsure | 0.517 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0fd96e82-01a5-4c0b-b33c-e9da621d8588` | ai | 0.852 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3f6439ed-6bb7-4fa3-82d5-2b173e4e8191` | unsure | 0.513 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `450c02c4-f611-4e57-9466-437bd9f18705` | unsure | 0.648 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `df6b0199-46e7-49fc-a53e-3b2fe84acc83` | unsure | 0.648 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `ec81a4d5-4430-4e3f-92bd-09b0b1758e36` | unsure | 0.619 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `69419c78-10c4-420d-a7b1-d944084c744c` | ai | 0.701 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c0f89c2c-c65e-4ad7-8069-d6951bf40ebd` | unsure | 0.615 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `a26880db-13cc-4d6c-9aa1-5bce9a4c30dc` | unsure | 0.628 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `1e1df9fb-ce50-440b-8450-3ff4cd5a15c5` | human | 0.267 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `3d49b694-1a8f-4711-b7c2-d8fc67b166a9` | human | 0.341 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `6c64c76a-6e2f-46ff-95e6-1390d235615b` | human | 0.196 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a4930c45-9abe-4069-83fd-8786479d1750` | unsure | 0.510 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `be5910aa-5b2c-4b89-990f-f2fd160d34d1` | unsure | 0.390 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `859762ff-5a16-4ea9-bafc-b4acc1184c97` | unsure | 0.413 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `01b0efa1-134d-4243-8fce-ec258a09fdbb` | unsure | 0.488 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `13a5bee4-901e-4338-960e-c961dfc08534` | human | 0.250 |  |
| MF04 | malformed | text is only punctuation | 200 | `13a42d19-b23d-4f1c-bd5c-94b07e3d7767` | unsure | 0.406 |  |
| MF05 | malformed | text is a very long single word | 200 | `4bbf70fd-1895-44d9-b2f1-b37d86914335` | ai | 0.849 |  |
| MF06 | malformed | text is emoji only | 200 | `68dd5108-0a13-4eb3-b728-999997f715a4` | ai | 0.898 |  |
| MF07 | malformed | text is right-to-left script | 200 | `215ee75d-d174-483b-99de-da7f285dfd82` | ai | 0.941 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `f2c03cb3-2bb5-45a9-80d8-6980a603ea06` | ai | 0.827 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b995aff6-11af-4d5b-b2ec-287d0f3ea685` | human | 0.342 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fdfd8a38-9183-48d4-af6a-485448c459e9` | human | 0.342 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `da3b1efa-257a-4609-990d-59ec67437fcb` | human | 0.342 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `59a55e76-1e0d-4c31-b1a4-c5c9708ba8c2` | human | 0.342 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `187bba1c-8483-4430-8949-aa1f657c9ccf` | human | 0.342 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

**Manual verdicts:**

| Verdict | Attack IDs | Count |
|---|---|---:|
| BROKE | EV01, EV02, EV03, EV04, EV05, EV06, EV07, EV08, EV09, FP05, PI01, PI02, MF03, MF04, MF05, MF06, MF07, MF08 | 18 |
| HELD | EV10, FP01, FP02, FP03, FP04, FP06, FP07, FP08, PI03, PI04, PI05, PI06, MF01, MF02, RQ01, RQ02, RQ03, RQ04, RQ05, RQ06, RQ07, RQ08, RQ09, RQ10, RQ11, RQ12, FL01_01, FL01_02, FL01_03, FL01_04, FL01_05, FL01_06, FL01_07, FL01_08, FL01_09, FL01_10, FL01_11, FL01_12 | 38 |

The flood family is judged collectively: five allowed requests followed by
seven HTTP 429 responses means the configured limiter held.

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
  "content_id": "12fa1bad-01e7-48a1-8ac3-5a070cd3bcd8",
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
  "content_id": "8c8bd4ec-b67d-4f76-984a-e1ee02402d16",
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
  "content_id": "2d03e12f-f937-4dc6-9cb1-a72046f0aa80",
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
  "content_id": "52444a09-2a60-404a-ba8b-48d97d4e709a",
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
  "content_id": "c5d9db57-58f4-4a67-9d0c-a996296a3971",
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
  "content_id": "8f1227aa-ff7f-4a9f-b407-c79cc72ca7d4",
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
  "content_id": "483808c9-cfc2-421c-a4a6-427ec5653628",
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
  "content_id": "f839c3cd-afd1-455f-ba1c-3fc6afdd1abd",
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
  "content_id": "d9cb7f84-b0ba-4b19-a39b-88f6cc5a1a00",
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
  "content_id": "0fd96e82-01a5-4c0b-b33c-e9da621d8588",
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
  "content_id": "3f6439ed-6bb7-4fa3-82d5-2b173e4e8191",
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
  "content_id": "450c02c4-f611-4e57-9466-437bd9f18705",
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
  "content_id": "df6b0199-46e7-49fc-a53e-3b2fe84acc83",
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
  "content_id": "ec81a4d5-4430-4e3f-92bd-09b0b1758e36",
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
  "content_id": "69419c78-10c4-420d-a7b1-d944084c744c",
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
  "content_id": "c0f89c2c-c65e-4ad7-8069-d6951bf40ebd",
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
  "content_id": "a26880db-13cc-4d6c-9aa1-5bce9a4c30dc",
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
  "content_id": "1e1df9fb-ce50-440b-8450-3ff4cd5a15c5",
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
  "content_id": "3d49b694-1a8f-4711-b7c2-d8fc67b166a9",
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
  "content_id": "6c64c76a-6e2f-46ff-95e6-1390d235615b",
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
  "content_id": "a4930c45-9abe-4069-83fd-8786479d1750",
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
  "content_id": "be5910aa-5b2c-4b89-990f-f2fd160d34d1",
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
  "content_id": "859762ff-5a16-4ea9-bafc-b4acc1184c97",
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
  "content_id": "01b0efa1-134d-4243-8fce-ec258a09fdbb",
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
  "content_id": "13a5bee4-901e-4338-960e-c961dfc08534",
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
  "content_id": "13a42d19-b23d-4f1c-bd5c-94b07e3d7767",
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
  "content_id": "4bbf70fd-1895-44d9-b2f1-b37d86914335",
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
  "content_id": "68dd5108-0a13-4eb3-b728-999997f715a4",
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
  "content_id": "215ee75d-d174-483b-99de-da7f285dfd82",
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
  "content_id": "f2c03cb3-2bb5-45a9-80d8-6980a603ea06",
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
  "content_id": "b995aff6-11af-4d5b-b2ec-287d0f3ea685",
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
  "content_id": "fdfd8a38-9183-48d4-af6a-485448c459e9",
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
  "content_id": "da3b1efa-257a-4609-990d-59ec67437fcb",
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
  "content_id": "59a55e76-1e0d-4c31-b1a4-c5c9708ba8c2",
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
  "content_id": "187bba1c-8483-4430-8949-aa1f657c9ccf",
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
