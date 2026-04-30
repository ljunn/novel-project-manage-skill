#!/usr/bin/env python3
"""Project-management helper for long-form web-novel projects."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASKS_REL = Path(".novel-project/.taskmaster/tasks.json")
PRD_REL = Path(".novel-project/.taskmaster/docs/prd.txt")
TASK_LOG_REL = Path("task_log.md")


def story_units(text: str) -> int:
    """Count Chinese characters plus Latin/digit word groups."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", "", text)
    chinese = re.findall(r"[\u4e00-\u9fff]", text)
    latin = re.findall(r"[A-Za-z0-9_]+", text)
    return len(chinese) + len(latin)


def write_if_missing(path: Path, content: str, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8").strip() and not force:
        return False
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def prd_template(title: str, genre: str, target_words: int, update_frequency: str, audience: str) -> str:
    target_wan = max(1, round(target_words / 10000))
    return f"""# 《{title}》项目需求文档

## 一、基础信息
- 作品名称：{title}
- 作品类型：{genre}
- 目标字数：{target_wan}万字
- 更新频率：{update_frequency}
- 目标读者：{audience}

## 二、核心设定
### 世界观
[详细描述世界背景、力量体系、社会结构、资源分配、禁忌与代价]

### 主线脉络
1. 开篇：
2. 发展：
3. 高潮：
4. 结局：

### 人物设定
#### 主角
- 姓名：
- 性格：
- 成长线：
- 关键转变点：

#### 重要配角
- 姓名：
- 功能：
- 欲望：
- 与主角关系：

## 三、分卷规划
### 第一卷：XXXX（1-50章）
- 核心冲突：
- 关键情节：
- 字数目标：15万字

### 第二卷：XXXX（51-100章）
- 核心冲突：
- 关键情节：
- 字数目标：

## 四、写作要求
- 文风：
- 节奏：
- 敏感点规避：
- 平台适配：
"""


def markdown_template(title: str, heading: str, body: str) -> str:
    return f"# {heading}\n\n{body.format(title=title).rstrip()}\n"


def task_log_template(title: str, target_words: int) -> str:
    return f"""# 创作进度日志

## 当前状态
- 创作阶段：规划中
- 书名：{title}
- 目标总字数：{target_words}
- 最新章节：无
- 当前处理章节：无
- 当前卷：第一卷
- 当前阶段：阶段1
- 当前阶段目标：立住主线、主角处境与核心卖点
- 主角位置：
- 主角状态：
- 下一章目标：立住开篇钩子、主角困境与核心异常
- 累计完成章节：0
- 累计完成字数：0

## 最近三章摘要
- 暂无

## 活跃伏笔
| 伏笔名称 | 埋设章节 | 当前状态 | 关联章节 |
|----------|----------|----------|----------|

## 待处理
- [ ] 待回收伏笔
- [ ] 待出场角色
- [ ] 未解决矛盾
"""


def default_files(title: str, genre: str, target_words: int, update_frequency: str, audience: str) -> dict[Path, str]:
    return {
        PRD_REL: prd_template(title, genre, target_words, update_frequency, audience),
        TASK_LOG_REL: task_log_template(title, target_words),
        Path(".novel-project/.taskmaster/docs/worldbuilding/README.md"): "# Worldbuilding\n\nUse this folder for detailed world rules, power systems, maps, social structures, and research notes.\n",
        Path("docs/项目总纲.md"): markdown_template(
            title,
            f"《{title}》项目总纲",
            """## 基本信息
- 题材：
- 预计章节数：
- 目标字数：
- 核心冲突：

## 主线三步法
- 终点站：
- 起爆事件：
- 连锁反应：

## 终极锚点
- 全书结局：
- 终极阻碍：
- 胜利方式：
- 终局代价：
""",
        ),
        Path("docs/章节规划.md"): markdown_template(
            title,
            "章节规划",
            """## 章节规划

| 章节 | 标题 | 核心事件 | 章尾钩子 | 目标字数 | 状态 |
|------|------|----------|----------|----------|------|
| 第1章 |  |  |  | 3000-5000 | todo |
""",
        ),
        Path("docs/作者意图.md"): markdown_template(
            title,
            "作者意图",
            """## 长期目标
- 核心情绪承诺：
- 最不能偏掉的卖点：
- 不允许写崩的关系/人物：
""",
        ),
        Path("docs/当前焦点.md"): markdown_template(
            title,
            "当前焦点",
            """## 最近 1-3 章优先事项
-

## 最近 1-3 章禁止偏航项
-
""",
        ),
        Path("docs/全书宪法.md"): markdown_template(
            title,
            "全书宪法",
            """## 不可违背项
- 主角底层行动逻辑：
- 世界底层规则：
- 长线关系边界：
- 终局方向：
""",
        ),
        Path("docs/卷纲.md"): markdown_template(
            title,
            "卷纲",
            """## 第一卷
- 章节范围：
- 核心冲突：
- 阶段高潮：
- 卷末状态变化：
""",
        ),
        Path("docs/阶段规划.md"): markdown_template(
            title,
            "阶段规划",
            """| 阶段 | 章节范围 | 当前问题 | 阶段目标 | 质量门禁 |
|------|----------|----------|----------|----------|
| 阶段1 | 1-10 |  | 立住主角、困境、卖点 | 黄金三章检查 |
""",
        ),
        Path("docs/变更日志.md"): markdown_template(
            title,
            "变更日志",
            """| 日期 | 变更 | 影响范围 | 后续动作 |
|------|------|----------|----------|
""",
        ),
        Path("plot/伏笔记录.md"): markdown_template(
            title,
            "伏笔记录",
            """## 活跃伏笔
| 伏笔名称 | 埋设章节 | 当前状态 | 关联章节 |
|----------|----------|----------|----------|

## 已回收伏笔
| 伏笔名称 | 埋设章节 | 回收章节 | 备注 |
|----------|----------|----------|------|
""",
        ),
        Path("plot/时间线.md"): markdown_template(
            title,
            "剧情时间线",
            """## 第一卷
-
""",
        ),
        Path("characters/README.md"): "# Character Files\n\nCreate one markdown file per major character.\n",
        Path("research/README.md"): "# Research\n\nStore market, genre, historical, cultural, and domain research here.\n",
    }


def default_tasks(project: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    tasks = [
        {
            "id": "SET-001",
            "phase": "设定完善",
            "title": "世界观细化",
            "priority": "high",
            "duration_days": 3,
            "status": "todo",
            "depends_on": [],
            "deliverables": ["地理/势力/资源设定", "力量或规则体系", "社会结构与禁忌"],
            "quality_gate": "世界规则能生成冲突，且主角行动会触发代价",
        },
        {
            "id": "SET-002",
            "phase": "设定完善",
            "title": "人物档案建立",
            "priority": "high",
            "duration_days": 4,
            "status": "todo",
            "depends_on": ["SET-001"],
            "deliverables": ["主角档案", "重要配角档案", "关系图谱"],
            "quality_gate": "主要人物都有欲望、缺口、行动逻辑和关系张力",
        },
        {
            "id": "OUT-001",
            "phase": "大纲构建",
            "title": "整体故事线梳理",
            "priority": "high",
            "duration_days": 2,
            "status": "todo",
            "depends_on": ["SET-001", "SET-002"],
            "deliverables": ["主线三步法", "关键转折点", "终极锚点"],
            "quality_gate": "终点站、起爆事件、连锁反应能互相咬合",
        },
        {
            "id": "OUT-002",
            "phase": "大纲构建",
            "title": "分卷大纲",
            "priority": "high",
            "duration_days": 2,
            "status": "todo",
            "depends_on": ["OUT-001"],
            "deliverables": ["卷名与核心冲突", "卷高潮", "章节范围"],
            "quality_gate": "每卷都有阶段问题、阶段回报和下一卷入口",
        },
        {
            "id": "OUT-003",
            "phase": "大纲构建",
            "title": "章节列表与情绪曲线",
            "priority": "high",
            "duration_days": 2,
            "status": "todo",
            "depends_on": ["OUT-002"],
            "deliverables": ["章节标题/概要", "章尾钩子", "情绪曲线"],
            "quality_gate": "前10章至少能看出卖点、冲突升级和第一个小高潮",
        },
        {
            "id": "CH-001",
            "phase": "章节写作",
            "title": "黄金三章写作",
            "priority": "high",
            "duration_days": 2,
            "status": "todo",
            "depends_on": ["OUT-003"],
            "deliverables": ["第1-3章正文", "开篇吸引力自查"],
            "quality_gate": "前三章展示题材承诺、主角困境、核心卖点和追读钩子",
        },
        {
            "id": "CH-002",
            "phase": "章节写作",
            "title": "第4-10章写作",
            "priority": "medium",
            "duration_days": 4,
            "status": "todo",
            "depends_on": ["CH-001"],
            "deliverables": ["第4-10章正文", "第一个小高潮"],
            "quality_gate": "完成第一个阶段回报，不连续铺垫超过三章",
        },
        {
            "id": "QC-001",
            "phase": "质量管控",
            "title": "前10章一致性与节奏检查",
            "priority": "high",
            "duration_days": 1,
            "status": "todo",
            "depends_on": ["CH-002"],
            "deliverables": ["质检报告", "返修任务"],
            "quality_gate": "设定、人物、节奏、爽点、章尾钩子都有证据化结论",
        },
        {
            "id": "QC-002",
            "phase": "质量管控",
            "title": "读者反馈分析",
            "priority": "medium",
            "duration_days": 1,
            "status": "todo",
            "depends_on": ["CH-002"],
            "deliverables": ["评论关键词", "期待/不满分类", "后续调整任务"],
            "quality_gate": "区分期待错配和执行问题，优先调整未来任务",
        },
    ]
    return {"project": project, "version": 1, "generated_at": now, "tasks": tasks}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_tasks(project_dir: Path, data: dict[str, Any], overwrite: bool = False) -> bool:
    path = project_dir / TASKS_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return False
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def write_tasks(project_dir: Path, data: dict[str, Any]) -> None:
    path = project_dir / TASKS_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_title_from_prd(prd: str, fallback: str) -> str:
    match = re.search(r"作品名称：\s*(.+)", prd)
    if match and match.group(1).strip():
        return match.group(1).strip()
    heading = re.search(r"#\s*《(.+?)》", prd)
    if heading:
        return heading.group(1).strip()
    return fallback


def chapter_paths(project_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for dirname in ("manuscript", "chapters"):
        directory = project_dir / dirname
        if directory.exists():
            paths.extend(path for path in sorted(directory.glob("*.md")) if is_chapter_file(path))
    return sorted(set(paths))


def is_chapter_file(path: Path) -> bool:
    name = path.name.lower()
    if name in {"readme.md", "index.md"}:
        return False
    return not path.name.startswith(".")


def manuscript_stats(project_dir: Path) -> dict[str, Any]:
    files = chapter_paths(project_dir)
    total = 0
    latest = None
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        total += story_units(text)
        latest = path
    return {
        "chapter_count": len(files),
        "word_count": total,
        "latest_chapter": str(latest.relative_to(project_dir)) if latest else None,
    }


def task_counts(tasks: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"todo": 0, "doing": 0, "blocked": 0, "done": 0, "other": 0}
    for task in tasks:
        status = str(task.get("status", "todo"))
        counts[status if status in counts else "other"] += 1
    return counts


def dependency_done(task: dict[str, Any], tasks_by_id: dict[str, dict[str, Any]]) -> bool:
    for dep_id in task.get("depends_on", []):
        dep = tasks_by_id.get(dep_id)
        if not dep or dep.get("status") != "done":
            return False
    return True


def choose_next_task(tasks: list[dict[str, Any]]) -> dict[str, Any] | None:
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks_by_id = {task.get("id"): task for task in tasks}
    candidates = [
        task
        for task in tasks
        if task.get("status", "todo") in {"todo", "doing", "blocked"}
        and dependency_done(task, tasks_by_id)
    ]
    if not candidates:
        return None
    candidates.sort(
        key=lambda task: (
            0 if task.get("status") == "blocked" else 1,
            priority_order.get(str(task.get("priority", "medium")), 3),
            str(task.get("id", "")),
        )
    )
    return candidates[0]


def project_warnings(project_dir: Path, data: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if not (project_dir / PRD_REL).exists():
        warnings.append("missing_prd")
    if not (project_dir / TASKS_REL).exists():
        warnings.append("missing_tasks")
    for rel in ["docs/项目总纲.md", "docs/章节规划.md", "plot/伏笔记录.md", "plot/时间线.md"]:
        if not (project_dir / rel).exists():
            warnings.append(f"missing:{rel}")
    if not (project_dir / TASK_LOG_REL).exists():
        warnings.append(f"missing:{TASK_LOG_REL}")
    stats = manuscript_stats(project_dir)
    tasks = data.get("tasks", []) if data else []
    if stats["chapter_count"] >= 20:
        for rel in ["docs/全书宪法.md", "docs/卷纲.md", "docs/阶段规划.md", "docs/变更日志.md"]:
            if not (project_dir / rel).exists():
                warnings.append(f"longform_missing:{rel}")
    if any(task.get("status") == "blocked" for task in tasks):
        warnings.append("blocked_tasks_present")
    return warnings


def cmd_init(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    project_dir.mkdir(parents=True, exist_ok=True)
    for directory in ["manuscript", "characters", "plot", "research", "docs"]:
        (project_dir / directory).mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    for rel, content in default_files(args.title, args.genre, args.target_words, args.update_frequency, args.audience).items():
        wrote = write_if_missing(project_dir / rel, content, force=args.force)
        (created if wrote else skipped).append(str(rel))

    data = default_tasks(args.title)
    tasks_written = save_tasks(project_dir, data, overwrite=args.force or not (project_dir / TASKS_REL).exists())
    if tasks_written:
        created.append(str(TASKS_REL))
    else:
        skipped.append(str(TASKS_REL))

    print(json.dumps({"project_dir": str(project_dir), "created": created, "skipped": skipped}, ensure_ascii=False, indent=2))
    return 0


def cmd_tasks(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    prd_path = project_dir / PRD_REL
    prd = prd_path.read_text(encoding="utf-8") if prd_path.exists() else ""
    project = extract_title_from_prd(prd, project_dir.name)
    written = save_tasks(project_dir, default_tasks(project), overwrite=args.overwrite)
    if not written:
        print(f"tasks.json already exists: {project_dir / TASKS_REL}", file=sys.stderr)
        print("Use --overwrite to regenerate it.", file=sys.stderr)
        return 1
    print(f"generated: {project_dir / TASKS_REL}")
    return 0


def build_status(project_dir: Path) -> dict[str, Any]:
    data = load_json(project_dir / TASKS_REL)
    tasks = data.get("tasks", []) if data else []
    next_task = choose_next_task(tasks)
    return {
        "project_dir": str(project_dir),
        "project": data.get("project", project_dir.name) if data else project_dir.name,
        "manuscript": manuscript_stats(project_dir),
        "tasks": {
            "total": len(tasks),
            "counts": task_counts(tasks),
            "next": next_task,
        },
        "warnings": project_warnings(project_dir, data),
    }


def print_status_text(status: dict[str, Any]) -> None:
    manuscript = status["manuscript"]
    counts = status["tasks"]["counts"]
    print(f"Project: {status['project']}")
    print(f"Chapters: {manuscript['chapter_count']} | Words: {manuscript['word_count']}")
    print(f"Latest: {manuscript['latest_chapter'] or 'none'}")
    print(
        "Tasks: "
        f"todo={counts['todo']} doing={counts['doing']} blocked={counts['blocked']} done={counts['done']}"
    )
    next_task = status["tasks"].get("next")
    if next_task:
        print(f"Next: [{next_task.get('priority')}] {next_task.get('id')} {next_task.get('title')}")
        print(f"Gate: {next_task.get('quality_gate')}")
    else:
        print("Next: none")
    if status["warnings"]:
        print("Warnings:")
        for warning in status["warnings"]:
            print(f"- {warning}")


def cmd_status(args: argparse.Namespace) -> int:
    status = build_status(Path(args.project_dir).resolve())
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print_status_text(status)
    return 0


def cmd_next_task(args: argparse.Namespace) -> int:
    status = build_status(Path(args.project_dir).resolve())
    task = status["tasks"].get("next")
    if not task:
        print("No ready task found.")
        return 1
    if args.json:
        print(json.dumps(task, ensure_ascii=False, indent=2))
    else:
        print(f"{task.get('id')} [{task.get('priority')}] {task.get('title')}")
        print(f"Phase: {task.get('phase')}")
        print(f"Deliverables: {', '.join(task.get('deliverables', []))}")
        print(f"Quality gate: {task.get('quality_gate')}")
    return 0


def safe_title(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", title).strip()
    cleaned = re.sub(r"\s+", "-", cleaned)
    return cleaned or "未命名"


def chapter_label(chapter_num: int) -> str:
    return f"第{chapter_num}章"


def chapter_filename(chapter_num: int, title: str) -> str:
    return f"第{chapter_num:04d}章-{safe_title(title)}.md"


def replace_or_append_field(text: str, label: str, value: str) -> str:
    pattern = rf"(?m)^- {re.escape(label)}.*$"
    replacement = f"- {label}{value}"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)
    if "## 当前状态\n" in text:
        return text.replace("## 当前状态\n", f"## 当前状态\n{replacement}\n", 1)
    return text.rstrip() + f"\n\n## 当前状态\n{replacement}\n"


def replace_section(text: str, header: str, lines: list[str]) -> str:
    body = "\n".join(lines).rstrip() + "\n"
    pattern = rf"(?ms)(^## {re.escape(header)}\n)(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    if match:
        return text[: match.start(2)] + body + text[match.end(2) :]
    return text.rstrip() + f"\n\n## {header}\n{body}"


def update_recent_summaries(text: str, label: str, summary: str) -> str:
    if not summary:
        return text
    pattern = r"(?ms)^## 最近三章摘要\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    old_lines: list[str] = []
    if match:
        old_lines = [
            line
            for line in match.group(1).splitlines()
            if line.strip() and line.strip() != "- 暂无" and not line.startswith(f"- {label}：")
        ]
    return replace_section(text, "最近三章摘要", [f"- {label}：{summary}"] + old_lines[:2])


def update_task_log(project_dir: Path, chapter_num: int, title: str, word_count: int, summary: str) -> None:
    path = project_dir / TASK_LOG_REL
    if not path.exists():
        path.write_text(task_log_template(project_dir.name, word_count), encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    label = f"{chapter_label(chapter_num)}：{title}"
    text = replace_or_append_field(text, "创作阶段：", "连载中")
    text = replace_or_append_field(text, "最新章节：", label)
    text = replace_or_append_field(text, "当前处理章节：", "无")
    text = replace_or_append_field(text, "累计完成章节：", str(max(chapter_num, manuscript_stats(project_dir)["chapter_count"])))
    text = replace_or_append_field(text, "累计完成字数：", str(manuscript_stats(project_dir)["word_count"]))
    text = update_recent_summaries(text, chapter_label(chapter_num), summary)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_chapter_plan(project_dir: Path, chapter_num: int, title: str, status: str, word_count: int | None = None) -> None:
    path = project_dir / "docs/章节规划.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            "# 章节规划\n\n## 章节规划\n\n| 章节 | 标题 | 核心事件 | 章尾钩子 | 目标字数 | 状态 |\n|------|------|----------|----------|----------|------|\n",
            encoding="utf-8",
        )
    text = path.read_text(encoding="utf-8")
    row_pattern = rf"(?m)^\|\s*第{chapter_num}章\s*\|.*$"
    display_words = str(word_count) if word_count is not None else "3000-5000"
    new_row = f"| 第{chapter_num}章 | {title} |  |  | {display_words} | {status} |"
    if re.search(row_pattern, text):
        text = re.sub(row_pattern, new_row, text, count=1)
    else:
        text = text.rstrip() + "\n" + new_row + "\n"
    path.write_text(text, encoding="utf-8")


def update_task_queue_for_chapter(project_dir: Path, chapter_num: int) -> None:
    path = project_dir / TASKS_REL
    data = load_json(path)
    if not data:
        return
    for task in data.get("tasks", []):
        task_id = task.get("id")
        if task_id == "CH-001" and chapter_num < 3 and task.get("status") != "done":
            task["status"] = "doing"
        elif task_id == "CH-001" and chapter_num >= 3:
            task["status"] = "done"
        elif task_id == "CH-002" and 4 <= chapter_num < 10 and task.get("status") != "done":
            task["status"] = "doing"
        elif task_id == "CH-002" and chapter_num >= 10:
            task["status"] = "done"
    write_tasks(project_dir, data)


def strip_markdown_noise(text: str) -> str:
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    return text.strip()


def check_manuscript_purity(text: str) -> list[str]:
    violations: list[str] = []
    stripped = strip_markdown_noise(text)
    if re.search(r"(?m)^\s{0,3}#{1,6}\s*", stripped):
        violations.append("contains_markdown_heading")
    forbidden_patterns = {
        "contains_author_note": r"作者说|本章说",
        "contains_body_heading": r"##\s*正文|#\s*正文",
        "contains_summary_heading": r"本章概要|章节备注|写作目标|质量检查|场景拆分",
        "contains_chapter_title_heading": r"(?m)^\s{0,3}#{1,6}\s*第\s*\d+\s*章",
    }
    for name, pattern in forbidden_patterns.items():
        if re.search(pattern, stripped):
            violations.append(name)
    return sorted(set(violations))


def check_chapter_file(path: Path, min_words: int) -> dict[str, Any]:
    if not path.exists():
        return {"file": str(path), "exists": False, "word_count": 0, "violations": ["missing_file"], "ok": False}
    text = path.read_text(encoding="utf-8", errors="ignore")
    word_count = story_units(text)
    violations = check_manuscript_purity(text)
    if word_count < min_words:
        violations.append(f"below_min_words:{min_words}")
    return {
        "file": str(path),
        "exists": True,
        "word_count": word_count,
        "violations": violations,
        "ok": not violations,
    }


def cmd_start_chapter(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    title = args.title or "未命名"
    target_path = project_dir / ".novel-project/runtime" / f"chapter-{args.chapter_num:04d}.target.md"
    manuscript_path = project_dir / "manuscript" / chapter_filename(args.chapter_num, title)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)
    target = f"""# {chapter_label(args.chapter_num)} 写作目标

- 标题：{title}
- 核心事件：
- 开场状态 A：
- 章末状态 B：
- 本章必须兑现：
- 本章必须埋/推进：
- 章尾钩子：
- 禁止偏航：

## 开写前必读
- .novel-project/.taskmaster/docs/prd.txt
- task_log.md
- docs/项目总纲.md
- docs/章节规划.md
- plot/伏笔记录.md
- plot/时间线.md
- characters/*.md（相关人物）
- 上一章正文

## 正文输出
- 写入：{manuscript_path.relative_to(project_dir)}
- 只写纯正文；标题、概要、作者说和质检报告不得进入 manuscript 文件。
"""
    target_path.write_text(target.rstrip() + "\n", encoding="utf-8")
    update_chapter_plan(project_dir, args.chapter_num, title, "doing")
    print(json.dumps({
        "target_path": str(target_path),
        "manuscript_path": str(manuscript_path),
        "pure_prose_required": True,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_check_chapter(args: argparse.Namespace) -> int:
    result = check_chapter_file(Path(args.chapter_file).resolve(), args.min_words)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"File: {result['file']}")
        print(f"Words: {result['word_count']}")
        if result["ok"]:
            print("OK: pure manuscript format and minimum length passed.")
        else:
            print("Issues:")
            for item in result["violations"]:
                print(f"- {item}")
    return 0 if result["ok"] else 1


def cmd_finish_chapter(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    chapter_file = Path(args.chapter_file).resolve()
    result = check_chapter_file(chapter_file, args.min_words)
    if not result["ok"] and not args.allow_issues:
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        print("Refusing to finish chapter while manuscript checks fail. Use --allow-issues to override.", file=sys.stderr)
        return 1
    title = args.title or "未命名"
    word_count = int(result["word_count"])
    update_chapter_plan(project_dir, args.chapter_num, title, "done", word_count)
    update_task_log(project_dir, args.chapter_num, title, word_count, args.summary or "")
    update_task_queue_for_chapter(project_dir, args.chapter_num)
    print(json.dumps({
        "chapter": args.chapter_num,
        "title": title,
        "word_count": word_count,
        "updated": ["docs/章节规划.md", "task_log.md", str(TASKS_REL)],
        "check": result,
    }, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage long-form web-novel project structure and tasks.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize a managed novel project.")
    init.add_argument("project_dir")
    init.add_argument("--title", required=True)
    init.add_argument("--genre", default="待定")
    init.add_argument("--target-words", type=int, default=3_000_000)
    init.add_argument("--update-frequency", default="每日更新")
    init.add_argument("--audience", default="平台读者")
    init.add_argument("--force", action="store_true", help="Overwrite populated template files.")
    init.set_defaults(func=cmd_init)

    tasks = sub.add_parser("tasks", help="Generate tasks.json from the PRD/template.")
    tasks.add_argument("project_dir")
    tasks.add_argument("--overwrite", action="store_true")
    tasks.set_defaults(func=cmd_tasks)

    status = sub.add_parser("status", help="Show project status.")
    status.add_argument("project_dir")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)

    next_task = sub.add_parser("next-task", help="Show the next ready task.")
    next_task.add_argument("project_dir")
    next_task.add_argument("--json", action="store_true")
    next_task.set_defaults(func=cmd_next_task)

    start = sub.add_parser("start-chapter", help="Create a chapter target and mark the chapter as in progress.")
    start.add_argument("project_dir")
    start.add_argument("chapter_num", type=int)
    start.add_argument("--title", default="未命名")
    start.set_defaults(func=cmd_start_chapter)

    check = sub.add_parser("check-chapter", help="Check manuscript word count and pure-prose formatting.")
    check.add_argument("chapter_file")
    check.add_argument("--min-words", type=int, default=3000)
    check.add_argument("--json", action="store_true")
    check.set_defaults(func=cmd_check_chapter)

    finish = sub.add_parser("finish-chapter", help="Finish a chapter and update progress records.")
    finish.add_argument("project_dir")
    finish.add_argument("chapter_num", type=int)
    finish.add_argument("chapter_file")
    finish.add_argument("--title", default="未命名")
    finish.add_argument("--summary", default="")
    finish.add_argument("--min-words", type=int, default=3000)
    finish.add_argument("--allow-issues", action="store_true")
    finish.set_defaults(func=cmd_finish_chapter)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
