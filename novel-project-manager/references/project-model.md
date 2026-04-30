# Project Model

This reference defines the managed novel project shape. Use it when creating a project, filling a PRD, generating tasks, or explaining where artifacts should live.

## Directory Structure

Default structure:

```text
[project]/
├── .novel-project/
│   └── .taskmaster/
│       ├── docs/
│       │   ├── prd.txt
│       │   └── worldbuilding/
│       └── tasks.json
├── task_log.md
├── docs/
│   ├── 项目总纲.md
│   ├── 章节规划.md
│   ├── 作者意图.md
│   ├── 当前焦点.md
│   ├── 全书宪法.md
│   ├── 卷纲.md
│   ├── 阶段规划.md
│   └── 变更日志.md
├── manuscript/
├── characters/
├── plot/
│   ├── 伏笔记录.md
│   └── 时间线.md
└── research/
```

Compatibility:

- `manuscript/` is the default chapter prose folder.
- If imported material uses the source design's `chapters/`, treat it as a legacy alias for reading/status. New chapter output should still go to `manuscript/`.
- `.novel-project/` is operational state; do not place prose there.

## PRD Template

Create `.novel-project/.taskmaster/docs/prd.txt` with these sections:

```text
# 《小说标题》项目需求文档

## 一、基础信息
- 作品名称：
- 作品类型：[仙侠/玄幻/都市/科幻/言情/悬疑等]
- 目标字数：XXX万字
- 更新频率：每日/每周X更
- 目标读者：

## 二、核心设定
### 世界观
[世界背景、力量体系、社会结构、资源分配、禁忌与代价]

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
```

## Task Schema

`tasks.json` should be boring and explicit. Use this schema:

```json
{
  "project": "小说标题",
  "version": 1,
  "tasks": [
    {
      "id": "SET-001",
      "phase": "设定完善",
      "title": "世界观细化",
      "priority": "high",
      "duration_days": 3,
      "status": "todo",
      "depends_on": [],
      "deliverables": ["地理设定", "力量体系规则", "社会结构文档"],
      "quality_gate": "世界规则能生成冲突，且主角行动会触发代价"
    }
  ]
}
```

Statuses: `todo`, `doing`, `blocked`, `done`.

Priorities: `high`, `medium`, `low`.

## Default Task Breakdown

Generate tasks in four phases:

- **设定完善**: worldbuilding, power/rule system, character files, relationship map.
- **大纲构建**: main plot, key turns, volume outlines, chapter list, emotion curve.
- **章节写作**: golden opening, first ten chapters, first climax, stable update batches.
- **质量管控**: volume self-check, consistency pass, pacing pass, reader feedback analysis.

Critical path:

```text
世界观设定 -> 人物设定 -> 主线设计 -> 分卷规划 -> 黄金三章 -> 第一个高潮 -> 中期转折 -> 结局
```

## Progress Dashboard

Use this compact report shape:

```text
## 项目进度
- 已进行：X天
- 已完成：X字 / 总目标Y字
- 写作速度：平均每天Z字
- 章节完成率：XX%
- 爽点密度：X个/章（人工评估）
- 更新稳定性：XX%

## 待处理任务
- [高优先级] 第45章高潮场景优化
- [中优先级] 配角感情线发展
- [低优先级] 次要副本设计
```

Do not invent metrics. If a value is not measured, label it `未评估`.

## Artifact Templates

Manuscript chapter:

```markdown
[从第一句故事正文直接开始，不加标题、不加备注、不加作者说]
```

Use filenames such as `第0001章_标题.md` or `0001_标题.md`; chapter titles, summaries, foreshadowing notes, and publishing notes belong in `task_log.md`, `docs/章节规划.md`, `plot/伏笔记录.md`, or a separate publishing package, not in the manuscript file.

Character card:

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
