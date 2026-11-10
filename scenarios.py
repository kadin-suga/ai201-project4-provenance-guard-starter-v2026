"""Concrete inputs for the five acceptance criteria in ``criteria.md``."""


# These ten samples come from prose already written in this repository before
# the unit 8 evaluation. Keeping the source fixed makes the three trials
# comparable and avoids silently tuning the sample after seeing the scores.
HUMAN_WRITING = [
    (
        "A false accusation can harm a real writer more than allowing one "
        "AI-generated submission through. Ten samples provide a meaningful "
        "test without making the evaluation too large."
    ),
    (
        "The two groups should produce meaningfully different scores, not "
        "merely land on opposite sides of a threshold by a tiny amount. A "
        "quarter-point gap leaves room for an unsure region."
    ),
    (
        "All three labels need to be reachable. If one never appears, the "
        "thresholds or scoring range are not functioning as intended."
    ),
    (
        "An appeal is the writer's protection against a false positive. It "
        "must work every time and leave auditable evidence."
    ),
    (
        "Bad input should be rejected predictably rather than crashing the "
        "service or producing a meaningless detection result. The character "
        "limit makes the handling of enormous submissions explicit."
    ),
    (
        "The system takes an equal-weighted average of the model and style "
        "signals. When they disagree, the average moves toward the unsure "
        "range instead of allowing either signal to decide alone."
    ),
    (
        "I worded the unsure label around the limits of the automated checks "
        "rather than suggesting that the writer did something wrong. It "
        "admits that the result is inconclusive without making an accusation."
    ),
    (
        "Generated writing often uses more regular sentence lengths, repeated "
        "vocabulary, and predictable punctuation. Human writing may be "
        "structurally less regular."
    ),
    (
        "It cannot determine authorship. Plain human writing can be "
        "predictable, while generated writing with unusual or rare language "
        "can be unpredictable."
    ),
    (
        "The service validates the request, measures two different signals, "
        "combines their scores, records the decision, and returns a label that "
        "a reader can understand."
    ),
]


AI_LIKE_WRITING = [
    (
        "The system provides useful results for users. The system processes "
        "each request in a consistent manner. The system records each result "
        "for future reference. These features help the system work well."
    ),
    (
        "Technology is important in modern life. It helps people complete "
        "tasks and communicate with others. It also provides useful tools. "
        "Therefore, technology has many benefits for society."
    ),
    (
        "Education provides many benefits to students. It helps students learn "
        "new skills. It helps students prepare for work. It also helps "
        "students become responsible members of society."
    ),
    (
        "Good communication is useful for every organization. Clear messages "
        "help people understand their tasks. Clear feedback helps people "
        "improve their work. As a result, communication supports success."
    ),
    (
        "Exercise is an important part of a healthy lifestyle. Regular "
        "exercise improves strength and energy. It can also reduce stress. "
        "For these reasons, people should exercise regularly."
    ),
]


SCENARIOS = [
    {
        "name": "my own writing false positives",
        "criterion": 1,
        "texts": HUMAN_WRITING,
    },
    {
        "name": "human and AI score separation",
        "criterion": 2,
        "texts": HUMAN_WRITING[:5] + AI_LIKE_WRITING,
        "groups": {"human": [0, 1, 2, 3, 4], "ai": [5, 6, 7, 8, 9]},
    },
    {
        "name": "all three labels reachable",
        "criterion": 3,
        "texts": [
            HUMAN_WRITING[5],
            HUMAN_WRITING[6],
            HUMAN_WRITING[8],
            AI_LIKE_WRITING[0],
            AI_LIKE_WRITING[1],
            (
                "At dawn I found a cobalt button beneath the radiator; by "
                "lunch, three crows had rearranged the tomatoes outside. "
                "Nobody believed the map, which was fair, because I had drawn "
                "it from memory during a thunderstorm."
            ),
        ],
    },
    {
        "name": "appeal changes status and is logged",
        "criterion": 4,
        "action": "appeal",
        "texts": HUMAN_WRITING[:5],
    },
    {
        "name": "invalid requests return documented 4xx JSON",
        "criterion": 5,
        "requests": [
            {"description": "missing text", "json": {"creator_id": "eval_bad_missing"}},
            {"description": "blank text", "json": {"text": "   ", "creator_id": "eval_bad_blank"}},
            {"description": "non-string text", "json": {"text": 42, "creator_id": "eval_bad_type"}},
            {
                "description": "malformed JSON",
                "raw": '{"text": "unfinished",',
                "content_type": "application/json",
            },
            {
                "description": "text longer than 10,000 characters",
                "json": {"text": "ordinary words " * 800, "creator_id": "eval_bad_huge"},
            },
        ],
    },
]


def validate() -> list[str]:
    """Return scenario-shape problems before a potentially long model run."""
    problems = []
    seen = set()
    for i, scenario in enumerate(SCENARIOS, 1):
        name = scenario.get("name")
        criterion = scenario.get("criterion")
        if not name:
            problems.append(f"scenario {i} has no name")
        if criterion in seen:
            problems.append(f"criterion {criterion} appears more than once")
        seen.add(criterion)

        choices = [key for key in ("texts", "requests") if scenario.get(key)]
        if len(choices) != 1:
            problems.append(f"scenario {i} must have exactly one of texts or requests")
        for j, text in enumerate(scenario.get("texts", []), 1):
            if not isinstance(text, str) or not text.strip():
                problems.append(f"scenario {i}, text {j} is not a nonblank string")
        for j, case in enumerate(scenario.get("requests", []), 1):
            if not isinstance(case, dict) or not ({"json", "raw"} & set(case)):
                problems.append(f"scenario {i}, request {j} needs json or raw")
    if seen != {1, 2, 3, 4, 5}:
        problems.append("scenarios must cover criteria 1 through 5 exactly once")
    return problems
