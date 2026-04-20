# DBAIOps

<p align="center">
  📄 这是 DBAIOps 的官方仓库，对应 VLDB 2026 论文
</p>

<p align="center">
  <a href="https://www.vldb.org/pvldb/vol19/p1319-zhou.pdf"><strong>DBAIOps: A Reasoning LLM-Enhanced Database Operation and Maintenance System using Knowledge Graphs</strong></a>
</p>

<p align="center">
  🚀 面向数据库运维场景的浏览器扩展助手，支持知识问答、AWR 报告分析、巡检分析与 SQL 优化。
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Knowledge-Q%26A-3B82F6?style=for-the-badge" alt="Knowledge Q&A" />
  <img src="https://img.shields.io/badge/AWR-Analysis-0EA5E9?style=for-the-badge" alt="AWR Analysis" />
  <img src="https://img.shields.io/badge/Inspection-Review-14B8A6?style=for-the-badge" alt="Inspection Review" />
  <img src="https://img.shields.io/badge/SQL-Optimization-F59E0B?style=for-the-badge" alt="SQL Optimization" />
  <img src="https://img.shields.io/badge/Service-Integration-8B5CF6?style=for-the-badge" alt="Service Integration" />
</p>

<p align="center">
  <a href="#2-快速开始">快速开始</a> •
  <a href="#项目简介">项目简介</a> •
  <a href="#3-分析能力说明">分析能力说明</a> •
  <a href="#4-使用说明">使用说明</a> •
  <a href="#上游致谢">上游致谢</a>
</p>

<p align="center">
  <a href="./README.md">English</a> | <strong>简体中文</strong>
</p>

<p align="center">
  ⭐ 欢迎 Star 仓库，关注 DBAIOps 的后续更新。
</p>

```bibtex
@article{zhou2026dbaiops,
  author = {Wei Zhou and Peng Sun and Xuanhe Zhou and Qianglei Zang and Ji Xu and Tieying Zhang and Guoliang Li and Fan Wu},
  title = {DBAIOps: A Reasoning LLM-Enhanced Database Operation and Maintenance System using Knowledge Graphs},
  journal = {Proceedings of the VLDB Endowment},
  volume = {19},
  number = {6},
  pages = {1319--1331},
  year = {2026},
  doi = {10.14778/3797919.3797937},
  url = {https://www.vldb.org/pvldb/vol19/p1319-zhou.pdf}
}
```

---

## 项目简介

```text
DBAIOps_v1.1.1/
├── manifest.json                # 扩展入口、权限声明与 MV3 元数据
├── background_simple.js         # 运行时主要使用的后台 service worker
├── content.js                   # 页面注入脚本入口
├── config/                      # 注册服务、知识库服务与知识库默认配置
├── docs/                        # 从扩展代码迁移保留下来的技术说明
├── i18n/                        # 多语言资源与翻译初始化逻辑
├── icons/                       # 运行时图标、头像资源、主题图标与二维码兜底图片
├── js/                          # 弹窗、设置页、帮助页及功能模块实现
├── pages/                       # 弹窗、全屏页、设置页、帮助页、隐私页与策略页
├── styles/                      # 弹窗、设置页与内容注入样式资源
└── README_usage.md              # 随扩展保留的原始使用说明
```

## 1. 仓库概览

### 1.1 核心能力

| 模块 | 说明 |
|------|------|
| 知识问答 | 支持 SQL 语法、故障排查、性能调优、最佳实践等知识检索 |
| AWR 分析 | 上传 Oracle AWR HTML 报告并生成 AI 辅助分析结果 |
| 巡检分析 | 查看数据库巡检任务、历史记录与问题摘要 |
| SQL 优化 | 提交 SQL 优化任务并查看建议结果 |
| 服务集成 | 配置知识库服务地址、API Key 与模型服务商 |

### 1.2 扩展工作区补充说明

- `config/` 主要保存扩展侧配置模板与数据库知识库默认配置。
- `pages/`、`js/`、`styles/`、`i18n/`、`icons/` 和 `docs/` 共同构成扩展的主要界面、交互流程、多语言资源、运行时素材以及迁移后保留的技术说明。
- 扩展目录之外，`assets/` 用于 README 截图和演示素材，顶层 `icons/` 保留仓库级品牌资源，而 `DBAIOps_v1.1.1.zip` 则作为发布压缩包一并保留。

---

## 2. 快速开始

按照下面的五个步骤，即可完成 DBAIOps 的基础接入、配置校验与首次使用。

### 2.1 第一步：加载未打包扩展

1. 打开浏览器扩展管理页面，例如：
   <div>
     <code>chrome://extensions/</code>（Google Chrome）<br/>
     <code>edge://extensions/</code>（Microsoft Edge）
   </div>
2. 启用开发者模式。在 Chromium 系浏览器中，**开发者模式** 开关通常位于扩展管理页面的右上角。
3. 点击 **加载已解压的扩展程序**。
4. 选择以下目录：
```bash
./DBAIOps_v1.1.1
```
5. 确认扩展图标、弹窗页面与设置页面能够正常打开。

> 说明：GitHub README 的渲染通常不能稳定支持 `chrome://` 或 `edge://` 这类浏览器内部地址的直接跳转。如果页面中不可点击，请将地址复制到浏览器地址栏打开。

