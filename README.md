# 小说项目管理技能

本仓库包含 `novel-project-manager` 智能体技能。

它融合了：

- 飞书知识库源思路中的需求文档、任务、进度和项目治理方法
- `junli-ai-novel` 深度章节流水线
- 写作技巧选择、质量门禁、正文纯度规则和长篇网文工作流约定

## 内容

- `novel-project-manager/SKILL.md`：技能入口和操作规则
- `novel-project-manager/scripts/novel_pm.py`：需求文档、任务、状态和调度工具
- `novel-project-manager/scripts/chapter_pipeline.py`：深度章节规划、写作、审阅和收尾流水线
- `novel-project-manager/references/`：项目模型、工作流、写作技巧、质量规则和深度流水线参考资料
- `novel-project-manager/rules/novel-lint/`：继承自深度流水线的正文巡检规则
- `wiki-source.md`：从飞书导出的源方案

## 校验

```bash
python3 -m py_compile novel-project-manager/scripts/*.py
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py novel-project-manager
```

## 基础用法

```bash
python3 novel-project-manager/scripts/novel_pm.py init <项目目录> --title "书名"
python3 novel-project-manager/scripts/novel_pm.py tasks <项目目录>
python3 novel-project-manager/scripts/chapter_pipeline.py preflight <项目目录>
python3 novel-project-manager/scripts/chapter_pipeline.py compose <项目目录> --chapter-num 1 --chapter-title "开篇"
```
