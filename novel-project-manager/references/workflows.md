# 工作流

执行用户请求而不是单纯解释技能时，使用本参考。

## 新项目

目标：把一个点子转成可管理的连载项目。

步骤：

1. 只收集六个必要信息：书名、题材、主角、核心冲突、目标字数/更新节奏、目标读者。
2. 运行：

   ```bash
   python3 scripts/novel_pm.py init <项目目录> --title "标题"
   ```

3. 根据用户点子填写需求文档，未知项明确标注。
4. 运行：

   ```bash
   python3 scripts/novel_pm.py tasks <项目目录>
   python3 scripts/novel_pm.py next-task <项目目录>
   ```

5. 汇报：已创建文件、需求文档缺失字段、下一项任务、第一个质量门禁。

如果点子已经足够启动，不要让用户填写大表。直接把点子转成需求文档草稿，并标出薄弱点。

## 今日调度

目标：用最高杠杆任务回答“今天写什么”。

步骤：

1. 运行 `status`。
2. 运行 `next-task`。
3. 检查该任务依赖的文件。
4. 从以下方向中选择：
   - 如果高优先级前置设定任务仍未完成，继续补前置设定；
   - 如果设定足够，写下一章计划章节；
   - 如果存在阻塞任务，先修阻塞；
   - 如果最新批次跨过质量门禁，先做质量检查。
5. 输出简短今日简报：
   - 今日任务；
   - 为什么轮到它；
   - 必读输入文件；
   - 预期交付物；
   - 质量门禁。

## 章节循环

目标：在不丢连贯性的前提下写作或返修章节。

预读顺序：

1. `.novel-project/.taskmaster/docs/prd.txt`
2. `.novel-project/.taskmaster/tasks.json`
3. `task_log.md`
4. `docs/项目总纲.md`
5. `docs/章节规划.md`
6. `plot/伏笔记录.md`
7. `plot/时间线.md`
8. 相关 `characters/*.md`
9. `manuscript/` 或旧别名 `chapters/` 中的上一章

起草前先运行内置深度流水线：

```bash
python3 scripts/chapter_pipeline.py preflight <项目目录>
python3 scripts/chapter_pipeline.py resume <项目目录>
python3 scripts/chapter_pipeline.py plan <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py compose <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py start <项目目录> <章节号> --chapter-title "标题"
```

快捷入口：

```bash
python3 scripts/chapter_pipeline.py next-chapter <项目目录> --chapter-title "标题"
```

写正文前，先写本章目标：

```text
- 核心事件：
- 开场状态 A：
- 章末状态 B：
- 本章必须兑现：
- 本章必须埋/推进：
- 章尾钩子：
- 禁止偏航：
```

`compose` 会自动把“推荐技巧栈”写入 `runtime/chapter-XXXX.intent.md` 和 `runtime/chapter-XXXX.context.json`。把它保留在工作笔记或运行时文件里，绝不写进正文。默认使用 `writing-quickref + chapter-workflow`，再只补充当前章节问题真正需要的技巧。

继承自 `junli-ai-novel` 的写作规则：

- 一章应有一个主导事件，最多两条主要线索。
- 每个场景都必须从状态 A 推进到状态 B。
- 对白要推动冲突或暴露人物，不要当作设定倾倒。
- 遵守贴身视角纪律，不泄露当前视角人物不可能知道的信息。
- 把抽象情绪转成动作、身体反应、决定和后果。
- 章末留下未解决压力，不用总结收尾。

写完正文后：

1. 统计字数。
2. 检查钩子、回报、冲突、连贯性、活跃伏笔和读者补偿。
3. 更新任务状态和进度记录。
4. 如果核心设定或结局方向改变，继续前先更新 `docs/变更日志.md`。
5. 保持正文文件只含故事正文，报告、摘要和作者说明都放到正文之外。

使用深度收尾链路：

```bash
python3 scripts/chapter_pipeline.py check <章节文件路径>
python3 scripts/chapter_pipeline.py lint <章节文件路径>
python3 scripts/chapter_pipeline.py dialogue-pass <章节文件路径>
python3 scripts/chapter_pipeline.py consistency <章节文件路径> --project-path <项目目录>
python3 scripts/chapter_pipeline.py review <章节文件路径> --project-path <项目目录>
python3 scripts/chapter_pipeline.py finish <项目目录> <章节号> <章节文件路径> --chapter-title "标题" --summary "摘要"
```

使用严格的 `junli-ai-novel` 正文约定：

- 写入 `manuscript/`；
- 从故事第一句直接开始；
- 文件名使用可识别章节格式，例如 `第0001章_标题.md` 或 `0001_标题.md`；
- 正文文件里不要出现 `# 第X章`、`## 正文`、元数据块、场景卡标题、作者说明或质量报告；
- 章节标题记录在文件名和 `docs/章节规划.md` 中。

## 质量管控

在以下门禁点做质量检查：

- 前 3 章完成后；
- 前 10 章完成后；
- 规划不稳定时每 5-10 章一次；
- 每卷结束时；
- 读者反馈显示预期错位时。

最低汇报格式：

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
- [优先级] 任务
```

## 长篇治理

满足任一条件时，把项目纳入长篇治理：

- 目标字数超过 100 万；
- 已写正文超过 30 万；
- 章节数超过 20；
- 用户要求分卷、阶段、审计、长线控制或结构调整。

必备文件：

- `docs/全书宪法.md`
- `docs/卷纲.md`
- `docs/阶段规划.md`
- `docs/变更日志.md`

如果缺失，先创建或补全，再推进大规模正文写作。

## 异常恢复

卡文：

1. 判断卡点是缺目标、缺冲突、缺代价、缺信息，还是缺过渡。
2. 给出三个方向。
3. 把选定方向转成具体任务。

设定冲突：

1. 停止写正文。
2. 判断更高优先级来源：全书宪法/世界规则 > 需求文档/大纲 > 任务状态 > 草稿。
3. 修正低优先级来源。
4. 如果影响长期剧情，记录变更。

节奏失衡：

1. 检查是否连续三章缺少回报。
2. 增加小高潮任务，或压缩铺垫。
3. 让下一章交付可见结果。

负面反馈：

1. 区分“承诺错了”和“执行偏弱”。
2. 提取反复出现的读者期待。
3. 优先更新后续任务；只有初始承诺本身坏了，才重写旧章节。
