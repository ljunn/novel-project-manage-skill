# Novel Project Manage Skill

This repository contains the `novel-project-manager` Codex skill.

It combines:

- the Feishu wiki source idea for PRD, tasks, progress, and project governance
- the `junli-ai-novel` deep chapter pipeline
- writing technique selection, quality gates, manuscript purity rules, and long-form web-novel workflow conventions

## Contents

- `novel-project-manager/SKILL.md`: skill entry and operating rules
- `novel-project-manager/scripts/novel_pm.py`: PRD, task, status, and dispatch tooling
- `novel-project-manager/scripts/chapter_pipeline.py`: deep chapter planning, writing, review, and finish pipeline
- `novel-project-manager/references/`: project model, workflows, writing techniques, quality rules, and deep-pipeline references
- `novel-project-manager/rules/novel-lint/`: prose lint rules inherited from the deep pipeline
- `wiki-source.md`: source design exported from Feishu

## Validation

```bash
python3 -m py_compile novel-project-manager/scripts/*.py
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py novel-project-manager
```

## Basic Usage

```bash
python3 novel-project-manager/scripts/novel_pm.py init <project_dir> --title "Title"
python3 novel-project-manager/scripts/novel_pm.py tasks <project_dir>
python3 novel-project-manager/scripts/chapter_pipeline.py preflight <project_dir>
python3 novel-project-manager/scripts/chapter_pipeline.py compose <project_dir> --chapter-num 1 --chapter-title "Opening"
```
