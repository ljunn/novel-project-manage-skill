# 技巧栈

起草或返修章节前使用本索引。`scripts/chapter_pipeline.py compose` 会根据章节标题、当前目标、活跃伏笔和额外引导自动推荐一个紧凑技巧栈。只有当前问题明显需要其他卡片时，才覆盖推荐。

## 每章默认

始终启用：

- `references/chapter/writing-quickref.md`：章节、场景、语言基线。
- `references/chapter/chapter-workflow.md`：预读、分场、纯正文规则。
- `references/chapter/chapter-template.md`：正文文件里不能放什么。

## 按章节需求选择

开头偏弱 / 钩子不清：

- `references/chapter/hook-techniques.md`
- `references/chapter/literary-opening.md`
- `references/chapter/suspense-design.md`

场景像大纲 / 悬浮 / 只有概述：

- `references/chapter/descriptive-taxonomy.md`
- `references/chapter/content-expansion.md`
- `references/chapter/flow-break-writing.md`

对白解释太多 / 人物声音相似：

- `references/chapter/dialogue-writing.md`
- `references/quality/rule-linting.md`

回报偏弱 / 压力太多但缺奖励：

- `references/chapter/reader-compensation.md`
- `references/chapter/suspense-design.md`
- `references/quality/quality-checklist.md`

日常或过渡章节发平：

- `references/chapter/daily-narrative.md`
- `references/chapter/reader-compensation.md`
- `references/chapter/hook-techniques.md`

群像 / 多线压力：

- `references/chapter/ensemble-writing.md`
- `references/chapter/nonlinear-narrative.md`
- `references/quality/consistency.md`

返修 / 去生成腔 / 文本过于抽象：

- `references/quality/micro-revision-ops.md`
- `references/quality/anti-ai-rewrite.md`
- `references/chapter/descriptive-taxonomy.md`
- `references/quality/style-guardrails.md`

长篇阶段或分卷控制：

- `references/governance/longform-governance.md`
- `references/planning/outline-refinement.md`
- `references/planning/main-plot-construction.md`

平台包装：

- `references/platform/marketing.md`
- `references/platform/platform-output-gate.md`

## 技巧栈输出

起草前，把类似下面的紧凑技巧栈写进工作笔记，不写进正文：

```text
技巧栈：
- 基线：writing-quickref + chapter-workflow
- 主技巧：hook-techniques
- 支撑技巧：reader-compensation
- 风险护栏：rule-linting
```

随后正常起草正文。读者永远不应该看到技巧标签、节拍标签或场景卡标题。
