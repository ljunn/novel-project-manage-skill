---
name: novel-project-manager
description: 长篇网文小说项目管理技能。用于初始化小说项目，把需求文档或故事点子转成结构化任务，管理正文、人物、情节、资料目录，选择今日写作任务，监控进度，处理卡文、设定冲突、节奏失衡、读者反馈，并在继续连载前执行质量门禁。
---

# 小说项目管理器

用这个技能把网文项目当成可管理的连载产品推进：先定需求文档，再拆任务，再执行章节，最后通过质量门禁和异常处理后才确认进度。

本技能融合源方案里的 `.novel-project` 任务管理模型，以及完整的 `junli-ai-novel` 深度章节流水线：写前先读项目记忆，起草前执行 `preflight/resume/plan/compose/start`，写后执行 `check/review/finish`，默认优先优化连载留存，而不是抽象文学表达。

## 先判断

动手前先判断用户请求属于哪一类：

- **新项目 / 粗略点子**：创建或补全需求文档，初始化目录结构，生成任务。
- **今日调度**：检查进度，选择下一项最有价值的任务。
- **章节执行**：恢复项目记忆，规划本章目标，然后写作或返修。
- **质量管控**：检查结构、连贯性、钩子、节奏、读者补偿和字数。
- **异常恢复**：先处理卡文、设定冲突、节奏失衡或负面反馈，再继续推进。

任务需要细节时，只读取相关参考文件：

- 项目结构、需求文档和任务字段：`references/project-model.md`
- 初始化、调度、章节循环和长篇治理流程：`references/workflows.md`
- 质量门禁、复杂度评分、检查项地图和异常处理：`references/quality-and-exceptions.md`
- 起草或返修前的写作技巧选择：`references/technique-stack.md`
- 深度写作方法与索引：先看 `references/wiki.md`，再只打开 `references/hubs/` 下相关索引页。

## 核心规则

1. 把需求文档视为项目契约。除非缺失字段已经补齐或明确标注“未知”，不要只凭松散点子开始大规模写正文。
2. 把 `.novel-project/.taskmaster/tasks.json` 作为执行队列。若文件缺失，先从需求文档生成任务，再做今日调度。
3. 项目管理信息和正文分离。管理状态放在 `.novel-project/`，纯章节正文放在 `manuscript/`，人物放在 `characters/`，情节记录放在 `plot/`，资料放在 `research/`。`chapters/` 只当作导入或旧项目别名。
4. 写作或返修章节前，先读取需求文档、任务列表、当前进度、章节规划、活跃伏笔、相关人物文件，以及可用的上一章。
5. 平台网文优先保证稳定连载、追读牵引、回报兑现、可见冲突和长线一致性。
6. 没有真正自动化完成的语义检查，不能声称已经自动检查。脚本只提供结构和进度类检查；一致性、钩子、节奏和文笔质量仍需要读证据。
7. 生成章节文件时遵守 `junli-ai-novel` 的输出纪律：正文文件只放故事正文。章节标题、摘要、伏笔备注、作者说明放入项目记录或单独发布说明，不写进正文文件。

## 脚本入口

使用两个内置命令行脚本：

- `scripts/novel_pm.py`：源方案里的需求文档、任务和项目管理层。
- `scripts/chapter_pipeline.py`：深度 `junli-ai-novel` 写作、治理、审阅和收尾层。

项目和任务管理：

```bash
python3 scripts/novel_pm.py init <项目目录> --title "小说标题"
python3 scripts/novel_pm.py tasks <项目目录>
python3 scripts/novel_pm.py status <项目目录>
python3 scripts/novel_pm.py next-task <项目目录>
```

章节写作和审阅优先使用深度流水线：

```bash
python3 scripts/chapter_pipeline.py preflight <项目目录>
python3 scripts/chapter_pipeline.py resume <项目目录>
python3 scripts/chapter_pipeline.py plan <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py compose <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py start <项目目录> <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py check <章节文件>
python3 scripts/chapter_pipeline.py finish <项目目录> <章节号> <章节文件> --chapter-title "标题" --summary "摘要"
```

快捷入口：

```bash
python3 scripts/chapter_pipeline.py next-chapter <项目目录> --chapter-title "标题"
python3 scripts/chapter_pipeline.py next-chapter <项目目录> --chapter-num <章节号> --chapter-path <章节文件> --summary "摘要"
```

轻量兜底：仅在不适合使用深度流水线时使用。

```bash
python3 scripts/novel_pm.py start-chapter <项目目录> <章节号> --title "标题"
python3 scripts/novel_pm.py check-chapter <章节文件>
python3 scripts/novel_pm.py finish-chapter <项目目录> <章节号> <章节文件> --title "标题" --summary "摘要"
```

常用选项：

- `init --force`：在已有目录里补齐缺失文件，不覆盖已有内容。
- `tasks --overwrite`：从需求文档或模板重新生成任务队列。
- `status --json`：输出可被程序读取的进度和警告。

## 操作流程

新项目：

1. 只追问必要缺口：书名、题材、核心主角、核心冲突、目标字数/更新节奏、目标读者。
2. 用 `novel_pm.py init` 创建需求文档和任务结构。
3. 填写或更新 `.novel-project/.taskmaster/docs/prd.txt`。
4. 用 `novel_pm.py tasks` 生成任务。
5. 确保深度流水线记忆文件存在；必要时运行 `chapter_pipeline.py bootstrap-longform <项目目录>`。
6. 汇报下一项任务和第一个质量门禁。

日常写作：

1. 运行 `status` 和 `next-task`。
2. 读取约束当前任务的文件。
3. 若要起草章节，依次执行深度链路：`preflight`、`resume`、`plan`、`compose`、`start`。
4. 执行 `compose` 后，读取 `runtime/chapter-XXXX.intent.md` 自动生成的“推荐技巧栈”；只有当前任务明显需要其他技巧时才覆盖。
5. 把纯正文写入 `manuscript/`，从故事第一句直接开始。
6. 起草后按需执行 `check`、`lint`、`dialogue-pass`、`consistency`、`review`、`finish`。

异常处理：

- 卡文超过两天：给出三个可执行的剧情救援方向，再把选定方向转成任务。
- 设定冲突：停止写正文，先在需求文档、世界观或情节记录中统一规则，再继续。
- 连续三章偏弱：在下一章普通推进前，先增加一个小高潮或回报任务。
- 负面读者反馈：区分预期错位和执行问题，优先更新后续任务，不要恐慌式重写全书。

## 输出标准

创建产物时，使用 `references/project-model.md` 里的模板。

章节正文文件必须是纯故事正文：

```markdown
[从第一句故事正文直接开始]
```

章节文件名要包含可识别的章节格式，便于深度审阅工具识别，例如 `第0001章_雨夜来客.md` 或 `0001_雨夜来客.md`。

不要把以下内容写进 `manuscript/` 章节文件：

- `# 第X章` 或 `## 第X章`
- `## 正文`, `## 本章概要`, `## 章节备注`
- 作者说 / 本章说
- 规划条目、场景卡、质量报告或摘要

人物卡保持这个格式：

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

## 集成说明

本技能已经内置完整深度流水线。用 `novel_pm.py` 做需求文档和任务调度，用 `chapter_pipeline.py` 做长篇章节执行、审阅、治理、营销和平台门禁。

当章节过短、偏平、钩子弱或上下文缺失时，`chapter_pipeline.py check/review` 可能返回警告或非零退出码。把它视为必须处理的质量门禁，不要因为 `finish` 仍可更新进度就忽略问题。