### 2.2 第二步：完成注册与知识库服务配置

#### 2.2.1 完成用户注册

![用户注册界面](assets/image-20250815140746815.png)

打开设置页面后填写用户信息。扩展默认会以 `config/registration.json` 作为注册服务模板，并在浏览器本地存储中保存个性化配置。

#### 2.2.2 配置知识库服务

![知识库服务配置](assets/image-20250815140930391.png)

进入知识库服务配置页面，填写 API Key 与服务地址。默认模板来源如下：
```bash
DBAIOps_v1.1.1/config/knowledge_service.json
```

### 2.3 第三步：配置模型服务商

当前 DBAIOps 通过浏览器端页面完成模型服务商配置。

#### 2.3.1 新增服务商并选择模型

![模型服务商配置](assets/image-20250815141625955.png)

常见流程如下：
1. 打开 **设置** -> **模型与服务商**。
2. 新增 `ollama`、`deepseek` 或其他兼容 OpenAI 接口的服务商。
3. 填写 API Base URL 与 API Key（如需要）。
4. 使用页面内测试功能验证连通性，并保存选中的模型。

![模型纳管界面](assets/image-20250815141948338.png)

#### 2.3.2 🧪 本地 Ollama 示例
```bash
http://localhost:11434/v1
```

#### 2.3.3 手动补充模型定义

![模型配置界面](assets/image-20250815142020584.png)

对于不支持自动发现的服务商，可以手动填写模型名称、Token 限制、温度等参数后保存配置。

![模型参数设置](assets/image-20250815142317185.png)

### 2.4 第四步：完成配置校验

保存注册信息、知识库服务配置和模型服务商配置后，建议确认以下事项：
- 能够正常选择目标知识库；
- 配置的服务地址可访问；
- 所选模型能够通过页面内的连通性测试；
- 弹窗页面能够正常提交问题并返回结果。

### 2.5 第五步：开始第一次使用

当扩展成功连通后，可以从以下任一流程开始实际使用：
- 在弹窗页或全屏页发起一次数据库知识问答；
- 上传 Oracle AWR 报告，并按照 [第 3.1 节](#31-awr-报告分析) 的流程进行分析；
- 参考 [第 3.2 节](#32-巡检分析) 查看巡检任务与历史摘要；
- 参考 [第 3.3 节](#33-sql-优化与脱敏) 发起 SQL 优化或脱敏相关任务。

---

## 3. 分析能力说明

### 3.1 AWR 报告分析

DBAIOps 当前保留了扩展内的 Oracle AWR 报告分析流程。

#### 3.1.1 📄 支持的数据来源
- Oracle 单实例 AWR HTML 报告
- 通过 `awrrpt.sql` 或 `awrrpti.sql` 生成的 RAC AWR 报告

#### 3.1.2 ⚠️ 当前说明
- `awrddrpi.sql` 生成的 AWR 对比报告不是当前主要目标场景。
- `awrgrpt.sql` 生成的全局报告建议在正式使用前先完成验证。

#### 3.1.3 ✅ 典型流程
1. 打开 AWR 分析面板。
2. 填写问题概述和接收邮箱（如需要）。
3. 上传 AWR 报告文件。
4. 选择分析语言。
5. 提交任务并在历史记录中查看结果。

### 3.2 巡检分析

当前扩展同样保留了数据库巡检分析流程，适合在运维回顾、周期性巡检和历史问题跟踪场景中使用。

![巡检诊断参考界面](assets/image-20251231152612751.png)

常见用途包括：
- 查看周期性巡检任务；
- 检查生成的摘要与异常项；
- 在模型或服务配置变更后重新分析历史任务。

### 3.3 SQL 优化与脱敏

DBAIOps 继续保留了扩展中的 SQL 优化与报告脱敏相关能力。

主要适用于：
- 提交 SQL 语句进行优化分析；
- 在上传报告前降低敏感 SQL 文本暴露风险；
- 为 DBA 与数据库工程师保留浏览器端分析流程。

---

## 4. 使用说明

#### 4.1 📦 打包与素材说明
- `DBAIOps_v1.1.1.zip` 作为发布压缩包被有意保留。
- `assets/DBAIOps_AWR_Analysis_Demo.mp4` 作为 AWR 功能演示视频被有意保留。
- `assets/DBAIOps_WeChat_Assistant_QR.jpg` 与 `assets/DBAIOps_Community_QR_Code.png` 作为支持与社区引导二维码素材被有意保留。
- `assets/` 下的截图文件继续保留，因为当前 README 与功能说明仍会直接引用这些素材。

#### 4.2 🛠️ 使用说明
- 本地验证时，请直接加载 `DBAIOps_v1.1.1` 作为未打包扩展，而不是再尝试运行旧版 DBAIOps 部署脚本。
- 如果浏览器内已有旧配置，建议在验证新地址前先执行扩展内配置重置。

## 上游致谢

当前仓库中的 DBAIOps 浏览器扩展工作区基于 BIC-QA 浏览器扩展代码整理与适配，并以 DBAIOps 的形式重新组织和交付。我们将 BIC-QA 视为本仓库的重要上游实现参考。上游项目： [BIC-QA 仓库](https://github.com/BIC-QA/BIC-QA)。
