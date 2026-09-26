# 教案技能（jiaoan-skill）

根据课程名称一键生成**可提交的 Word 教案**：整本教案（封面 + 课程信息表 + 每次课教案表）或单节课教案；支持套用学校模板、更新老教案。

核心解决 AI 生成教案的两大痛点：
- **内容空洞** —— 每个知识点都嵌入"六要素"真实案例（背景 / 与教学目标的关系 / 实施过程 / 成果与数据 / 教学点评 / 课堂提问），实施过程分步可操作，无数据不编造
- **缺图可读性差** —— 配图下限硬性保证（上机/实训 ≥6 张/节，混合 ≥5，理论 ≥4），案例图优先真实网图并标来源，AI 生成图无水印、逐张检查错字

同时保证：
- **时间预算精确** —— 每课"时间安排"行，上机必拆"学生独立练习 + 教师巡回辅导"，环节分钟相加 = 总课时
- **格式严谨** —— 小标题逐行、案例六要素分段、行距留白规范，可直接提交
- **懒人审核** —— 回复单个数字即可（1 继续 / 0 生成全部 / 2 图片 / 3 案例 / 4 内容 / 5·6·7 组合 / 9 全部重做）
- **整本先预研** —— 生成前检索人才培养方案，出约 500 字教学目标与内容框架，经你核实后再生成

## 安装（豆包 / Claude Code / Cursor 等支持 Agent Skills 的环境）

```bash
npx skills add https://github.com/liuning60/jiaoan-skill -skill lesson-plan-generator
```

或手动安装：把本仓库 `lesson-plan-generator/` 文件夹放入环境的技能目录（豆包：`...\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\`），重启即生效。

## 使用示例

> "用教案技能给《数字视觉设计》生成整本教案，高职，18 周每周 4 节，套郑州旅院模板"

按提示回答 9 个必问项（模式 / 学段学科 / 课程名 / 课时 / 课程类型与时间构成 / 配图偏好 / 界面图选项 / 模板 / 运行平台），即可获得整本或单节教案。

## 跨平台兼容

- **默认豆包**；也可在 Claude Code / Cursor 等环境运行（详见 SKILL.md「跨平台工具映射表」——流程与验收标准一致，仅工具通道不同）
- 英文版见姊妹仓库：https://github.com/liuning60/lesson-plan-generator

## 目录结构

```
jiaoan-skill/
├── README.md
├── LICENSE              (MIT)
└── lesson-plan-generator/        ← 技能本体（中文版）
    ├── SKILL.md
    └── references/
        ├── case-engine.md         案例六要素与检索策略
        ├── image-engine.md        配图下限、水印、网图取舍、体积控制
        ├── interaction-protocol.md 数字审核协议
        ├── lesson-structures.md   大学/中学结构、时间安排、排版规范
        ├── template-and-update.md 套模板、老教案更新、踩坑解法
        └── lessons-learned.md     实测踩坑与验收清单
```

## License

MIT — 可自由使用、修改、再分发，商用亦可（详见 LICENSE）。
