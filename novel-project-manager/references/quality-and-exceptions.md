# Quality And Exceptions

Use this reference for scoring project complexity, choosing tool-like checks, and handling common web-novel production failures.

## Complexity Score

Score each dimension from 1 to 5:

- Worldbuilding complexity
- Number/depth of characters
- Number of plot lines
- Professional research need
- Update intensity

Interpretation:

- 5-10: light management; PRD + task list is enough.
- 11-17: normal serial management; use chapter gates and consistency records.
- 18-25: high-risk long-form project; require volume/phase governance and regular audits.

## Tool Map

Core checks:

- chapter outline generation
- dialogue optimization
- plot conflict detection
- pacing analysis
- sensitive-content review
- chapter attraction scoring
- reader feedback analysis

Standard checks:

- power-system balance
- worldbuilding consistency
- foreshadowing management
- emotion curve
- chapter hook
- update cadence
- word count and progress
- comparable-market research
- popular-element analysis
- golden-finger design
- progression-system planning
- dungeon/case/arc generation
- romance-line development
- antagonist shaping
- payoff-density analysis

Extended checks:

- poem/name generation for xianxia
- map assistance
- timeline management
- multi-line coordination
- system-interface design
- infinite-flow instance design
- cosmic-horror integration
- science-fiction plausibility
- historical verification
- food description enhancement
- battle scene optimization
- daily-life plot design

Do not pretend all checks are automated. Treat this map as a dispatch list: decide whether a script, research pass, or human-readable review is needed.

## Model/Agent Division

Use this as a role split, not a hard dependency:

- Main reasoning/writing model: core plot, character depth, complex worldbuilding, key chapters.
- Research model/tool: historical/cultural background, domain facts, trend and audience preference research.
- Fast fallback model/tool: daily-life filler, dialogue polish, scene detail, transition paragraphs.

When only one model is available, simulate the split by doing the passes separately.

## Quality Gates

First 3 chapters:

- genre/promise is visible within the opening;
- protagonist has a concrete problem;
- the selling point is shown, not only explained;
- first hook points to the next chapter;
- no long lore dump before conflict.

Every chapter:

- one dominant event;
- state A -> state B movement;
- at least one payoff, reveal, relationship move, upgrade, or tactical win;
- active pressure at the end;
- no contradiction with PRD/world/character records.

Every 5-10 chapters:

- repeated payoff pattern is not stale;
- protagonist agency remains visible;
- supporting cast is not only functional;
- foreshadowing has active status;
- timeline and power progression still make sense.

Volume ending:

- volume conflict is resolved or transformed;
- next volume's problem is seeded;
- major foreshadowing is either paid or deliberately carried;
- reader receives enough compensation for setbacks.

## Failure Modes

### Stuck For More Than Two Days

Trigger: same task stays `doing` or `blocked` beyond its expected duration.

Action:

1. Identify missing engine: goal, conflict, cost, opponent, secret, transition, or payoff.
2. Provide three rescue directions:
   - intensify existing conflict;
   - reveal hidden information;
   - force a new decision under time pressure.
3. Convert chosen direction to a task.

### Setting Conflict

Trigger: new draft violates worldbuilding, power rules, timeline, character motivation, or previous chapter facts.

Action:

1. Prefer higher-level memory: constitution/world rules > PRD/outline > plot/timeline > task state > draft.
2. Patch the lower-priority source.
3. If the change affects ending, long arc, power ceiling, or relationship boundary, update `docs/变更日志.md`.

### Pacing Imbalance

Trigger: three consecutive chapters have no concrete payoff or only setup.

Action:

1. Add a small climax, tactical win, reveal, relationship move, or upgrade.
2. Compress exposition.
3. Make the next task a payoff task before more setup.

### Negative Reader Feedback

Trigger: negative feedback ratio exceeds 30%, or repeated comments point at the same mismatch.

Action:

1. Classify as expectation mismatch, character dislike, pacing fatigue, payoff failure, or setting confusion.
2. Extract the reader promise being violated.
3. Adjust future task queue first.
4. Rewrite old chapters only when the initial promise itself is wrong.

## Reporting Standard

Use evidence. Do not output vague praise or vague criticism.

Good:

```text
- 节奏风险：第12-14章连续三章都在解释规则，只有第13章末尾有轻微信息反转；下一章应先兑现一次可见收益。
```

Bad:

```text
- 节奏有点慢，建议加强。
```
