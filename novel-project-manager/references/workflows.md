# Workflows

Use this reference when executing a user request rather than merely explaining the skill.

## New Project

Goal: convert an idea into a managed serial project.

Steps:

1. Collect only the six essentials: title, genre, protagonist, core conflict, target length/update rhythm, target readers.
2. Run:

   ```bash
   python3 scripts/novel_pm.py init <project_dir> --title "标题"
   ```

3. Fill the PRD from the user's idea. Keep unknowns explicit.
4. Run:

   ```bash
   python3 scripts/novel_pm.py tasks <project_dir>
   python3 scripts/novel_pm.py next-task <project_dir>
   ```

5. Report: created files, missing PRD fields, next task, first quality gate.

Do not ask the user to fill a huge form if the idea is enough to start. Convert their idea into a draft PRD and mark weak spots.

## Daily Dispatch

Goal: answer "今天写什么" with the highest leverage task.

Steps:

1. Run `status`.
2. Run `next-task`.
3. Inspect the task's dependency files.
4. Choose one of:
   - continue prerequisite setup if a high-priority setup task is still open;
   - write the next planned chapter if setup is adequate;
   - repair a blocker if any task is blocked;
   - run a quality pass if the latest batch crossed a gate.
5. Output a short daily brief:
   - today's task;
   - why this task is next;
   - required input files;
   - expected deliverable;
   - quality gate.

## Chapter Cycle

Goal: write or revise a chapter without losing continuity.

Pre-read order:

1. `.novel-project/.taskmaster/docs/prd.txt`
2. `.novel-project/.taskmaster/tasks.json`
3. `task_log.md`
4. `docs/项目总纲.md`
5. `docs/章节规划.md`
6. `plot/伏笔记录.md`
7. `plot/时间线.md`
8. relevant `characters/*.md`
9. previous chapter in `manuscript/` or legacy `chapters/`

Run the bundled deep pipeline before drafting:

```bash
python3 scripts/chapter_pipeline.py preflight <项目目录>
python3 scripts/chapter_pipeline.py resume <项目目录>
python3 scripts/chapter_pipeline.py plan <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py compose <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py start <项目目录> <章节号> --chapter-title "标题"
```

Shortcut:

```bash
python3 scripts/chapter_pipeline.py next-chapter <项目目录> --chapter-title "标题"
```

Before prose, write a chapter target:

```text
- 核心事件：
- 开场状态 A：
- 章末状态 B：
- 本章必须兑现：
- 本章必须埋/推进：
- 章尾钩子：
- 禁止偏航：
```

`compose` automatically writes a `Recommended Technique Stack` into `runtime/chapter-XXXX.intent.md` and `runtime/chapter-XXXX.context.json`. Keep it in working notes or runtime files, never inside the manuscript. Default to `writing-quickref + chapter-workflow`, then add only the techniques needed for the current chapter problem.

Writing rules inherited from `junli-ai-novel`:

- One chapter should have one dominant event and at most two major threads.
- Every scene must move from state A to state B.
- Dialogue should push conflict or expose character; do not use it as a lore dump.
- Use close POV discipline; do not leak information the POV character cannot know.
- Convert abstract emotion into action, body response, decision, and consequence.
- End with unresolved pressure, not a summary.

After prose:

1. Count words.
2. Check hook, payoff, conflict, continuity, active foreshadowing, and reader compensation.
3. Update task status and progress records.
4. If a core setting or ending direction changed, update `docs/变更日志.md` before continuing.
5. Keep the manuscript file pure story prose. Put reports, summaries, and author notes outside the manuscript.

Use the deep finish path:

```bash
python3 scripts/chapter_pipeline.py check <章节文件路径>
python3 scripts/chapter_pipeline.py lint <章节文件路径>
python3 scripts/chapter_pipeline.py dialogue-pass <章节文件路径>
python3 scripts/chapter_pipeline.py consistency <章节文件路径> --project-path <项目目录>
python3 scripts/chapter_pipeline.py review <章节文件路径> --project-path <项目目录>
python3 scripts/chapter_pipeline.py finish <项目目录> <章节号> <章节文件路径> --chapter-title "标题" --summary "摘要"
```

Use the strict `junli-ai-novel` manuscript convention:

- write into `manuscript/`;
- start from the first story sentence;
- name files with a detectable chapter pattern such as `第0001章_标题.md` or `0001_标题.md`;
- no `# 第X章`, `## 正文`, metadata blocks, scene-card headings, author notes, or quality reports in the manuscript file;
- record the chapter title in filename and `docs/章节规划.md`.

## Quality Control

Run a quality pass at these gates:

- after the first 3 chapters;
- after the first 10 chapters;
- every 5-10 chapters during unstable planning;
- every volume ending;
- whenever reader feedback shows expectation mismatch.

Minimum report:

```text
## 检查结论
- 继续 / 先返修 / 先重构

## 证据
- 钩子：
- 回报：
- 冲突：
- 人物一致性：
- 设定一致性：
- 节奏：

## 下一步任务
- [priority] task
```

## Long-Form Governance

Treat a project as long-form governance when any condition is true:

- target length exceeds 1,000,000 Chinese characters/words;
- actual manuscript exceeds 300,000;
- chapter count exceeds 20;
- user asks for volumes, phases, audits, long-line control, or structural changes.

Required files:

- `docs/全书宪法.md`
- `docs/卷纲.md`
- `docs/阶段规划.md`
- `docs/变更日志.md`

If these are missing, create or complete them before pushing forward with major drafting.

## Exception Recovery

Stuck writing:

1. Identify whether the stuck point is missing goal, missing conflict, missing cost, missing information, or missing transition.
2. Offer three directions.
3. Convert the chosen direction into a concrete task.

Setting conflict:

1. Stop drafting.
2. Identify the higher-priority source: constitution/world rules > PRD/outline > task state > draft.
3. Patch the lower-priority source.
4. Record the change if it affects long-term plot.

Pacing imbalance:

1. Check whether three consecutive chapters lack payoff.
2. Add a small-climax task or compress setup.
3. Make the next chapter deliver a visible result.

Negative feedback:

1. Separate "wrong promise" from "weak execution".
2. Extract repeated reader expectations.
3. Update future tasks and only rewrite old chapters when the promise itself is broken.
