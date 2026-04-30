---
name: novel-project-manager
description: Novel writing project-management skill for long-form web novels. Use when Codex needs to initialize a novel project, turn a PRD or story idea into structured tasks, manage manuscript/character/plot/research folders, choose today's writing task, monitor progress, handle stuck writing/setting conflicts/pacing issues/reader feedback, or run quality gates before continuing serial web-novel writing.
---

# Novel Project Manager

Use this skill to run a web-novel project like a managed serial product: PRD first, task breakdown second, chapter execution third, quality gates and exception handling before declaring progress.

This skill combines the source design's `.novel-project` task-management model with the full `junli-ai-novel` deep chapter pipeline: read project memory before writing, run preflight/resume/plan/compose/start before drafting, check/review/finish after drafting, and optimize for serial retention rather than literary abstraction by default.

## First Decision

Classify the user request before doing work:

- **New project / rough idea**: create or complete PRD, initialize structure, generate tasks.
- **Daily dispatch**: inspect progress and choose the next highest-value task.
- **Chapter execution**: recover memory, plan chapter target, then write or revise.
- **Quality control**: check structure, consistency, hooks, pacing, reader compensation, and word count.
- **Exception recovery**: resolve stuck writing, setting conflicts, pacing imbalance, or negative feedback before continuing.

When the task needs details, read only the relevant reference:

- Project structure, PRD, and task schema: `references/project-model.md`
- Workflows for init, dispatch, chapter cycle, and long-form governance: `references/workflows.md`
- Quality gates, complexity scoring, tool map, and exception handling: `references/quality-and-exceptions.md`
- Writing technique selection before drafting or revision: `references/technique-stack.md`
- Deep writing methods and hubs: start from `references/wiki.md`, then open only the relevant hub under `references/hubs/`.

## Core Rules

1. Treat the PRD as the project contract. Do not start large-scale drafting from a loose idea unless the missing PRD fields are either filled or explicitly marked unknown.
2. Use the `.novel-project/.taskmaster/tasks.json` task list as the execution queue. If it is absent, generate it from the PRD before dispatching daily work.
3. Separate project management from manuscript text. Put management state under `.novel-project/`, pure chapter prose under `manuscript/`, characters under `characters/`, plot records under `plot/`, and research under `research/`. Treat `chapters/` only as an import/legacy alias.
4. Before writing or revising a chapter, read the PRD, task list, current progress, chapter plan, active foreshadowing, relevant character files, and the previous chapter when available.
5. For platform web novels, prioritize stable serialization, follow-up pull, payoff delivery, visible conflict, and long-line consistency.
6. Never claim a semantic check was automated unless it actually was. Scripts in this skill provide structure/progress checks; consistency, hooks, pacing, and prose quality still require reading evidence.
7. When producing chapter files, follow `junli-ai-novel` output discipline: the manuscript file contains only story prose. Put chapter title, summary, foreshadowing notes, and author notes into project records or a separate publishing note, not inside the manuscript file.

## Script Entry

Use two bundled CLIs:

- `scripts/novel_pm.py`: PRD/task/project-management layer from the source design.
- `scripts/chapter_pipeline.py`: deep `junli-ai-novel` writing, governance, review, and finish layer.

For project/task management:

```bash
python3 scripts/novel_pm.py init <project_dir> --title "小说标题"
python3 scripts/novel_pm.py tasks <project_dir>
python3 scripts/novel_pm.py status <project_dir>
python3 scripts/novel_pm.py next-task <project_dir>
```

For chapter writing and review, prefer the deep pipeline:

```bash
python3 scripts/chapter_pipeline.py preflight <project_dir>
python3 scripts/chapter_pipeline.py resume <project_dir>
python3 scripts/chapter_pipeline.py plan <project_dir> --chapter-num <chapter_num> --chapter-title "标题"
python3 scripts/chapter_pipeline.py compose <project_dir> --chapter-num <chapter_num> --chapter-title "标题"
python3 scripts/chapter_pipeline.py start <project_dir> <chapter_num> --chapter-title "标题"
python3 scripts/chapter_pipeline.py check <chapter_file>
python3 scripts/chapter_pipeline.py finish <project_dir> <chapter_num> <chapter_file> --chapter-title "标题" --summary "摘要"
```

Shortcut:

```bash
python3 scripts/chapter_pipeline.py next-chapter <project_dir> --chapter-title "标题"
python3 scripts/chapter_pipeline.py next-chapter <project_dir> --chapter-num <chapter_num> --chapter-path <chapter_file> --summary "摘要"
```

Lightweight fallback, only when the deep pipeline is not appropriate:

```bash
python3 scripts/novel_pm.py start-chapter <project_dir> <chapter_num> --title "标题"
python3 scripts/novel_pm.py check-chapter <chapter_file>
python3 scripts/novel_pm.py finish-chapter <project_dir> <chapter_num> <chapter_file> --title "标题" --summary "摘要"
```

Useful options:

- `init --force`: create missing files even in an existing folder without overwriting populated files.
- `tasks --overwrite`: regenerate the task queue from the PRD/template.
- `status --json`: emit machine-readable progress and warnings.

## Operating Flow

For a new project:

1. Ask only for missing essentials: title, genre, core protagonist, core conflict, target length/update rhythm, and reader target.
2. Create the PRD/task structure with `novel_pm.py init`.
3. Fill or update `.novel-project/.taskmaster/docs/prd.txt`.
4. Generate tasks with `novel_pm.py tasks`.
5. Ensure deep-pipeline memory files exist. If needed, run `chapter_pipeline.py bootstrap-longform <project_dir>`.
6. Report the next task and the first quality gate.

For daily writing:

1. Run `status` and `next-task`.
2. Read the files that constrain the task.
3. If drafting a chapter, run the deep chain: `preflight -> resume -> plan -> compose -> start`.
4. During `compose`, read the auto-generated `Recommended Technique Stack` in `runtime/chapter-XXXX.intent.md`; override it only when the task clearly needs a different technique.
5. Write pure prose into `manuscript/`, starting from the first sentence of the story.
6. After drafting, run `check -> lint/dialogue-pass/consistency/review as needed -> finish`.

For exceptions:

- Stuck for more than two days: produce three viable plot rescue directions, then convert the chosen direction into a task.
- Setting conflict: stop drafting, reconcile the rule in PRD/worldbuilding/plot records, then continue.
- Three weak chapters in a row: add a small-climax/payoff task before the next ordinary chapter.
- Negative reader feedback: separate expectation mismatch from execution problem, then update future tasks rather than panic-rewriting the whole book.

## Output Standards

When creating artifacts, use the templates in `references/project-model.md`.

Manuscript chapter files must be pure story text:

```markdown
[从第一句故事正文直接开始]
```

Name chapter files with a recognizable chapter pattern so the deep review tools can identify them, for example `第0001章_雨夜来客.md` or `0001_雨夜来客.md`.

Do not put these inside `manuscript/` chapter files:

- `# 第X章` or `## 第X章`
- `## 正文`, `## 本章概要`, `## 章节备注`
- 作者说 / 本章说
- planning bullets, scene cards, quality reports, or summaries

Keep character cards in this shape:

```markdown
# 姓名

- 年龄：
- 外貌：
- 性格：
- 背景：
- 关键事件：
- 成长线：
- 关系网：
```

## Integration Note

This skill now bundles the full deep pipeline. Use `novel_pm.py` for PRD/task dispatch, and `chapter_pipeline.py` for actual long-form chapter execution, review, governance, marketing, and platform gates.

`chapter_pipeline.py check/review` may return warnings or a non-zero exit code when a chapter is short, flat, weakly hooked, or has missing context. Treat that as a quality gate requiring review; do not ignore it just because `finish` can still update progress.
