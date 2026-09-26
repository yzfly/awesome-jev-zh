# Awesome Jev ZH

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-black.svg?style=flat-square)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/license-CC0--1.0-black.svg?style=flat-square)](LICENSE)
[![自动收录](https://img.shields.io/badge/热门项目-每日自动收录-black.svg?style=flat-square)](#-热门项目自动榜)

**Jev 不生成文本。** 第一次看到这句话时我以为是个缺陷，后来才发现这正是它的设计核心。

它的用法是：给它一段 state（一封邮件、一行日志、一个工单），再给它几个带类型的问题，它在 70–500ms 内一次性答完——从你给的选项里选一个、在你给的量表上打一个分、或者给出一个 0 到 1 的概率，每个答案都附带一个置信度。输入 $0.042 / MTok，输出不计费。

它的边界也很清楚：要写文案、要总结文章、要解释判断理由，LLM 仍然是更合适的工具。这一条后面还会出现好几次。

那它解决了什么？整理这份列表的过程中，我越来越确信一件事：**我们今天写的很多 LLM 调用，本质上只是在做选择题。** 拼 prompt、逐 token 生成、剥掉 markdown 代码块、`json.loads`、校验 schema、失败了再重试——绕这么大一圈，只为了拿回 `"billing"` 这一个词。这段代码我自己写过不止一次。Jev 想省掉的就是这一圈。

另外有两个数字想先摆出来，免得看完才发现：**「快 193 倍」来自 TypeSafe 自己的评测**，官方也标注了那是收益上限；而独立评测里，在钓鱼邮件这个具体任务上，直接问它一句只有 62.6% 的准确率，两行正则规则能到 91.8%。完整数据在 [冷静看待](#-冷静看待) 一节。

这是 Jev 生态的中文精选列表，外加两份中文指南和一份 [图解说明](https://code.jiangshu.ai/awesome-jev-zh/)。

<sub>非官方整理，与 TypeSafe AI 无隶属关系 · Jev 于 2026-09-15 开放 early access · 所有厂商自评数据都标注了出处</sub>

---

## 目录

**入门** — [官方资源](#-官方资源) · [优质项目](#-优质项目) · [Jev 是什么](#-jev-是什么) · [体验渠道](#-体验渠道) · [上手](#-上手) · [规格与定价](#-规格与定价) · [该用与不该用](#-该用与不该用) · [中文指南](#-中文指南)

**项目** — [热门自动榜](#-热门项目自动榜) · [SDK](#-sdk-与客户端) · [应用](#-应用) · [Demo](#-demo) · [Agent 工具](#-agent-工具) · [复现与评测](#-复现与评测)

**资料** — [Cookbook 与模式](#-cookbook-与模式) · [文章](#-文章) · [社区](#-社区) · [冷静看待](#-冷静看待)

---

## 📘 官方资源

官方文档写得相当清楚。真要弄懂这个模型，这里是最短的路径；二手解读（包括这份列表）只能算补充。

| 资源 | 说明 |
| :-- | :-- |
| [TypeSafe 官网](https://typesafe.ai) | 官网、waitlist、产品介绍 |
| [文档首页](https://docs.typesafe.ai/introduction) | 入门、原语、模式、API、SDK |
| [Quick start](https://docs.typesafe.ai/introduction/quickstart) | 最短上手路径，下面 [上手](#-上手) 一节是它的中文版 |
| [Playground](https://console.typesafe.ai/playground) | 浏览器里粘 state、加问题、看类型化结果 |
| [API Keys 控制台](https://console.typesafe.ai/settings/keys) | 拿 `TYPESAFE_API_KEY` |
| [HTTP API 参考](https://docs.typesafe.ai/api) | `POST https://api.typesafe.ai/v1/systemone` |
| [Models](https://docs.typesafe.ai/models) | 模型 ID、价格、上下文与速率限制 |
| [Confidence](https://docs.typesafe.ai/confidence) | 置信度的语义与用法，必读 |
| [State 概念](https://docs.typesafe.ai/concepts/state) | 怎么组织喂进去的状态 |
| [System One 概念](https://docs.typesafe.ai/concepts/system-one) | 这类模型到底是什么 |
| [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one) | 官方的架构心法 |
| [用例地图](https://docs.typesafe.ai/concepts/use-case-map) | 官方列的适用场景全景 |
| [AI 入门读本](https://docs.typesafe.ai/introduction/machine-learning-primer) | 给非 ML 背景工程师的铺垫 |
| [Jev 1.13 能力毛边](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | 官方公布的已知失败模式，上生产前必读 |
| [Workflow evals](https://evals.typesafe.ai) | 官方公开的评测方法与结果，属厂商自评 |
| [Agent skill 文档](https://docs.typesafe.ai/agent-skill) | 给 Claude Code / Codex 等编程 Agent 的技能包 |
| [GitHub 组织 `typesafe-ai`](https://github.com/typesafe-ai) | 官方开源仓库 |
| [法务条款](https://docs.typesafe.ai/legal) | 数据使用与合规 |

官方博文，四篇立场文章：

| 博文 | 内容 |
| :-- | :-- |
| [Introducing System One Models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | 发布博文。架构、RLCD、定价、Doom 与 Wikiracing demo、FAQ |
| [The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson) | 它的核心论点：优化错了任务，规模再大也盖不过去 |
| [AI: too good to be true, too bad to be useful](https://typesafe.ai/blog/ai-too-good-to-be-true-too-bad-to-be-useful-typesafe-ai) | 为什么自动化不该用偏好对齐过的聊天模型 |
| [Manifesto](https://typesafe.ai/manifesto) | 主张给软件用的机器原生智能，而不是聊天 |

---

## ⭐ 优质项目

Star 过 500 的项目，全生态一共这些。时间有限就先看这一栏，方向从浏览器操作、Agent 框架、上下文工程一直排到几个能自己训的开源复现。

> 门槛是**纯 Star 数**（2026-09-21 UTC 快照，表里的徽章实时更新）。Star 多只说明被最多人看过、试过、吵过，不等于代码质量好或者能直接上生产——这里面大半是 Jev 发布一周内写出来的。表格按星数降序，所以第二行的 QuantDinger 是个规模完全不同的项目，看说明就明白了。每行都标了它所在的分区，想看同方向的其他项目往那儿翻。

| 项目 | Star | 方向 | 说明 |
| :-- | :-- | :-- | :-- |
| [**browser-use/jev-ultrafast**](https://github.com/browser-use/jev-ultrafast) | ![](https://badgen.net/github/stars/browser-use/jev-ultrafast) | 浏览器 Agent | 全生态第一爆款。一次请求里让 Jev 同时选出「做什么操作」和「操作哪个 DOM 元素」，只有真要打字时才叫小模型。Google Flights 苏黎世→伦敦订票 **7 秒 / $0.0039**。同类见 [应用](#-应用) |
| [**OpenByteInc/QuantDinger**](https://github.com/OpenByteInc/QuantDinger) | ![](https://badgen.net/github/stars/OpenByteInc/QuantDinger) | 交易系统 | 开源交易 OS，下单前的决策网关从 LLM 换成 Jev（走 `/v1/systemone`，没配 key 就回退 LLM）。**它的 Star 主要来自交易系统本身，Jev 只是一个可选组件**，放在这儿是因为规则只看星数。同类见 [应用](#-应用) |
| [**NandhaKishorM/laya**](https://github.com/NandhaKishorM/laya) | ![](https://badgen.net/github/stars/NandhaKishorM/laya) | 多语言决策模型 | 非自回归 System 1 决策引擎：单问题 33ms、批量 7.2ms/问（T4 自测），同样用严格评分规则做 RL，**覆盖 100+ 语言**——中文场景想找可自建的替代品，这是目前星数最高的一个。作者称此路线早于 Jev，README 里与 Jev 的同数据集对比属自评 |
| [**tamaratran/fast-jev-compaction**](https://github.com/tamaratran/fast-jev-compaction) | ![](https://badgen.net/github/stars/tamaratran/fast-jev-compaction) | 上下文工程 | Claude Code 插件：把上下文压缩的「总结」换成 Jev 判断——每次工具调用和结果都打分，决定留不留。**上下文工程的新范式**，[Agent 工具](#-agent-工具) 里的 winnow、yoshi 都是同一思路的变体 |
| [**vercel/eve**](https://github.com/vercel/eve) | ![](https://badgen.net/github/stars/vercel/eve) | Agent 框架 | Vercel 的 Agent 框架，实验性 `autoModel` 默认用 Gateway 上的 `typesafe-ai/jev` 从白名单里挑语言模型。目前把 Jev 放进默认路径的主流框架，就这一个。同类见 [Agent 工具](#-agent-工具) |
| [**TheoLeeCJ/SemIf**](https://github.com/TheoLeeCJ/SemIf) | ![](https://badgen.net/github/stars/TheoLeeCJ/SemIf) | 开源复现 | 最受关注的复现，原名 `openjev`。一张 RTX 3090 能不能跑 Jev 风格的东西？直接读选项 logits，不生成文本。**不是 TypeSafe 的模型**，作者自己也强调无隶属关系。同类见 [复现与评测](#-复现与评测) |
| [**TianyuCodings/NanoJev**](https://github.com/TianyuCodings/NanoJev) | ![](https://badgen.net/github/stars/TianyuCodings/NanoJev) | 开源复现 | nano 版 Jev：并行决策、动态候选、端到端训练流水线。**想搞懂训练的从这个读** |
| [**jarrodwatts/jev-trader**](https://github.com/jarrodwatts/jev-trader) | ![](https://badgen.net/github/stars/jarrodwatts/jev-trader) | 链上交易 | 每个 Monad 区块对 Kuru 的 MON-USDC 做一次买卖决策——区块时间摆在那儿，这是少数几个「延迟本身就是硬约束」的场景。在线：[jev-trader.vercel.app](https://jev-trader.vercel.app/) |
| [**jaredpalmer/kev**](https://github.com/jaredpalmer/kev) | ![](https://badgen.net/github/stars/jaredpalmer/kev) | 开源复现 | Qwen 上挂 LoRA + readout head（0.5B–8B），`POST /v1/systemone` 与官方 SDK 兼容，改个 `base_url` 就能跑本地。冻结评测集上域外 kev-8b 0.77 对真 Jev 0.86（作者自测）。M5 上 1h45m 能训出 0.5B |
| [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) | ![](https://badgen.net/github/stars/typesafe-ai/skills) | 官方技能包 | 官方出的 Agent 技能包：原语、模式、怎么组织 evaluation。`claude plugin install typesafe@typesafe-ai`。其余官方仓库见 [官方资源](#-官方资源) 与 [SDK](#-sdk-与客户端) |
| [**bespokelabsai/nimble**](https://github.com/bespokelabsai/nimble) | ![](https://badgen.net/github/stars/bespokelabsai/nimble) | 开源复现 | Bespoke Labs 出的开源 Jev：数据、训练、服务三件套一起给。Qwen3.5-9B 上只对答案 token 做 LoRA，324 条留出样本对齐参考标签 **90.1%**（基座 66.4%、Jev 1.13.0 93.2%），**明确声明没有蒸馏 Jev**。Mac 与 NVIDIA 都能跑。同类见 [复现与评测](#-复现与评测) |
| [**vinnylarouge/jevlike**](https://github.com/vinnylarouge/jevlike) | ![](https://badgen.net/github/stars/vinnylarouge/jevlike) | 开源复现 | 训练一个小的单次 scorer：上下文 + N 个文本选项 → 每个选项一个概率。含 Doom / 国际象棋视觉 demo。**明确声明不是 TypeSafe 架构或 RLCD 的复现** |
| [**yibie/awesome-jev**](https://github.com/yibie/awesome-jev) | ![](https://badgen.net/github/stars/yibie/awesome-jev) | 清单 | 另一份英文清单，除了项目和集成还收社区争论，想看反对意见的去这儿。其他同类见 [其他 awesome 列表](#其他-awesome-列表) |
| [**Anil-matcha/awesome-jev-by-typesafe**](https://github.com/Anil-matcha/awesome-jev-by-typesafe) | ![](https://badgen.net/github/stars/Anil-matcha/awesome-jev-by-typesafe) | 清单 | 英文清单里做得最细的一份：用例、模式、prompt、起步代码，每条都标了出处。其他同类见 [其他 awesome 列表](#其他-awesome-列表) |
| [**awlevin/typesafe-computer-use**](https://github.com/awlevin/typesafe-computer-use) | ![](https://badgen.net/github/stars/awlevin/typesafe-computer-use) | computer use | macOS computer-use：OCR 屏幕 → Jev 分类下一步动作 → 点击。约 **$0.0002/步** |
| [**githubnext/localjev**](https://github.com/githubnext/localjev) | ![](https://badgen.net/github/stars/githubnext/localjev) | 协议桥 | GitHub Next 出的协议桥：本机起一个 Jev 兼容的 `/v1/systemone`，背后转成分类 prompt 发给任意 OpenAI 兼容端点。**概率是模型自报的，不是读 logits**，作者写明「wire-compatible, but not mathematically equivalent」。同类见 [复现与评测](#-复现与评测) |
| [**milind-soni/tiptour-macos**](https://github.com/milind-soni/tiptour-macos) | ![](https://badgen.net/github/stars/milind-soni/tiptour-macos) | computer use | macOS 本地 computer use：CoreML + OCR 在本机认出按钮和文字，Jev 只从这份控件清单里选点哪一个，截图不出本机。作者报单步约 90ms。同类见 [应用](#-应用) |

剩下的项目按用途分在 [SDK](#-sdk-与客户端)、[应用](#-应用)、[Demo](#-demo)、[Agent 工具](#-agent-工具)、[复现与评测](#-复现与评测) 五栏里，每天重抓的完整榜单在 [热门自动榜](#-热门项目自动榜)。

---

## 🧠 Jev 是什么

它针对一份 state——一封邮件、一行日志、一个工单、一坨游戏坐标 JSON——评估一组带类型的问题，返回代码能直接 `if`、能排序、能路由的值。就这么简单。

TypeSafe 管这类模型叫 System One，取自卡尼曼的「系统一」，快速直觉的那套。训练方法叫 RLCD，优化目标是概率诚实而不是人类偏好——RLHF 那套「让人满意」的训练会毁掉校准，因为犹豫的回答不讨喜。对聊天这是优点，对自动化这是灾难：你没法拿一个假的 90% 去写门控。

**这套说法目前没有公开论文。** 校准好不好，在你自己的数据上量，别信任何人的 slide。

<details>
<summary><b>那它背后到底是什么技术？</b>（官方不说，但开源复现已经把机制拼出来了）</summary>

官方**刻意没有公开架构**：参数量、模型类别、训练数据组成全部未披露，发布博文的 FAQ 里「为什么需要新的训练算法」「这个结果怎么做到的」两条明写了不在本文回答。所以下面分两块——官方声称的，和复现者实际做出来的。

**官方声称的三点**

- 叫 System One 模型，取自卡尼曼的「系统一」
- 训练方法 RLCD，优化目标是概率校准而非人类偏好（无论文、无公式、无算法步骤）
- **并行而非自回归**：「一次查询生成全部输出」，不逐 token 解码——40–200 倍加速归因于此，但没给数学解释

**复现者做出来的机制**（这部分有代码可读，比官方博文实在）

[jaredpalmer/kev](https://github.com/jaredpalmer/kev) 的说明最清楚，它用 Qwen 2.5-0.5B ~ 3-8B 作骨干 + LoRA（r=16）：

- **不解码，用 pointer head 打分**——把每个选项的 `</opt>` 隐状态与 `<decide>` 隐状态相互打分，再过 softmax。概率来自这个打分头的监督训练，不是 next-token 预测
- **一次前向答完多题**——所有问题和 state 打包进同一条 token 序列，用 **block-causal 注意力掩码**让每个问题都能看到 state、但看不到兄弟问题；每个问题分支的 position id 重新计数，所以**问题顺序不影响结果**。作者实测打包请求与拆开单发的结果一致到 `4e-6`
- **训练**：在选项分布上做交叉熵，训练数据和线上请求走同一个渲染器。学习率是关键，5e-5 比默认 2e-4 好，高了会「侵蚀基座模型已有的知识」

[TheoLeeCJ/SemIf](https://github.com/TheoLeeCJ/SemIf)（直接读选项 logits）、[TianyuCodings/NanoJev](https://github.com/TianyuCodings/NanoJev)、[vinnylarouge/jevlike](https://github.com/vinnylarouge/jevlike) 三家路子一致。所以公开可验证的那部分机制可以概括成一句：**一个普通的 transformer 骨干，外挂一个在候选项上打分的 readout head，一次前向把所有题答完，靠掩码保证题与题之间互相看不见。**

这也解释了它的几个硬边界：选项必须预先穷举（所以 Choice 上限 255）、不可能输出 schema 之外的东西（结构上做不到幻觉）、以及为什么它彻底不会写字——模型里根本没有解码这一步。

注意复现者都声明过与 TypeSafe 无隶属关系，也没说自己复现了 RLCD。**上面是「一个能跑出类似行为的合理机制」，不是 TypeSafe 的实现。**

</details>

| | 大语言模型 | Jev |
| :-- | :-- | :-- |
| 输出 | 字符串，逐 token 生成 | 类型化的值 + 概率 + 置信度 |
| 幻觉 | 可能编造，可能违反 schema | 结构上不可能，合法输出已在 schema 里穷举 |
| 延迟 | 秒级 | 70–500ms，一次并行 pass 答完所有问题 |
| 输入价格 | 通常 $0.1–$15 / MTok | $0.042 / MTok |
| 输出价格 | 按 token 计费 | 不计费 |
| 写代码、写文章 | 会 | 完全不会，这是设计 |
| 擅长 | 生成、推理、对话 | 分类、路由、打分、抽取、过滤、选下一步动作 |

一句话：一次前沿智能的函数调用。非结构化状态进，类型化概率决策出。

### 三个原语

| 原语 | 问它什么 | 返回 | 典型用途 |
| :-- | :-- | :-- | :-- |
| [**Choice**](https://docs.typesafe.ai/primitives/choice) | 从这些选项里选一个 | `choice` + `probabilities` + `confidence` | 意图路由、工单分派、选下一个点击的元素、function calling |
| [**Score**](https://docs.typesafe.ai/primitives/score) | 按这个量表给它打分 | `score` + `probabilities` + `confidence` | 质量打分、情绪强度、优先级、重排序 |
| [**Noul**](https://docs.typesafe.ai/primitives/noul) | 这句话是真的吗 | `noul`（0–1 的概率） | 护栏、是非校验、语义检索、内容审核 |

同一次请求里的问题对同一份 state **并行求值、彼此隔离**——它们互相看不见对方的答案。所以别指望它做多步推理，那不是它的活。

核心心法就一句，记不住别的也得记住这句：**问题尽量原子，组合逻辑写在你自己的代码里。** 后面有数据证明这句话值 32 个百分点。

<details>
<summary><b>术语对照</b>（读英文文档前先统一一下词）</summary>

| 英文 | 本列表译法 | 说明 |
| :-- | :-- | :-- |
| System One model | 系统一模型 | 与「系统二」（会推理会生成的 LLM）相对 |
| state | 状态 | 你丢给模型的那坨上下文，字符串 / JSON / 文本数组均可 |
| typed question | 带类型的问题 | Choice / Score / Noul 三选一 |
| Noul | 保留原词 | TypeSafe 生造词，指 0–1 的是非真值概率，不译 |
| criteria | 判据 / 选项 | Choice 是选项字典，Score 是量表档位 |
| calibrated probabilities | 校准概率 | 模型说 70%，长期就该有 70% 对 |
| confidence | 置信度 | 告诉你「要不要动手」，答案告诉你「是什么」 |
| RLCD | 校准决策强化学习 | TypeSafe 自研训练方法 |
| speculative fan-out | 投机扇出 | 一次多问几题（含用不上的），在代码里筛 |
| cardinality | 候选基数 | 单个 Choice 最多 255 个选项 |
| jaggedness | 能力毛边 | 官方主动公布的失败模式清单 |

</details>

---

## 🚪 体验渠道

「我想试试 Jev」这件事，今天一共有五条路：**免密钥试用**、**托管网关**、**官方直连**、**无 key 先写代码**、**自己跑**。官方那条要排 waitlist，但完全不必干等。

下面每条都标了要不要排队、要不要付钱、以及我踩到的坑。**标「实测」的数字来自 2026-09-19 我在自己机器上的真实调用**，脚本见各小节；标「官方」的来自厂商文档，两者别混着看。

| 渠道 | 要排队 | 要付钱 | 模型 ID | 延迟（实测中位） | 一句话 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| [**classifier.dev**](https://classifier.dev/) | 不用 | **完全免费，连注册都不用** | 上报 `jev-1.13.0` | 220ms 逐条 · **20ms 批量** | 想立刻摸到真 Jev 就走这条，代价是只剩「分类」一个功能 |
| [**Vercel AI Gateway**](https://vercel.com/ai-gateway/models/jev) | 不用 | **要绑信用卡**，送 $5 | `typesafe-ai/jev` | 310–370ms | 三个原语齐全的最快路径，绑卡这关劝退不少人 |
| [TypeSafe 官方 API](https://console.typesafe.ai/settings/keys) | **要** | 看配额 | `jev-latest` / `jev-1.13.0` | 官方称 70–500ms | 功能最全、延迟最低，但得等 |
| [官方 Playground](https://console.typesafe.ai/playground) | 看账号 | — | — | — | 不写代码，粘一段 state 点几下 |
| [官方 adapter](https://github.com/typesafe-ai/system-one-adapter-python) | 不用 | 用你自己的 LLM key | — | 取决于后端 | 先把代码写完，后端暂时挂普通 LLM |
| [OpenRouter](https://openrouter.ai/typesafe/jev-1.13) | — | — | `typesafe/jev-1.13` | — | **暂时别指望**，见下 |
| 开源复现（[kev](https://github.com/jaredpalmer/kev) · [SemIf](https://github.com/TheoLeeCJ/SemIf) · [laya](https://github.com/NandhaKishorM/laya)） | 不用 | 自己的显卡 | 自己训 | 看硬件 | 唯一能完全离线、数据不出内网的路子，见 [复现与评测](#-复现与评测) |

### 零门槛：classifier.dev

**不用注册、不用 key、不用绑卡，一条 curl 就能碰到真的 Jev 1.13。** 目前门槛最低的一条路，没有之一：

```bash
curl "https://classifier.dev/billing,technical,sales/我的信用卡被扣了两次款"
# billing
```

要拿结构化结果就走 POST，返回体里会写清楚到底调了什么模型：

```bash
curl -X POST https://classifier.dev/ -H "Content-Type: application/json" \
  -d '{"input":"线上全挂了，所有接口 502","labels":["billing","technical","sales"]}'
```

```json
{
  "tier": "fast",
  "model": "jev-1.13.0",
  "modelsUsed": ["jev-1.13.0"],
  "results": [{ "label": "technical", "confidence": 1,
                "scores": { "billing": 0, "technical": 1, "sales": 0 } }]
}
```

字段名有个小坑：单条用 `input`，批量用 `inputs`（传数组，最多 1000 条）；写成 `text` / `texts` 会返回 `no_input` 错误。

官方给的免费额度是 fast 档 3,000 次/分钟、20,000 次/天（按 IP 算），smart 档 200/分钟、2,000/天；Pro $20/月按账号放大十倍。

### classifier.dev 和 Jev 是什么关系

先说最容易误会的一点：**它不是 Jev 的竞品，它是搭在 Jev 上的。** 返回体里的 `"model": "jev-1.13.0"` 和官方直连是同一个模型同一个版本。所以「谁更准」这个问题本身问错了——同样的输入，它们给的是同一个答案。

真正的区别在**你能往里喂多少信息**，以及**出事时会发生什么**：

| | classifier.dev | Jev 直连（官方 / Gateway） |
| :-- | :-- | :-- |
| 门槛 | 无注册、无 key、无卡 | Gateway 要绑卡；官方要排队 |
| 能用的原语 | 只有分类，即 Choice 的一个子集 | Choice / Score / Noul 三个都有 |
| 一次请求问几题 | 1 题 | 多题并行，**实测加到 4 题延迟不变** |
| 选项能否带描述 | **不能，只能给标签词** | 能，`criteria` 里每个选项都能写说明 |
| 批量 | 一次最多 1,000 条，实测 **20ms/条** | 按请求算 |
| 出错时 | Jev 不可用会**静默回退到一串 LLM**（官方说明），要看 `modelsUsed` 才知道 | 报错就是报错 |
| smart 档 | 不确定的答案升级到推理模型，实测最慢 **3.5s** | 无此概念 |
| 计费 | 免费 / $20 月订阅 | $0.042 / MTok |

那个「选项能否带描述」不是小事。我用同一份中文数据量过，**光给标签词比给带描述的标签，准确率掉 13.3 个百分点**（80.0% → 93.3%，3 轮完全复现）。Jev 直连的 `criteria` 能写「支付、扣款、发票、退款、订阅账单」，classifier.dev 只能收一个 `billing`——差的就是这个。

所以选型很清楚：**摸底、原型、一次性脚本用 classifier.dev；真要上生产，尤其是需要 Score / Noul、需要一次问多题、或者不接受静默回退的，走直连。**

### 中文场景小实测

这份列表里一直缺中文数据，我补一组。15 条中文客服工单，我自己标的部门与紧急度，走 Vercel Gateway 直连 Jev，一次请求同时问三题（Choice 路由 + boolean 紧急 + Score 不满程度）：

| 指标 | 结果 |
| :-- | :-- |
| 部门路由准确率 | **14/15 = 93.3%** |
| 紧急度准确率 | **14/15 = 93.3%** |
| 延迟 | 最快 281 / 中位 370 / p95 448 ms |
| 唯一错判 | 「优惠券输进去提示无效，但明明还没过期」判成 technical（conf 0.85），我标的是 billing |

> **这不是评测，别当评测引用。** n=15、标签我一个人定的、错判那条本身就模棱两可（优惠券失效算账单问题还是程序问题？换成人也会犹豫）。它只够说明「中文没有明显掉链子」，不够支撑任何百分比结论。严肃的中文评测目前仍然只有 [judgekit](#独立评测) 一份。

有两个现象值得单独记一笔：

**一，批量比逐条准。** 同样 15 条数据，一条条发准确率 80%，塞进一个请求发是 15/15，3 轮完全一致、不是噪声。推测是同一批里的其他样本给了模型相对参照。这条在官方文档里没见人提过，**如果你的场景能攒批，攒批不只是快，可能还更准**。

**二，confidence 在中文上偏饱和。** 15 条里 12 条直接给 1.00。唯一那条错判确实掉到了 0.85，最低的 0.70 反而是对的——所以拿 confidence 做门控在这份数据上能用，但阈值别卡太高，1.00 出现得太频繁了。上生产前务必在你自己的数据上重新量，这也是官方 [Confidence 文档](https://docs.typesafe.ai/confidence) 反复强调的。

### 本地部署：完全离线的几条路

数据不能出内网、或者延迟要压到实时交互那个量级（语音、控制回路）的时候，托管渠道就不够看了。Jev 本身没有开放权重，但几个开源复现已经能跑出同类行为，**其中 laya 是唯一进入实时区间的**：

| 方案 | 骨干 | 参数 | 单题延迟 | 批量 | 硬件 | 原语 | 许可 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| [**laya-multilingual**](https://github.com/NandhaKishorM/laya) | mmBERT-base | **322M** | **32.8 ms** | **7.2 ms/题** | 单张 T4 | choice / score / noul 全有 | Apache-2.0 |
| [laya](https://github.com/NandhaKishorM/laya) | ModernBERT-large | 421M | 39.5 ms | 15.9 ms/题 | 单张 T4 | 同上 | Apache-2.0 |
| [kev-0.5b](https://github.com/jaredpalmer/kev) | Qwen2.5-0.5B + LoRA | 0.5B | ~160 ms (fp32) | — | 消费级即可 | typed questions | Apache-2.0 |
| [kev-4b](https://github.com/jaredpalmer/kev) | Qwen3-4B + LoRA | 4B | ~1 s (bf16) | 3 题 277ms (M5) | 32GB Mac | typed questions | Apache-2.0 |
| [SemIf](https://github.com/TheoLeeCJ/SemIf) | Qwen3.5-4B | 4B | 1.02 s | 20 决策/秒（共享 state） | RTX 3090 / MLX | 直读选项 logits | MIT |

两点值得单独说：

**kev 的卖点是 API 兼容。** `python -m kev.serve --run jaredpalmer/kev-4b --port 8009` 起一个 `/v1/systemone` 端点，官方 SDK 改个 `base_url` 就切过来了——**先拿官方 API 把代码写完，再无痛换本地**，这条路径目前只有它提供。代价是慢：4B 在 Apple Silicon 上约 1 秒。冻结测试集上 kev-4b 0.790 对真 Jev 0.857（作者自测，764 条）。

**laya 的中文表现是这几个里最好的，而且它不是 4B 大模型，是个 322M 的编码器。** 51 种语言的 MASSIVE intent（20 选项，随机基线 0.05）上 `zh-CN` 拿 0.630、`zh-TW` 0.540，zh-CN 在整个语言表里排前列。

作者还自测了 laya 对 Jev：typed-decisions 0.766 对 0.727、AG News 0.950 对 0.910、DAIR Emotion 0.595 对 0.480。**我们复现了后两项，结论只对了一半**（各 400 条，托管的真 Jev 1.13 走 Vercel AI Gateway，两种提示写法都试过取各自最好的）：

| | 本地 laya（fp32） | 真 Jev 1.13 |
| :-- | --: | --: |
| AG News | **92.8%** | 85.5%（原生 criteria）／88.0%（classifier.dev） |
| dair-ai emotion | 54.0% | **61.5%**（原生 criteria）／62.7%（classifier.dev） |

AG News 上 laya 确实赢，方向与作者自评一致；**但 emotion 上方向是反的**——作者称 laya 0.595 胜 Jev 0.480，实测是 Jev 赢 8–9 个点。细粒度情绪分类要用 laya 的，务必先在自己的数据上量。

另一条容易踩的：**提示写法不能跨模型迁移。** 同一个任务，给选项加描述对两者的影响方向相反——AG News 上 laya +1.6 / Jev −2.5，emotion 上 laya −7.2 / Jev +1.4。换模型必须重调。

#### 把上面这些跑到 CPU 上：EdgeJev

> 利益相关：[**yzfly/edgejev**](https://github.com/yzfly/edgejev) 是本清单维护者写的，刚发布，star 数还不够进 [优质项目](#-优质项目) 那一栏。放在这里是因为它正好解决这一节的问题，数据都可以自己复现。

上面那张表的延迟大多是 GPU 上的数字。laya 自己的提示里写着 CPU 上 `~200-500 ms`——真要落到没有显卡的机器上，得先做一轮 ONNX + 量化。EdgeJev 把这一步打包成 `build / serve / eval / bench` 四个命令，**运行时只要 onnxruntime + tokenizers + numpy，不需要 torch**，Linux / macOS（Apple Silicon 走 CoreML）/ Windows 都能跑。

```bash
uv tool install "edgejev[build]"
edgejev build --backend laya --out ./jev-int8   # 只此一步要 torch
edgejev serve --model ./jev-int8 --port 8009    # 官方协议的 /v1/systemone
```

4 vCPU Xeon（AVX512-VNNI）上，`laya-multilingual` 单题 **15.6 ms**、三题一次 44.8 ms，体积 1290 MB → 324 MB；`--precision fp32` 与上游 PyTorch **逐位一致**（最大概率偏差 0.00000）。

顺带记三个量化上的坑，都是实测：

* **动态量化会让结果依赖 batch。** fp32 ONNX 单条与批量差 `0.000e+00`，int8 动态差 **2.43**——激活 scale 在运行时按实际张量算，padding 一变就变。对一个卖校准概率的模型是硬伤，要可复现就固定 `batch=1` 或用 fp32。
* **别用 QUInt8。** 同 8 bit 同体积，但 x86 的 VNNI 只对有符号 int8 有快路径：实测 QUInt8 27.9 ms、QInt8 15.6 ms。（ARM 走 SDOT，不适用此条。）
* **保留嵌入表不量化没用。** 322M 里 196.6M 是 256k 词表的嵌入表，看着像精度大头，保留后精度没回来（91.0% / 51.5%），体积反而从 325 MB 涨到 915 MB。

#### 另一条路：本地起一个 Jev 兼容的 `/v1/systemone`

上面那张表是「换一个自己的模型」。还有一类项目不换 API——**在本机起一个官方协议的端点，官方 SDK 改个 `TYPESAFE_BASE_URL` 就切过去了**。按「概率是怎么来的」分成三种，差别比看上去大得多：

| 方案 | 概率从哪来 | 后端 | 代价 |
| :-- | :-- | :-- | :-- |
| [**githubnext/localjev**](https://github.com/githubnext/localjev) | **提示模型自己报** | 任意 OpenAI 兼容端点（默认 oMLX 上的 DiffusionGemma 26B-A4B-4bit） | 最好装，但绕回了生成+解析+重试 |
| [razorback16/openjev](https://github.com/razorback16/openjev) | **真从 logits 读** | 打了补丁的 vLLM | 概率是真的，但依赖未合入的 vLLM 扩展 |
| [ekzhang/openjev-sglang](https://github.com/ekzhang/openjev-sglang) | 真从 logits 读（prefill-only） | SGLang | 同上，装起来有门槛 |

**localjev 是 GitHub Next 出的**，TypeScript/Bun 写的一层**协议桥，自己不做推理**：把 state 和带类型的问题翻译成一个分类 prompt → 发给上游 LLM → 要它吐 JSON 概率标量/向量 → 校验、格式错就重试（`LOCALJEV_MALFORMED_RETRIES` 默认 2）→ 归一化 → 算出 choice、期望分、熵置信度 → 按 Jev 的响应格式返回。

它的 README 把取舍写得很坦白，值得原样引用：**wire-compatible, but not mathematically equivalent**——「概率是模型生成／自报的，不是直接从 logits 读的，上生产前请在你自己的负载上验证校准」。

所以要清楚自己换来了什么：**协议兼容，但 Jev 想消灭的那一圈全回来了**——逐 token 生成、解析 JSON、schema 校验、失败重试。延迟和成本是完整 LLM 的量级，不是 System One 的量级。它真正的价值是**在没有 Jev key 的机器上把代码跑通**，以及拿它的 bake-off 脚本横向比不同本地模型（仓库里有一份 M5 Max 上 1,200 请求的评测报告，跑了 AG News / BoolQ / SST-5，作者明确说是小样本筛选而非定论）。

想要真概率就得往下走一层：openjev 用 DiffusionGemma 的一步 structured read 直接拿 logprobs，但依赖 vLLM 未合入的 `diffusion_seed_canvas`、`diffusion_read_only` 等扩展。**准确和易装，目前只能二选一。**

> 顺带澄清一个容易混的点：[SemIf](https://github.com/TheoLeeCJ/SemIf) 曾用名也叫 `openjev`，和上面 razorback16 的 `openjev` **是两个不相干的项目**。

> **部署上有个坑能直接毁掉延迟优势**：默认 `max_loaded=1`，如果请求在不同语言间来回切，模型会**每个请求重建一次**——实测 CPU 上中位 7.4 秒、T4 上 10.3 秒。上生产务必预加载并放大 `max_loaded`，否则 33ms 会变成 10 秒。

### 坑清单

按踩到的概率排，前四条都是我这次真撞上的：

| 坑 | 说明 |
| :-- | :-- |
| **Vercel 必须绑信用卡** | 不绑卡任何请求都是 `403 customer_verification_required`，跟 key 对不对无关。绑完才给 $5 免费额度，**额度从你第一次请求开始起算** |
| **Gateway 上 `noul` 改名叫 `boolean`** | 官方 API 是 `{"type":"noul"}` 返回 `noul` 字段；Gateway 只认 `'boolean' \| 'choice' \| 'score'`，返回 `probability`。照官方文档抄过去直接报错 |
| **`criteria` 必填，而且三种类型形状不同** | Choice 要**对象**（`{"billing":"说明"}`），Score 要**数组**（`["低","中","高"]`），boolean 不要。Choice 写成 `options` / `choices` 都不认 |
| **jev 不能走 `/v1/chat/completions`** | 它是 evaluation 类型模型，走聊天端点会明确报错 `is an evaluation model, not a language model`。Gateway 的原生端点是 `POST /v1/evaluate` |
| **`ai` 包要 7.0.103 以上** | `experimental_evaluate` 是 7.0.103 才加的，7.0.102 及以前没有这个导出。或者直接用 `@ai-sdk/typesafe-ai` |
| **npm 上的 `typesafe-sdk` 不是官方包** | 那是个 0.0.0 的占位包，跟 TypeSafe 无关。官方 JS 是 `@typesafe-ai/sdk`；`pip install typesafe-sdk` 才是对的（PyPI 上是官方的） |
| **免费层有速率限制** | 实测连发十几次就会撞 `429 rate_limit_exceeded`（提示 upstream 高负载），退避重试即可。买了 credits 才进付费层放宽限制 |
| **一旦买了 credits 就没有月度免费额度了** | 官方原话：购买后账号转入付费层，monthly free credit 不再适用。只想白嫖就别充值 |
| **Spend Management 管不住 AI Gateway** | 文档明写暂停项目 *does not stop AI Gateway API key usage*。要限额得用 Gateway 自己的 [Budgets](https://vercel.com/docs/ai-gateway/observability-and-spend/budgets)，可以按 team / 项目 / 单个 key / 成员分别设 |
| **Auto top-up 记得保持关闭** | 默认就是关的，别手滑打开，否则余额见底会自动扣款续费 |
| **OpenRouter 还没真正上线** | 有模型页，但 2026-09-19 实测 `/api/v1/models` 返回的 446 个模型里没有 jev。别照着它写代码 |
| **Gateway 元数据里 `context_window` 写 32000** | 对应官方的「state + 最长问题 ≤ 32k」那一项，不是 64k 总量；另外 `max_tokens` 报 0，某些会校验这个字段的框架会被卡住 |

---

## ⚡ 上手

渠道怎么选、各自有什么坑，都在上一节 [体验渠道](#-体验渠道)。这一节只讲代码——以官方 Python SDK 为例，其他渠道换个客户端，问题的写法是一样的。

```bash
pip install typesafe-sdk        # 或 uv add typesafe-sdk
export TYPESAFE_API_KEY=sk-...  # SDK 自动读取
```

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()

response = client.system_one(
    state="你好，我的 Stripe 账号连了三天都连不上，再不行我就退订了。",
    questions={
        "department": Choice(
            instructions="这个工单该给哪个组",
            criteria={
                "billing":   "支付或订阅问题",
                "technical": "Bug 或集成问题",
                "sales":     "定价或账号咨询",
            },
        ),
        "frustration": Score(
            instructions="客户的不满程度",
            criteria=["平静陈述事实", "有情绪但还讲道理", "非常愤怒，措辞激烈"],
        ),
        "is_urgent": Noul(
            instructions="这条消息表达了紧急或时间压力",
        ),
    },
)
```

返回长这样。有两处值得一提：`output_tokens` 记了 48 但不计费；还有那个 `confidence: 0.596`，下面马上会用到。

```json
{
  "model": "jev-latest",
  "answers": {
    "department":  { "type": "choice", "choice": "billing", "confidence": 0.596 },
    "frustration": { "type": "score",  "score": 1.035,      "confidence": 0.842 },
    "is_urgent":   { "type": "noul",   "noul": 0.999 }
  },
  "usage": { "input_tokens": 312, "output_tokens": 48 }
}
```

回到那个 `confidence: 0.596`——这是官方文档自己的示例。0.596 其实是在说：**这一条不适合直接路由。** 原因也很直观：这条工单同时提到了扣款和没人理，本来就跨 billing 与 technical 两类，换成人也会犹豫。

我自己第一次用的时候就栽在这里——拿着 `choice` 直接执行，没看 `confidence`。这两个字段的分工是：`choice` 告诉你是什么，`confidence` 告诉你要不要动手。完整讲解见 [中文上手指南](docs/quickstart.md)。

```bash
npm install @typesafe-ai/sdk                           # 官方 JS/TS
claude plugin marketplace add typesafe-ai/skills       # Claude Code 技能包
npx skills add typesafe-ai/skills --skill typesafe-ai  # 其他 Agent
```

---

## 📐 规格与定价

后面判断「值不值得用」的时候，这几个数字会反复用到：

| 项 | 值 |
| :-- | :-- |
| 模型 | Jev 1.13 · `jev-1.13.0`，别名 `jev-latest` / `jev-preview` |
| 输入 | **$0.042 / MTok** |
| 输出 | **免费**（官方称 too cheap to meter） |
| 上下文 | 64k / 次请求，其中 state + 最长问题 ≤ 32k |
| Choice 候选上限 | 255 |
| 速率 | 250,000 token/秒 · 1,200 请求/分钟 |
| 模态 | 纯文本，不支持图像 / 音频 / 视频 |
| 端点 | `POST https://api.typesafe.ai/v1/systemone` |
| 延迟 | 70–500ms（官方数据） |

比起「快 N 倍」，具体场景的开销更能说明问题：官方 Doom demo 跑 10 次查询/秒约 **$7/小时**；browser-use 订一张机票全程 **7 秒 / $0.0039**。这个价格意味着可以对页面上每一个 DOM 元素都问一遍——真正改变做法的是这一点，而不是某个倍数。

<sub>来源：[Models 文档](https://docs.typesafe.ai/models) · [发布博文](https://typesafe.ai/blog/introducing-system-one-models-and-jev)</sub>

---

## 🧭 该用与不该用

没有哪个模型适合所有场景。跑 benchmark 之前先对照一下这张表，能省不少时间。

| 场景 | | 为什么 |
| :-- | :-- | :-- |
| 高频、重复、答案空间已知的判断 | 主场 | 一次调用几十题并行，便宜到每个 DOM 元素都能问一遍 |
| Agent 的每一步「选哪个元素 / 调哪个工具」 | 主场 | browser-use、mobile-jev 全在干这件事，把 LLM 从决策回路里摘出去 |
| LLM 的输入输出护栏 / 内容审核 | 推荐 | 阈值写在代码里，比让 LLM 判断自己稳定 |
| 无 embedding 的语义检索与重排序 | 推荐 | 逐条问 Noul 按概率排序，省掉一整套向量库 |
| 上下文剪枝 | 推荐 | fast-jev-compaction、winnow、yoshi 都是这个思路 |
| 开放式抽取（候选未知） | 要改写 | 先用正则出候选再让它选，见 [Cookbook](#-cookbook-与模式) |
| 低频调用（一天几十次） | 不值当 | 省下的钱抵不过多一个供应商 |
| 窄任务 + 有标注数据 | 先量一下 | 传统基线（正则 / TF-IDF）在某些任务上更准，见 [冷静看待](#-冷静看待) |
| 输出文字、代码、摘要 | 不会 | 这是设计，不是缺陷 |
| 多步推理、要解释理由 | 不合适 | 它只给概率，不给理由 |

---

## 📈 热门项目自动榜

这一段由脚本每天重抓重排，人工精选区不受影响。收录与去噪逻辑都在 [`collect_hot.py`](scripts/collect_hot.py)，发现误收可以补进 [`denylist.txt`](scripts/denylist.txt)。星数高只说明关注度高，不代表质量好，把它当作「大家在往哪个方向探索」的信号更合适。

<!-- HOT:START -->
> 🤖 由 [`scripts/collect_hot.py`](scripts/collect_hot.py) 每日自动抓取并排序，最后更新：**2026-09-26**（UTC）。收录规则：2026-09-10 之后创建、名称/描述/README 命中 Jev 生态关键词、Star ≥ 3，外加 [`typesafe-ai`](https://github.com/typesafe-ai) 官方组织全量。`🆕` = 本周新进榜，`▲` = 相比上次抓取的 Star 增量。

| # | 项目 | Star | 变化 | 语言 | 一句话 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | [**NandhaKishorM/laya**](https://github.com/NandhaKishorM/laya) `🆕` | ![](https://badgen.net/github/stars/NandhaKishorM/laya) | ▲ 1609 | Python | Non-autoregressive System 1 decision engine. Typed choice, score and yes/no decisions over any… |
| 2 | [**browser-use/jev-ultrafast**](https://github.com/browser-use/jev-ultrafast) | ![](https://badgen.net/github/stars/browser-use/jev-ultrafast) | ▲ 410 | Python | Fastest and cheapest web agent |
| 3 | [**jaredpalmer/kev**](https://github.com/jaredpalmer/kev) `🆕` | ![](https://badgen.net/github/stars/jaredpalmer/kev) | ▲ 270 | Python | Jev-like family of decision models built on top of Qwen3.5/3.8 you can train and run on your own |
| 4 | [**tamaratran/fast-jev-compaction**](https://github.com/tamaratran/fast-jev-compaction) | ![](https://badgen.net/github/stars/tamaratran/fast-jev-compaction) | ▲ 134 | TS | Claude Code plugin that replaces the compaction summary with Jev decisions: every tool call and… |
| 5 | [**jev-chat/jev-chat-jarvis**](https://github.com/jev-chat/jev-chat-jarvis) `🆕` | ![](https://badgen.net/github/stars/jev-chat/jev-chat-jarvis) | ▲ 427 | Kotlin | 装在手机上的对话副驾：在 QQ / X / 飞书里读懂对方、给出候选回复、一键填入输入框，发不发由你。非侵入，只读屏幕，不 hook 不改包。 |
| 6 | [**mizorewww/laya-mlx**](https://github.com/mizorewww/laya-mlx) `🆕` | ![](https://badgen.net/github/stars/mizorewww/laya-mlx) | ▲ 116 | Python | Native MLX runtime for Laya typed decision models — 7–14 ms short decisions on M3 Max. No text… |
| 7 | [**TheoLeeCJ/SemIf-OpenJev**](https://github.com/TheoLeeCJ/SemIf-OpenJev) `🆕` | ![](https://badgen.net/github/stars/TheoLeeCJ/SemIf-OpenJev) | ▲ 82 | Python | Semantic ifs from open models, on a 3090 at home. Independent; not affiliated with Jev or TypeS… |
| 8 | [**jarrodwatts/jev-trader**](https://github.com/jarrodwatts/jev-trader) | ![](https://badgen.net/github/stars/jarrodwatts/jev-trader) | ▲ 56 | TS | One AI trade decision every Monad block. Jev on Kuru MON-USDC. |
| 9 | [**TianyuCodings/NanoJev**](https://github.com/TianyuCodings/NanoJev) | ![](https://badgen.net/github/stars/TianyuCodings/NanoJev) | ▲ 49 | Python | A nano replica of Jev: parallel decisions, dynamic candidates, and an end-to-end training pipel… |
| 10 | [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) `官方` | ![](https://badgen.net/github/stars/typesafe-ai/skills) | ▲ 49 | — | Agent skills for building with TypeSafe's System One API |
| 11 | [**yibie/awesome-jev**](https://github.com/yibie/awesome-jev) | ![](https://badgen.net/github/stars/yibie/awesome-jev) | ▲ 63 | Python | A curated list of public projects, integrations, and discussions built on Jev — TypeSafe AI's S… |
| 12 | [**vinnylarouge/jevlike**](https://github.com/vinnylarouge/jevlike) | ![](https://badgen.net/github/stars/vinnylarouge/jevlike) | ▲ 10 | Python | — |
| 13 | [**awlevin/typesafe-computer-use**](https://github.com/awlevin/typesafe-computer-use) | ![](https://badgen.net/github/stars/awlevin/typesafe-computer-use) | ▲ 22 | Python | Computer use for about $0.0002 a step: OCR the screen, classify the next action with TypeSafe,… |
| 14 | [**heyjunpenn/awesome-jev**](https://github.com/heyjunpenn/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/heyjunpenn/awesome-jev) | ▲ 25 | Astro | A verified, community-maintained catalog of 916 open-source projects built with Jev. |
| 15 | [**kerpopule/hermes-jev-skills**](https://github.com/kerpopule/hermes-jev-skills) `🆕` | ![](https://badgen.net/github/stars/kerpopule/hermes-jev-skills) | ▲ 44 | Python | Jev-powered model routing, memory, compaction, skill selection, computer and browser use for He… |
| 16 | [**githubnext/localjev**](https://github.com/githubnext/localjev) `🆕` | ![](https://badgen.net/github/stars/githubnext/localjev) | ▲ 18 | TS | — |
| 17 | [**v-modal/awesome-jev-tools**](https://github.com/v-modal/awesome-jev-tools) `🆕` | ![](https://badgen.net/github/stars/v-modal/awesome-jev-tools) | ▲ 7 | — | A curated list of tools built for Jev — TypeSafe AI's System One model for typed decisions. |
| 18 | [**nokia-applied-research/AnyJev**](https://github.com/nokia-applied-research/AnyJev) `🆕` | ![](https://badgen.net/github/stars/nokia-applied-research/AnyJev) | ▲ 198 | Python | Turn any LLM into a Jev-style decision model: typed decisions, real probabilities, no training.… |
| 19 | [**wfzyx/von**](https://github.com/wfzyx/von) `🆕` | ![](https://badgen.net/github/stars/wfzyx/von) | ▲ 43 | Python | The open-source System One decision model. Sub-15ms, non-autoregressive, local drop-in alternat… |
| 20 | [**anishfn/shapeshift**](https://github.com/anishfn/shapeshift) `🆕` | ![](https://badgen.net/github/stars/anishfn/shapeshift) | ▲ 55 | TS | An input that becomes what you mean: one text box that morphs into the right UI as you type. Po… |
| 21 | [**TypeLLM/TypeLLM**](https://github.com/TypeLLM/TypeLLM) `🆕` | ![](https://badgen.net/github/stars/TypeLLM/TypeLLM) | ▲ 581 | Python | TypeLLM: LLMs with type-safe generation |
| 22 | [**devagrawal09/jev-review**](https://github.com/devagrawal09/jev-review) | ![](https://badgen.net/github/stars/devagrawal09/jev-review) | ▲ 13 | TS | A staged code-review workflow and local dashboard built with TypeSafe Jev. |
| 23 | [**Sac-Y/Jev-cu**](https://github.com/Sac-Y/Jev-cu) `🆕` | ![](https://badgen.net/github/stars/Sac-Y/Jev-cu) | ▲ 5 | JS | — |
| 24 | [**thruwire/foreman**](https://github.com/thruwire/foreman) | ![](https://badgen.net/github/stars/thruwire/foreman) | ▲ 14 | Python | Software factory foreman based on TypeSafe's Jev model |
| 25 | [**jev-chat/jev-chat-windows**](https://github.com/jev-chat/jev-chat-windows) `🆕` | ![](https://badgen.net/github/stars/jev-chat/jev-chat-windows) | ▲ 27 | Python | JevChat-Windows：聊天窗口旁挂的回复辅助。窗口截图 + 本地离线 OCR 读对方消息 → Jev 判断意图 → 3 条候选一键填入，发送永远手动 |
| 26 | [**taeold/djev-run**](https://github.com/taeold/djev-run) `🆕` | ![](https://badgen.net/github/stars/taeold/djev-run) | ▲ 22 | HTML | — |
| 27 | [**rmalde/minecraft-agent**](https://github.com/rmalde/minecraft-agent) `🆕` | ![](https://badgen.net/github/stars/rmalde/minecraft-agent) | ▲ 5 | JS | Astra planner and JEV controller for Minecraft, with native recording, tested routes, and run v… |
| 28 | [**featherless-ai/simple-jev**](https://github.com/featherless-ai/simple-jev) `🆕` | ![](https://badgen.net/github/stars/featherless-ai/simple-jev) | ▲ 12 | Python | Turn any open model into a classifier/jev endpoint |
| 29 | [**logicrw/awesome-jev-projects**](https://github.com/logicrw/awesome-jev-projects) `🆕` | ![](https://badgen.net/github/stars/logicrw/awesome-jev-projects) | ▲ 31 | JS | Awesome Jev: source-backed open-source ecosystem radar, plain-language project discovery, and a… |
| 30 | [**wy-coliney/jev-browser-use**](https://github.com/wy-coliney/jev-browser-use) `🆕` | ![](https://badgen.net/github/stars/wy-coliney/jev-browser-use) | ▲ 49 | JS | 5–10x faster browser operations: Jev clicks, Codex thinks and verifies. Built at EZCollegeApp. |
| 31 | [**AbdelStark/awesome-typesafe-jev**](https://github.com/AbdelStark/awesome-typesafe-jev) `🆕` | ![](https://badgen.net/github/stars/AbdelStark/awesome-typesafe-jev) | ▲ 9 | HTML | Awesome Jev: a source-backed field guide to TypeSafe's System One model, with SDKs, live demos,… |
| 32 | [**Rizzo-AI-Academy/rizzo-flow**](https://github.com/Rizzo-AI-Academy/rizzo-flow) `🆕` | ![](https://badgen.net/github/stars/Rizzo-AI-Academy/rizzo-flow) | ▲ 73 | Python | The open, local take on Jev: typed decisions from an LLM, without generating a single token |
| 33 | [**wuyoscar/jev-skill**](https://github.com/wuyoscar/jev-skill) `🆕` | ![](https://badgen.net/github/stars/wuyoscar/jev-skill) | ▲ 11 | Python | An awesome collection of Jev use cases, workflows, and agent skills. |
| 34 | [**receptron/laya**](https://github.com/receptron/laya) `🆕` | ![](https://badgen.net/github/stars/receptron/laya) | ▲ 52 | TS | Run Laya, the open-source Jev-compatible System-1 decision model, from Node.js / TypeScript via… |
| 35 | [**AnotiaWang/awesome-jev**](https://github.com/AnotiaWang/awesome-jev) | ![](https://badgen.net/github/stars/AnotiaWang/awesome-jev) | ▲ 105 | — | A curated list of awesome Jev / TypeSafe System One applications, libraries, and resources. |
| 36 | [**superagents-lab/jev-search**](https://github.com/superagents-lab/jev-search) | ![](https://badgen.net/github/stars/superagents-lab/jev-search) | ▲ 8 | TS | Search the web with TypeSafe's Jev: source selection, query understanding and relevance ranking… |
| 37 | [**jerryjliu/docjev**](https://github.com/jerryjliu/docjev) `🆕` | ![](https://badgen.net/github/stars/jerryjliu/docjev) | ▲ 18 | Python | A very fast document classifier/splitter using Jev |
| 38 | [**kyotofin/tax-doc-classifier**](https://github.com/kyotofin/tax-doc-classifier) `🆕` | ![](https://badgen.net/github/stars/kyotofin/tax-doc-classifier) | ▲ 11 | TS | Tax document page classifier built on Jev decisions. 100% strict accuracy across 261 IRS forms,… |
| 39 | [**razorback16/openjev**](https://github.com/razorback16/openjev) `🆕` | ![](https://badgen.net/github/stars/razorback16/openjev) | ▲ 26 | Python | Open, Jev-compatible System One decision server on DiffusionGemma |
| 40 | [**Mapika/decider**](https://github.com/Mapika/decider) | ![](https://badgen.net/github/stars/Mapika/decider) | ▲ 72 | Python | A family of System One-style models fine-tuned from Qwen3.5, designed for one-pass typed decisi… |
| 41 | [**gargpratyush/jev-router**](https://github.com/gargpratyush/jev-router) | ![](https://badgen.net/github/stars/gargpratyush/jev-router) | ▲ 21 | JS | Route to the cheapest model in claude code for your task using jev-router |
| 42 | [**cobanov/awesome-jev**](https://github.com/cobanov/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/cobanov/awesome-jev) | ▲ 12 | — | A curated, source-backed list of projects built with Jev, TypeSafe AI's System One model for ty… |
| 43 | [**jev-chat/jev-chat-jarvis-mac**](https://github.com/jev-chat/jev-chat-jarvis-mac) `🆕` | ![](https://badgen.net/github/stars/jev-chat/jev-chat-jarvis-mac) | ▲ 39 | Python | 聊天悬浮窗助手（macOS）：屏幕感知 + 本地小模型判断意图与风险，按话术生成回复候选。纯只读。 |
| 44 | [**droidrun/mobile-jev**](https://github.com/droidrun/mobile-jev) | ![](https://badgen.net/github/stars/droidrun/mobile-jev) | ▲ 10 | JS | — |
| 45 | [**OmniJev/awesome-jev-gallery**](https://github.com/OmniJev/awesome-jev-gallery) `🆕` | ![](https://badgen.net/github/stars/OmniJev/awesome-jev-gallery) | ▲ 70 | JS | Papers, open reproductions and independent evaluations behind System One models and Jev. |
| 46 | [**fhshaik/typesafe-mario**](https://github.com/fhshaik/typesafe-mario) | ![](https://badgen.net/github/stars/fhshaik/typesafe-mario) | ▲ 7 | Python | A TypeSafe/Jev agent that plays Super Mario Bros. from structured emulator state. |
| 47 | [**kydlikebtc/awesome-jev**](https://github.com/kydlikebtc/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/kydlikebtc/awesome-jev) | ▲ 99 | Python | 1207 public resources for Jev, TypeSafe AI's System One decision model, indexed by decision pat… |
| 48 | [**dabit3/jev-experiments**](https://github.com/dabit3/jev-experiments) | ![](https://badgen.net/github/stars/dabit3/jev-experiments) | ▲ 2 | TS | — |
| 49 | [**realZachi/pg-jev**](https://github.com/realZachi/pg-jev) | ![](https://badgen.net/github/stars/realZachi/pg-jev) | ▲ 18 | Shell | Ask your Postgres tables questions in plain language. A PostgreSQL extension powered by TypeSaf… |
| 50 | [**jkudish/jev-mcp**](https://github.com/jkudish/jev-mcp) | ![](https://badgen.net/github/stars/jkudish/jev-mcp) | ▲ 25 | JS | Fast, cheap, typed judgments from TypeSafe's Jev model, as MCP tools. |
| 51 | [**Yinsongxu/LLM2Jev**](https://github.com/Yinsongxu/LLM2Jev) `🆕` | ![](https://badgen.net/github/stars/Yinsongxu/LLM2Jev) | ▲ 17 | Python | Turn local language models into Jev-style structured decision models. Get results from text and… |
| 52 | [**Zefan-Cai/Open-Jev**](https://github.com/Zefan-Cai/Open-Jev) `🆕` | ![](https://badgen.net/github/stars/Zefan-Cai/Open-Jev) | ▲ 16 | Python | — |
| 53 | [**ekzhang/openjev-sglang**](https://github.com/ekzhang/openjev-sglang) | ![](https://badgen.net/github/stars/ekzhang/openjev-sglang) | ▲ 5 | Python | Jev-compatible API endpoint based on open models (prefill-only) |
| 54 | [**itsmostafa/system-one-connector**](https://github.com/itsmostafa/system-one-connector) `🆕` | ![](https://badgen.net/github/stars/itsmostafa/system-one-connector) | — | Go | System One MCP connector to evaluate anything fast and cheap. Give your AI agent direct access… |
| 55 | [**Alex314618-create/JevRev**](https://github.com/Alex314618-create/JevRev) `🆕` | ![](https://badgen.net/github/stars/Alex314618-create/JevRev) | — | TS | An LLM + Jev workflow that changes EVERYTHING. Boost your vertebrate brain with a spine inside. |
| 56 | [**malevrigns/agent-jev**](https://github.com/malevrigns/agent-jev) `🆕` | ![](https://badgen.net/github/stars/malevrigns/agent-jev) | ▲ 11 | Python | AgentJev-0.6B - a fast 'System One' decision model for AI Agents: feed it any unstructured stat… |
| 57 | [**moritzkremb/jev-voice-browser**](https://github.com/moritzkremb/jev-voice-browser) `🆕` | ![](https://badgen.net/github/stars/moritzkremb/jev-voice-browser) | ▲ 19 | JS | Control a real browser by voice. Jev (TypeSafe System One) decides intent + target in ~300 ms p… |
| 58 | [**typesafe-ai/system-one-adapter-python**](https://github.com/typesafe-ai/system-one-adapter-python) `官方` | ![](https://badgen.net/github/stars/typesafe-ai/system-one-adapter-python) | ▲ 6 | Python | Drop-in TypeSafeClient replacement backed by LLM APIs |
| 59 | [**sutro-sh/jev-align**](https://github.com/sutro-sh/jev-align) `🆕` | ![](https://badgen.net/github/stars/sutro-sh/jev-align) | ▲ 1 | Python | Build calibrated AI Functions from human feedback using Jev and GEPA. |
| 60 | [**Heman10x-NGU/openJev-verdict-2.0**](https://github.com/Heman10x-NGU/openJev-verdict-2.0) `🆕` | ![](https://badgen.net/github/stars/Heman10x-NGU/openJev-verdict-2.0) | ▲ 1 | Python | Calibrated 151M Non-Autoregressive Decision Engine beating TypeSafe Jev & Laya on LocalLLaMA/ty… |
<!-- HOT:END -->

---

## 🧰 SDK 与客户端

多数情况下官方那两个 SDK 就够用。社区版本主要补官方还没覆盖的语言，质量参差不齐，接入前翻一下源码比较稳妥。

### 官方

| 项目 | Star | 安装 | 说明 |
| :-- | :-- | :-- | :-- |
| [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) | ![](https://badgen.net/github/stars/typesafe-ai/skills) | `claude plugin install typesafe@typesafe-ai` | 官方 Agent 技能包：原语、模式、怎么组织 evaluation |
| [**typesafe-ai/system-one-adapter-python**](https://github.com/typesafe-ai/system-one-adapter-python) | ![](https://badgen.net/github/stars/typesafe-ai/system-one-adapter-python) | `pip install system-one-adapter` | 官方出的 `TypeSafeClient` 替身，后端走普通 LLM API。**没拿到 waitlist 也能先写代码**，还能用同一套问题横向对比 Jev 与聊天模型 |
| [**typesafe-ai/typesafe-sdk-js**](https://github.com/typesafe-ai/typesafe-sdk-js) | ![](https://badgen.net/github/stars/typesafe-ai/typesafe-sdk-js) | `npm i @typesafe-ai/sdk` | 官方 TS/JS 客户端，类型定义完整 |
| [**typesafe-ai/typesafe-sdk-python**](https://github.com/typesafe-ai/typesafe-sdk-python) | ![](https://badgen.net/github/stars/typesafe-ai/typesafe-sdk-python) | `pip install typesafe-sdk` | 官方 Python 客户端，同步/异步双版本，自带重试 |
| [Vercel AI SDK provider](https://ai-sdk.dev/providers/ai-sdk-providers/typesafe-ai) | — | `npm i @ai-sdk/typesafe-ai` | `experimental_evaluate` + `typeSafeAi.evaluationModel('jev-latest')` |

### 社区

| 语言 | 项目 | Star | 说明 |
| :-- | :-- | :-- | :-- |
| TypeScript | [**pithings/advocaat**](https://github.com/pithings/advocaat) | ![](https://badgen.net/github/stars/pithings/advocaat) | 小而美的 TS 客户端，给三原语打了 tagged helper |
| Erlang/OTP | [**dannote/jev**](https://github.com/dannote/jev) | ![](https://badgen.net/github/stars/dannote/jev) | 从 GenServer 回复 Jev，直接模式匹配答案 |
| Ruby | [**kieranklaassen/ruby_llm-typesafe**](https://github.com/kieranklaassen/ruby_llm-typesafe) | ![](https://badgen.net/github/stars/kieranklaassen/ruby_llm-typesafe) | RubyLLM 2 的 TypeSafe provider，带离线模型元数据 |
| Shell | [**shiftynick/jev-axi**](https://github.com/shiftynick/jev-axi) | ![](https://badgen.net/github/stars/shiftynick/jev-axi) | 面向 Agent 的 CLI：pick / rate / check / rank / triage |
| Rust | [**Twister915/typesafe-ai**](https://github.com/Twister915/typesafe-ai) | ![](https://badgen.net/github/stars/Twister915/typesafe-ai) | 另一个 Rust 客户端，异步 + 阻塞传输、可观测重试 |
| .NET | [**saibimajdi/typesafeai-dotnet-sdk**](https://github.com/saibimajdi/typesafeai-dotnet-sdk) | ![](https://badgen.net/github/stars/saibimajdi/typesafeai-dotnet-sdk) | 类型化问题 + 带置信度的答案 |
| Elixir | [**nshkrdotcom/typesafe_sdk**](https://github.com/nshkrdotcom/typesafe_sdk) | ![](https://badgen.net/github/stars/nshkrdotcom/typesafe_sdk) | Hex 包，支持 `system_one` 与模型列表 |
| Ruby | [**joshmn/typesafe-sdk**](https://github.com/joshmn/typesafe-sdk) | ![](https://badgen.net/github/stars/joshmn/typesafe-sdk) | Ruby 3.1+ 客户端，线程安全连接池；无异步客户端 |
| Shell | [**y0usaf/typesafe-cli**](https://github.com/y0usaf/typesafe-cli) | ![](https://badgen.net/github/stars/y0usaf/typesafe-cli) | 命令行直接问 noul/choice/score，返回数字不返回废话 |
| Rust | [**gilljon/typesafe-ai-rs**](https://github.com/gilljon/typesafe-ai-rs) | ![](https://badgen.net/github/stars/gilljon/typesafe-ai-rs) | 独立的异步 / 阻塞 System One 客户端 |
| Go | [**Gaurav-Gosain/jev-go**](https://github.com/Gaurav-Gosain/jev-go) | ![](https://badgen.net/github/stars/Gaurav-Gosain/jev-go) | `go get github.com/Gaurav-Gosain/jev-go`，返回类型化判断与校准概率 |
| Scala/ZIO | [**jamesward/zio-typesafe-ai**](https://github.com/jamesward/zio-typesafe-ai) | ![](https://badgen.net/github/stars/jamesward/zio-typesafe-ai) | ZIO 客户端，带 noul/choice/score 小 DSL |
| Laravel | [**Butochnikov/laravel-typesafe-jev**](https://github.com/Butochnikov/laravel-typesafe-jev) | ![](https://badgen.net/github/stars/Butochnikov/laravel-typesafe-jev) | Laravel 12/13 集成：Facade、scoped DI、recording fake |
| Rails | [**GenieRobot/typesafe-ai-rails**](https://github.com/GenieRobot/typesafe-ai-rails) | ![](https://badgen.net/github/stars/GenieRobot/typesafe-ai-rails) | Rails 集成：配置、用量/成本遥测、可选置信度策略 |
| Python | [**AboveColin/jevclient**](https://github.com/AboveColin/jevclient) | ![](https://badgen.net/github/stars/AboveColin/jevclient) | 非官方异步 Python 客户端 `pip install jevclient` |
| PHP | [**Butochnikov/typesafe-sdk-php**](https://github.com/Butochnikov/typesafe-sdk-php) | ![](https://badgen.net/github/stars/Butochnikov/typesafe-sdk-php) | 类型化 DTO、Promise 与异常 |
| Rust | [**AbdelStark/s1-rs**](https://github.com/AbdelStark/s1-rs) | ![](https://badgen.net/github/stars/AbdelStark/s1-rs) | derive 宏层：Choice/Score/Noul、类型化问题集、置信度门控、无网络测试 |

> **包名容易看错**：PyPI 上要装的是 `typesafe-sdk`。[`typesafe-ai`](https://pypi.org/project/typesafe-ai/) 是社区注册的占位包，用来挡蹭名字的恶意包，本身不是官方 SDK。

---

## 🛠 应用

这些项目已经把 Jev 放进了真实的循环里。整份列表我自己读得最久的就是这一栏——别人踩过的坑，可以直接绕开。

| 项目 | Star | 说明 |
| :-- | :-- | :-- |
| [**browser-use/jev-ultrafast**](https://github.com/browser-use/jev-ultrafast) | ![](https://badgen.net/github/stars/browser-use/jev-ultrafast) | 全生态第一爆款。Browser Use 官方出品的浏览器 Agent：一次请求里让 Jev 同时选出「做什么操作」和「操作哪个 DOM 元素」，只有真要打字时才叫小模型。Google Flights 苏黎世→伦敦订票 **7 秒 / $0.0039**。附库、本地 inspector 与测时 |
| [**OpenByteInc/QuantDinger**](https://github.com/OpenByteInc/QuantDinger) | ![](https://badgen.net/github/stars/OpenByteInc/QuantDinger) | 开源交易 OS（加密 / 股票 / 外汇，含回测与实盘）：下单前的决策网关从 LLM 换成 Jev，走 `/v1/systemone`，没配 key 就回退 LLM。Jev 在这里是可选组件，但接得完整，文档里连超时和降级路径都写了 |
| [**tamaratran/fast-jev-compaction**](https://github.com/tamaratran/fast-jev-compaction) | ![](https://badgen.net/github/stars/tamaratran/fast-jev-compaction) | Claude Code 插件：把上下文压缩的「总结」换成 Jev 判断——每次工具调用和结果都打分，决定留不留。**上下文工程的新范式** |
| [**jarrodwatts/jev-trader**](https://github.com/jarrodwatts/jev-trader) | ![](https://badgen.net/github/stars/jarrodwatts/jev-trader) | 每个 Monad 区块对 Kuru 的 MON-USDC 做一次买卖决策。在线：[jev-trader.vercel.app](https://jev-trader.vercel.app/) |
| [**awlevin/typesafe-computer-use**](https://github.com/awlevin/typesafe-computer-use) | ![](https://badgen.net/github/stars/awlevin/typesafe-computer-use) | macOS computer-use：OCR 屏幕 → Jev 分类下一步动作 → 点击。约 **$0.0002/步** |
| [**milind-soni/tiptour-macos**](https://github.com/milind-soni/tiptour-macos) | ![](https://badgen.net/github/stars/milind-soni/tiptour-macos) | macOS 本地 computer use：CoreML + OCR 在本机认出按钮和文字，Jev 只从这份控件清单里选点哪一个。截图不出本机（识别出的文字仍要发给 Jev），12 步上限，作者报单步约 90ms。要写字得切到 Gemini 模式——Jev 不生成文本 |
| [**thruwire/foreman**](https://github.com/thruwire/foreman) | ![](https://badgen.net/github/stars/thruwire/foreman) | 软件工厂循环：Codex 负责写，Jev 独立判断「做完没 / 测试够不够 / 要不要叫人」。把「谁来验收」这件事从 LLM 手里拿走 |
| [**devagrawal09/jev-review**](https://github.com/devagrawal09/jev-review) | ![](https://badgen.net/github/stars/devagrawal09/jev-review) | 分阶段代码审查工作流 + 本地 dashboard，由一串聚焦的 Jev 调用驱动 |
| [**mrmps/classifier-dev**](https://github.com/mrmps/classifier-dev) | ![](https://badgen.net/github/stars/mrmps/classifier-dev) | 零样本文本分类的公开 HTTP 服务（[classifier.dev](https://classifier.dev)），一个 Cloudflare Worker，免 key 免注册，`curl classifier.dev/spam,not+spam/...` 就能用。**fast 档直接是 Jev**（API 返回 `model: jev-1.13.0`），smart 档把 Jev 置信度低于 0.7 的题再交给推理模型复问——典型的置信度门控级联。JevBench 因此把它列为「跑别人模型的服务」，只登记不排名 |
| [**droidrun/mobile-jev**](https://github.com/droidrun/mobile-jev) | ![](https://badgen.net/github/stars/droidrun/mobile-jev) | Android Agent，每次点击由 Jev 决定。打开 Uber、旧金山机场→金门大桥，**21 秒 / 9 步**到支付页，**不需要 ADB** |
| [**shhivv/third-hand**](https://github.com/shhivv/third-hand) | ![](https://badgen.net/github/stars/shhivv/third-hand) | macOS 控制，**Jev 是唯一模型**，不挂任何 LLM。它「输入」的文字是从你那句指令里挑出来的，不是生成的——所以能填表单，写不了新句子。Apple Silicon 签名版可直接下载 |
| [**realZachi/pg-jev**](https://github.com/realZachi/pg-jev) | ![](https://badgen.net/github/stars/realZachi/pg-jev) | PostgreSQL 扩展：**直接在 SQL 里用自然语言问你的表**。`WHERE jev_noul(comment, '这是投诉') > 0.8` 这种写法 |
| [**kitze/skillbox**](https://github.com/kitze/skillbox) | ![](https://badgen.net/github/stars/kitze/skillbox) | 自托管、带版本的 Agent 技能库，MCP + 作用域客户端，可选用 Jev 做技能推荐 |
| [**lakeday-org/perch**](https://github.com/lakeday-org/perch) | ![](https://badgen.net/github/stars/lakeday-org/perch) | AST 驱动的语义 code lint |
| [**kitze/unclutter**](https://github.com/kitze/unclutter) | ![](https://badgen.net/github/stars/kitze/unclutter) | Chrome / Firefox 扩展：Jev 标出页面上不重要的元素，本地按页面模板记住，下次访问直接藏 |
| [**RomanSlack/jev-drone**](https://github.com/RomanSlack/jev-drone) | ![](https://badgen.net/github/stars/RomanSlack/jev-drone) | MuJoCo 四旋翼：控制与安全留在代码里，Jev 只做 2.5Hz 的战术判断 |
| [**mrnugget/jev-shell-history**](https://github.com/mrnugget/jev-shell-history) | ![](https://badgen.net/github/stars/mrnugget/jev-shell-history) | Thorsten Ball 写的 zsh 历史补全：最近 100 条去重历史当候选，Choice 选一条、Noul 再把关要不要显示，过期结果直接丢。fish 那种体验，但按语义排 |
| [**trungdq88/youtube-sponsor-detection**](https://github.com/trungdq88/youtube-sponsor-detection) | ![](https://badgen.net/github/stars/trungdq88/youtube-sponsor-detection) | 看 YouTube 时跳过口播广告：字幕分窗交给 Jev 判断哪几句是赞助，程序再把句子编号换算成时间轴。没字幕就先走语音转写 |
| [**ChetasLua/jevmeter**](https://github.com/ChetasLua/jevmeter) | ![](https://badgen.net/github/stars/ChetasLua/jevmeter) | 给任意视频挂实时 Jev 仪表：逐句打分，导出 16:9 成片 |
| [**realZachi/typesafe-adblock**](https://github.com/realZachi/typesafe-adblock) | ![](https://badgen.net/github/stars/realZachi/typesafe-adblock) | Chrome 扩展，逐个 DOM 元素问「这是广告吗」。规则库可以退休了 |
| [**jexp/neo4jev**](https://github.com/jexp/neo4jev) | ![](https://badgen.net/github/stars/jexp/neo4jev) | 让 Jev 在 Neo4j 图上导航：对邻居节点做分类，一步步走过去 |
| [**monteduro/killmyidea**](https://github.com/monteduro/killmyidea) | ![](https://badgen.net/github/stars/monteduro/killmyidea) | 描述你的创业点子，Jev 判决：毙掉、改改、还是发。玩法很毒但很有代表性 |
| [**yusukebe/hono-jev-router**](https://github.com/yusukebe/hono-jev-router) | ![](https://badgen.net/github/stars/yusukebe/hono-jev-router) | Hono 语义路由：不看路径看请求的意思——人来的返网页、Agent 来的返 Markdown。逐条判断路由描述取第一个过阈值的，普通路由优先。在线：[hono-jev-router.yusuke.run](https://hono-jev-router.yusuke.run) |
| [**AboveColin/HA-Jev**](https://github.com/AboveColin/HA-Jev) | ![](https://badgen.net/github/stars/AboveColin/HA-Jev) | Home Assistant 集成：把「关于家里状态的类型化提问」变成传感器与自动化动作，带每日 token 预算实体 |
| [**ellipsis-dev/blink**](https://github.com/ellipsis-dev/blink) | ![](https://badgen.net/github/stars/ellipsis-dev/blink) | 代码库语义搜索，Jev 驱动。不用向量库 |
| [**devanshbatham/commit-miner**](https://github.com/devanshbatham/commit-miner) | ![](https://badgen.net/github/stars/devanshbatham/commit-miner) | Rust CLI，给 commit diff 分类：修 bug、安全/CWE、变更类型，出 HTML/CSV 报告 |
| [**TarunTomar122/jev-askable-arm**](https://github.com/TarunTomar122/jev-askable-arm) | ![](https://badgen.net/github/stars/TarunTomar122/jev-askable-arm) | 仿真 Franka 机械臂：英文目标 zero-shot，Jev 把硬编码原语串起来 |
| [**reachjalil/jevlogs**](https://github.com/reachjalil/jevlogs) | ![](https://badgen.net/github/stars/reachjalil/jevlogs) | OpenTelemetry 日志分流：先让 Jev 打诊断价值和优先级，再决定要不要花钱叫 LLM |
| [**sufianetaouil/every**](https://github.com/sufianetaouil/every) | ![](https://badgen.net/github/stars/sufianetaouil/every) | 语义代码搜索 CLI：对每个函数问一个是非题，按 Noul 概率排序 |
| [**santos-sanz/jev-audio-beeper**](https://github.com/santos-sanz/jev-audio-beeper) | ![](https://badgen.net/github/stars/santos-sanz/jev-audio-beeper) | 低延迟脏话检测：Jev 判定后 ffmpeg 在约 466ms 内叠一声 beep |
| [**asfarsadewa/human-compiler**](https://github.com/asfarsadewa/human-compiler) | ![](https://badgen.net/github/stars/asfarsadewa/human-compiler) | 粘贴职场废话，Jev 给「被动攻击 / 紧急感 / 信息密度」打分，代码按 rustc 风格报诊断。在线：[human-compiler.asfarlab.fun](https://human-compiler.asfarlab.fun) |
| [**classifier.dev**](https://classifier.dev/) | — | **托管的零门槛分类 API，底座就是 Jev 1.13**（返回体里写着 `model: jev-1.13.0`）。不用注册、不用 key、不用绑卡，一条 curl 就能跑；批量一次 1,000 条，实测 20ms/条。代价是只剩分类一个原语、选项不能带描述、Jev 挂了会静默回退到 OpenRouter 上的 LLM 链（看 `modelsUsed` 字段才知道）。对比见 [体验渠道](#-体验渠道) |

---

## 🎮 Demo

发布 48 小时内涌现出来的小玩具。我是挑了两三个跑完之后，才真正对它的能力边界有了感觉——比读十页文档快得多。

| 项目 | Star / 链接 | 说明 |
| :-- | :-- | :-- |
| [**fhshaik/typesafe-mario**](https://github.com/fhshaik/typesafe-mario) | ![](https://badgen.net/github/stars/fhshaik/typesafe-mario) | 从结构化模拟器状态玩超级马里奥 |
| [**standardagents/jevpilot**](https://github.com/standardagents/jevpilot) | ![](https://badgen.net/github/stars/standardagents/jevpilot) | Three.js 驾驶模拟器 + Jev 自动驾驶，可直接玩 |
| [**openroboto-ai/jev-robot-control**](https://github.com/openroboto-ai/jev-robot-control) | ![](https://badgen.net/github/stars/openroboto-ai/jev-robot-control) | MuJoCo 里的 xArm7 把苹果放进盘子，三个模型同台：Jev 1.13 和 GPT-6 Astra 都放进去了，**成本 $0.019 对 $5.93**（墙钟 182s 对 707s），GPT-4.1 mini 撞到 160 周期上限没完成。单次试验，物理和关节控制留在代码里 |
| [**sorrycc/typesafe-snake**](https://github.com/sorrycc/typesafe-snake) | ![](https://badgen.net/github/stars/sorrycc/typesafe-snake) | 中文社区出品（[sorrycc](https://github.com/sorrycc)，umi 作者）：贪吃蛇每个 tick 一次 System One 选择，只在合法走法里选 |
| [**phyous/tsai-sc**](https://github.com/phyous/tsai-sc) | ![](https://badgen.net/github/stars/phyous/tsai-sc) | Jev 用键鼠操作原版星际争霸共享战役，带验证跑次与概率轨迹 |
| [**opaielsheikh/ai-elo-ranker**](https://github.com/opaielsheikh/ai-elo-ranker) | ![](https://badgen.net/github/stars/opaielsheikh/ai-elo-ranker) | 高速递归 AI Elo 锦标赛引擎，Jev + 瑞士轮匹配 |
| [**lukaske/jev-doom-agent**](https://github.com/lukaske/jev-doom-agent) | ![](https://badgen.net/github/stars/lukaske/jev-doom-agent) | 浏览器里的 Doom（Chocolate Doom WASM），空间状态 + 实时决策遥测。**官方发布 demo 的同源玩法，约 $7/小时** |
| [**lbotinelly/jev-little-airways**](https://github.com/lbotinelly/jev-little-airways) | ![](https://badgen.net/github/stars/lbotinelly/jev-little-airways) | 玩具群岛空管：每架飞机只看得见自己附近，Jev 判断备降 / 紧急 / 谁先落地，约 150ms |
| [**phureewat29/got-jev**](https://github.com/phureewat29/got-jev) | ![](https://badgen.net/github/stars/phureewat29/got-jev) | 权力的游戏角色扮演：故事模型写下一场，Jev 回答「他在哪、多危险、配什么音乐」 |
| [**mizchi/jev-gomoku**](https://github.com/mizchi/jev-gomoku) | ![](https://badgen.net/github/stars/mizchi/jev-gomoku) | MoonBit 客户端 + 两个 Jev 互相下五子棋，[配套文章](https://zenn.dev/mizchi/articles/jev-plays-gomoku)带耗时日志 |
| [**joshlarsen/jev-t-rex-runner**](https://github.com/joshlarsen/jev-t-rex-runner) | ![](https://badgen.net/github/stars/joshlarsen/jev-t-rex-runner) | Chrome 小恐龙由 Jev 来跳 |
| [**siroccomask/snake-jev**](https://github.com/siroccomask/snake-jev) | ![](https://badgen.net/github/stars/siroccomask/snake-jev) | 贪吃蛇，每局几百次类型化转向决策 |
| [Jev Tetris](https://jev-omega.vercel.app) | 🔗 在线 | Jev 按空洞、堆高、起伏选旋转和落点列 |
| [Jev Pac-Man](https://jev-pacman.ephraimduncan.com) | 🔗 在线 | 迷宫做成 JSON，每个路口由 Jev 选转向 |
| [Yes / No](https://yesno.coderai.dev) | 🔗 在线 | 免登录 Noul demo，问一句得到 yes/no/maybe |
| [TypeSafe Typewriter](https://typesafe-demo.val.run/) | 🔗 在线 | Val Town demo：打字时 16 条类型化判断实时更新 |
| [Hollow Creek](https://hollow-creek-sigma.vercel.app) | 🔗 在线 | 村庄 NPC 每个 tick **评判**你（在做什么、对你什么感觉），而不是和你聊天 |
| [Jev Guard](https://guard-jev.vercel.app) | 🔗 在线 | 评论审核 playground |
| [Jev Room](https://jev-room.moe136231.chatgpt.site) | 🔗 在线 | 一句话 → 六个房间设定，Jev 选，应用渲染 |
| [Ask Jev](https://askjev.ai) | 🔗 在线 | 随便问一句，看它怎么**判断**而不是怎么回答。感受「选择式 AI」最快的一个入口，但别把结果当知识——没有任何事实准确率评测 |
| [1kpapers](https://1kpapers.com) | 🔗 在线 | 1000+ 篇 AI 论文按 24 个主题归类：先让 LLM 把论文写成摘要，再让 Jev 给摘要贴标签。全量推理 $4.07 |
| [Probably](https://probably-lang.southpolesteve.workers.dev) | 🔗 在线 | 玩具语言：把「这封邮件急不急」这种语义判断直接写进 `if` 分支。Jev 判条件、解释器走流程、另一个模型写文字，三件事分得很干净 |
| [RISC-jeV](https://jev-riscv-production.up.railway.app) | 🔗 在线 | 拿 Jev 当逻辑门用：先判 AND / OR，再拼成 SERV 的 RISC-V 指令。看组合原理的，不是更快的算法 |
| [Jev Plays Pokémon](https://jev-plays-pokemon.standardagents.ai) | 🔗 在线 | 长程游戏：几千次决策累积推进剧情，拿到第一枚徽章。比剪辑好的片段更能看出长时间跑下来什么样 |
| [Jev City](https://01a0b7a9-5619-7ec6-a0d8-fb357ed42aa3.skydive.app/) | 🔗 在线 | 九个路口的交通灯沙盘：程序给路口状态，Jev 选放行方向 |
| [Jev 聊天小游戏](https://jev-chat.gigabitmillion-games.workers.dev/) | 🔗 在线 | 先判断你在说什么、语气怎样，游戏再决定怎么接话 |
| [Kernel 浏览器演示](https://jev-browser-use.val.run) | 🔗 在线 | 云端浏览器里的「观察 → 选择 → 操作」循环 |
| [Tester Army](https://tester.army/e2e) | 🔗 在线 | Web / 移动端 E2E 测试：Jev 参与每一步「下一步点哪」，断言仍要自己写 |
| [NoSugarForKids](https://nosugarforkids.com) | 🔗 在线 | 零食多维评分：每个维度问一题，网站汇总成表。评分问题本身没公开 |
| [官方智能家居 demo](https://docs.typesafe.ai/demos/smart-home) | 🔗 官方 | 演示**投机扇出**：一次问很多题，代码留下有用的，LLM 只管拆复合指令和闲聊 |

---

## 🤖 Agent 工具

把 Jev 接进 Claude Code、Codex、Cursor、MCP 的工具。这个方向的项目出得最快，原因也不难理解：编程 Agent 的每一步——路由到哪个模型、加载哪个技能、这条工具结果该不该留在上下文里——本质上都是选择题。

| 项目 | Star | 说明 |
| :-- | :-- | :-- |
| [**vercel/eve**](https://github.com/vercel/eve) | ![](https://badgen.net/github/stars/vercel/eve) | Vercel 的 Agent 框架，实验性 `autoModel` 默认用 Gateway 上的 `typesafe-ai/jev` 从白名单里挑语言模型 |
| [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) | ![](https://badgen.net/github/stars/typesafe-ai/skills) | **官方技能包**。Claude Code：`claude plugin marketplace add typesafe-ai/skills` → `claude plugin install typesafe@typesafe-ai`；其他 Agent：`npx skills add typesafe-ai/skills --skill typesafe-ai` |
| [**gargpratyush/jev-router**](https://github.com/gargpratyush/jev-router) | ![](https://badgen.net/github/stars/gargpratyush/jev-router) | Claude Code 与 Codex 的每轮路由：简单活走快档，难活走强档。`npm i -g jev-router` |
| [**jkudish/jev-mcp**](https://github.com/jkudish/jev-mcp) | ![](https://badgen.net/github/stars/jkudish/jev-mcp) | Node MCP，封装三条 cookbook：`jev_verify` 引文核验、`jev_screen` 注入护栏、`jev_find` 无 embedding 语义排序。`npx -y github:jkudish/jev-mcp` |
| [**NiazMorshed2007/jev-review**](https://github.com/NiazMorshed2007/jev-review) | ![](https://badgen.net/github/stars/NiazMorshed2007/jev-review) | 本地优先 MCP：Claude Code / Codex / Cursor / OpenCode 边写边拿结构化质量审查 |
| [**itsmostafa/typesafe-mcp**](https://github.com/itsmostafa/typesafe-mcp) | ![](https://badgen.net/github/stars/itsmostafa/typesafe-mcp) | Go 写的 CLI + 单二进制 MCP，适配 Claude Desktop / Claude Code / Codex |
| [**0xNatoshi/jev-codex-router**](https://github.com/0xNatoshi/jev-codex-router) | ![](https://badgen.net/github/stars/0xNatoshi/jev-codex-router) | Codex 每轮路由：Jev 选模型、思考深度和速度模式 |
| [**y0usaf/pi-jev**](https://github.com/y0usaf/pi-jev) | ![](https://badgen.net/github/stars/y0usaf/pi-jev) | Pi 扩展：影子模式工具调用门控、输出评判、类型化 `jev_ask` |
| [**dbreunig/building-with-jev-skill**](https://github.com/dbreunig/building-with-jev-skill) | ![](https://badgen.net/github/stars/dbreunig/building-with-jev-skill) | 一个专门教 Agent「怎么写调用 Jev 的程序」的 Skill |
| [**DevMortimer/pi-warden**](https://github.com/DevMortimer/pi-warden) | ![](https://badgen.net/github/stars/DevMortimer/pi-warden) | Pi 护栏：把判决当成 held tool result 而不是弹窗；对照项目规则文件检查写入 |
| [**Dicklesworthstone/skillranker**](https://github.com/Dicklesworthstone/skillranker) | ![](https://badgen.net/github/stars/Dicklesworthstone/skillranker) | Rust CLI，用实时会话上下文给 Agent 技能排序，只加载最该加载的那个 |
| [**supercorp-ai/supercov**](https://github.com/supercorp-ai/supercov) | ![](https://badgen.net/github/stars/supercorp-ai/supercov) | 给编程 Agent 的代码质量与测试覆盖率：Jev 给每个源文件打分，Agent 就知道先修什么 |
| [**Ying-Kai-Liao/jev-browser**](https://github.com/Ying-Kai-Liao/jev-browser) | ![](https://badgen.net/github/stars/Ying-Kai-Liao/jev-browser) | LLM 规划、Jev 在 Playwright 快照上决定每次点击（约 300ms/次）。含 MCP：`npx -y -p jev-browser jev-browser-mcp` |
| [**nidhi-singh02/agent-router**](https://github.com/nidhi-singh02/agent-router) | ![](https://badgen.net/github/stars/nidhi-singh02/agent-router) | CLI 按任务挑 Cursor / Claude Code / Codex / OpenCode + 模型档位，然后直接启动 |
| [**GhalebDweikat/winnow**](https://github.com/GhalebDweikat/winnow) | ![](https://badgen.net/github/stars/GhalebDweikat/winnow) | Claude Code 的校准上下文筛子：每个工具结果都被判一次再决定留不留 |
| [**shantanugoel/ask-jev-skill**](https://github.com/shantanugoel/ask-jev-skill) | ![](https://badgen.net/github/stars/shantanugoel/ask-jev-skill) | Hermes Skill：Agent 需要有界决策时去问 Jev |
| [**compozy/yoshi**](https://github.com/compozy/yoshi) | ![](https://badgen.net/github/stars/compozy/yoshi) | Claude Code / Codex 的上下文剪枝代理：Jev 判断哪些历史还需要，可量化 |
| [**jomatsu/pi-jev-auto-mode**](https://github.com/jomatsu/pi-jev-auto-mode) | ![](https://badgen.net/github/stars/jomatsu/pi-jev-auto-mode) | Pi 自动模式：Jev 按语义批准 `bash` / `write` / `edit`，判断不了就拒绝 |
| [**blakestone-x/jev-mcp**](https://github.com/blakestone-x/jev-mcp) | ![](https://badgen.net/github/stars/blakestone-x/jev-mcp) | Python MCP：classify / score / check / match / screen |
| [**sharziki/semdecide**](https://github.com/sharziki/semdecide) | ![](https://badgen.net/github/stars/sharziki/semdecide) | 给 Unix 管道和 CI 用的类型化语义决策，`cat log \| semdecide ...` |
| [**romaluev/jev-ego**](https://github.com/romaluev/jev-ego) | ![](https://badgen.net/github/stars/romaluev/jev-ego) | [ego lite](https://lite.ego.app/) 上的浏览器 Agent，observe / act / suggest / step CLI |
| [**AbdelStark/bicameral**](https://github.com/AbdelStark/bicameral) | ![](https://badgen.net/github/stars/AbdelStark/bicameral) | Pi 编程 harness：LLM 写代码，Jev 提供策略、循环检测与 review 的类型化反射。**明确不是沙箱** |
| [**samtay32/jev-system-architect**](https://github.com/samtay32/jev-system-architect) | ![](https://badgen.net/github/stars/samtay32/jev-system-architect) | 专找代码里脆弱的语义逻辑，改写成 Choice / Score / Noul 边界 |

---

## 🔬 复现与评测

这些是受 Jev 接口启发的独立工作，**都不是 TypeSafe 的模型**。想弄明白它在技术上怎么做到的，这些复现比官方博文讲得清楚。

### 开源复现

| 项目 | Star | 说明 |
| :-- | :-- | :-- |
| [**NandhaKishorM/laya**](https://github.com/NandhaKishorM/laya) | ![](https://badgen.net/github/stars/NandhaKishorM/laya) | 多语言非自回归 System 1 决策引擎：choice / score / noul 单次前向，33ms 一问、批量 7.2ms 一问（T4 自测），**覆盖 100+ 语言**，权重与 Colab demo 都在 Hugging Face 上。作者称这条路线早于 Jev，README 里与 Jev 的同数据集对比属作者自评 |
| [**TheoLeeCJ/SemIf**](https://github.com/TheoLeeCJ/SemIf) | ![](https://badgen.net/github/stars/TheoLeeCJ/SemIf) | 最受关注的复现（原名 `openjev`）：一张 RTX 3090 能不能跑 Jev 风格的东西？直接读选项 logits，不生成文本 |
| [**TianyuCodings/NanoJev**](https://github.com/TianyuCodings/NanoJev) | ![](https://badgen.net/github/stars/TianyuCodings/NanoJev) | nano 版 Jev：并行决策、动态候选、端到端训练流水线。**想搞懂训练的从这个读** |
| [**jaredpalmer/kev**](https://github.com/jaredpalmer/kev) | ![](https://badgen.net/github/stars/jaredpalmer/kev) | Qwen 上挂 LoRA + readout head（0.5B / 0.6B / 4B / 8B），block-causal mask 保证问题之间互相看不见，打包与分开请求的结果对到 4e-6。`POST /v1/systemone` 与官方 SDK 兼容，改 `base_url` 即可本地跑。冻结评测集域外分：kev-4b 0.76、kev-8b 0.77、真 Jev 0.86（作者自测） |
| [**bespokelabsai/nimble**](https://github.com/bespokelabsai/nimble) | ![](https://badgen.net/github/stars/bespokelabsai/nimble) | Bespoke Labs 的开源 Jev（Bespoke Nimble 9B）：**数据、训练、服务的完整配方**。Qwen3.5-9B 上只对答案 token 做 LoRA，数据靠「改一个事实让正确答案翻转」的对比式构造；324 条留出样本上对齐参考标签 90.1%（基座 66.4%、Jev 1.13.0 93.2%）。作者写明一天做完、**没有蒸馏 Jev** |
| [**vinnylarouge/jevlike**](https://github.com/vinnylarouge/jevlike) | ![](https://badgen.net/github/stars/vinnylarouge/jevlike) | 训练一个小的单次 scorer：上下文 + N 个文本选项 → 每个选项一个概率。含 Doom / 国际象棋视觉 demo 与 Wikispeedia 下一跳例子。**明确声明不是 TypeSafe 架构或 RLCD 的复现** |
| [**githubnext/localjev**](https://github.com/githubnext/localjev) | ![](https://badgen.net/github/stars/githubnext/localjev) | GitHub Next 出的**协议桥**（TypeScript/Bun）：本机起一个 Jev 兼容的 `/v1/systemone`，背后转成分类 prompt 发给任意 OpenAI 兼容端点（默认 oMLX 上的 DiffusionGemma）。**概率是模型自报的，不是读 logits**，作者自己写明「wire-compatible, but not mathematically equivalent」。附 AG News / BoolQ / SST-5 的多模型 bake-off 脚本。详见 [体验渠道](#-体验渠道) |
| [**featherless-ai/simple-jev**](https://github.com/featherless-ai/simple-jev) | ![](https://badgen.net/github/stars/featherless-ai/simple-jev) | 把 HF 上任意兼容开源模型变成 classifier / jev 端点：读每个问题的下一 token logits，由服务端拼出 JSON，模型不生成回答。有免登录公开 demo API（2k 上下文、2 RPS）和 playground，共用校验与评分逻辑放在纯 Python 的 `common/` 里 |
| [**Mapika/decider**](https://github.com/Mapika/decider) | ![](https://badgen.net/github/stars/Mapika/decider) | 基于 Qwen3.5-2B 微调：一次前向给出类型化决策和校准概率 |
| [**razorback16/openjev**](https://github.com/razorback16/openjev) | ![](https://badgen.net/github/stars/razorback16/openjev) | DiffusionGemma 上的 Jev 兼容决策服务，用一步 structured read **真从 logits 拿概率**；代价是依赖 vLLM 未合入的 `diffusion_seed_canvas`、`diffusion_read_only` 等扩展。注意与曾用名相同的 [SemIf](https://github.com/TheoLeeCJ/SemIf) 无关 |
| [**ekzhang/openjev-sglang**](https://github.com/ekzhang/openjev-sglang) | ![](https://badgen.net/github/stars/ekzhang/openjev-sglang) | 基于开源模型的 Jev 兼容 API 端点（prefill-only） |
| [**Heman10x-NGU/openJev-verdict-2.0**](https://github.com/Heman10x-NGU/openJev-verdict-2.0) | ![](https://badgen.net/github/stars/Heman10x-NGU/openJev-verdict-2.0) | 151M 的非自回归决策引擎（ModernBERT-base + GLiClass），单次判断约 20–25ms，还带一个 WebGPU 的浏览器端引擎。JevBench v1.4 引擎那一行排到第 4。注意仓库里 Verdict 2.0 的权重还是 Git LFS 指针，能下载的是 HF 上的 `rlcd-modernbert-151m` |
| [**hr98w/jev-visual**](https://github.com/hr98w/jev-visual) | ![](https://badgen.net/github/stars/hr98w/jev-visual) | Apple Silicon 上的 Jev 风格视觉推理教学实验：共享上下文、直接给候选打分 |
| [**logan-markewich/jeff**](https://github.com/logan-markewich/jeff) | ![](https://badgen.net/github/stars/logan-markewich/jeff) | GLiFormer 400M 撑起的自托管 Jev 替身：官方 `typesafe-sdk` 把 `TYPESAFE_BASE_URL` 指过来就能切，choice / score / noul 全支持。作者自己写明自托管便宜、但推理重的任务不如 Jev |
| [**kshetrajna12/reflex**](https://github.com/kshetrajna12/reflex) | ![](https://badgen.net/github/stars/kshetrajna12/reflex) | 小型开放决策模型：state + 类型化问题 → 校准概率 |
| [**bnsd55/jevmlx**](https://github.com/bnsd55/jevmlx) | ![](https://badgen.net/github/stars/bnsd55/jevmlx) | Apple Silicon 上给任意 MLX 模型做 Jev 式并行受限决策 |
| [**deepanwadhwa/OpenDecision**](https://github.com/deepanwadhwa/OpenDecision) | ![](https://badgen.net/github/stars/deepanwadhwa/OpenDecision) | ModernBERT-large 零样本 NLI 当决策引擎：把每个选项当作蕴含假设打分。除 Choice / Noul / Score 外多一个 **Relation**（支持 / 矛盾 / 未知 / 冲突），带文档取证检索，有 TypeSafe SDK 兼容端点和 ViZDoom demo |
| [**ikermoel/open-alternative-jev**](https://github.com/ikermoel/open-alternative-jev) | ![](https://badgen.net/github/stars/ikermoel/open-alternative-jev) | **是库不是服务**（`pip install open-alternative-jev`，import 名 `so1`），不提供 HTTP 端点。RACE-H 上 packed 模式 92.9% / 4.55 题每秒，比逐题前向的 1.66 快 2.7 倍，处理 token 数少 60%。HF Space 有免装 demo。JevBench 顺带测出一个坑：选项顺序反过来，同一模型的是非题准确率从 72% 掉到 21% |
| [**r-ms/mini-jev**](https://github.com/r-ms/mini-jev) | ![](https://badgen.net/github/stars/r-ms/mini-jev) | 冻结的 Qwen3-4B 上，Jev 式类型化决策接口长什么样 |
| [**zhengxuyu/litjev**](https://github.com/zhengxuyu/litjev) | ![](https://badgen.net/github/stars/zhengxuyu/litjev) | Jev 的复现：把任意 Qwen 模型变成快速决策模型，提供与 Jev 完全相同的 /v1/systemone schema（Choice、Score、Noul），不训练、不生成回答文本，附 MMLU-Pro 直答评测 |
| [**mithalouni/system-one-open**](https://github.com/mithalouni/system-one-open) | ![](https://badgen.net/github/stars/mithalouni/system-one-open) | Gemma 4 E2B（注意力 LoRA）+ Gemma 3 270M，在 Modal 上训练与部署：TypeSafe 公开评测的严格子集 76.7%（Jev 86.9%），27 个问题一次调用 97ms（H100）。八个复刻官方发布 demo 的页面都是实录 |
| [**rorshopping/jev-on-a-laptop**](https://github.com/rorshopping/jev-on-a-laptop) | ![](https://badgen.net/github/stars/rorshopping/jev-on-a-laptop) | 非官方研究：1.5B–8B 现成模型在 Apple Silicon 上做并行类型化决策 |
| [**sgoedecke/system-one**](https://github.com/sgoedecke/system-one) | ![](https://badgen.net/github/stars/sgoedecke/system-one) | 把任意 LLM 变成 System One 的最小实现：批量单 token 选择推理，与 `typesafe-sdk` 兼容。用 Qwen3-8B 复刻了 Doom 和 Wikiracing——同模型同提示下，比走普通 tool call **快 3.5 倍**（动作间隔 172ms vs 600ms） |
| [**OmniJev/PlayJev**](https://github.com/OmniJev/PlayJev) | ![](https://badgen.net/github/stars/OmniJev/PlayJev) | 多模态复现：微调 Qwen3.5-0.8B 看 448 px 游戏画面玩十个网页小游戏，一次前向读选项字母的概率出招，不生成文本；权重、两轮 DAgger 的复现脚本和浏览器 demo 都公开 |
| [**stephanj/parallelConstraintDecoding**](https://github.com/stephanj/parallelConstraintDecoding) | ![](https://badgen.net/github/stars/stephanj/parallelConstraintDecoding) | Java + Python 双版本的并行受限解码实现 |
| [**genai-craft/openvons**](https://github.com/genai-craft/openvons) | ![](https://badgen.net/github/stars/genai-craft/openvons) | 日文向 open-Jev：文本 / 图像 / 日语语音命令的概率判断层 |
| [**siliconkernel/vllm-jev-decison**](https://github.com/siliconkernel/vllm-jev-decison) | ![](https://badgen.net/github/stars/siliconkernel/vllm-jev-decison) | 给 vLLM 加「只分类」模式：有限 schema 候选打分 + 概率 |
| [**us/jev-local**](https://github.com/us/jev-local) | ![](https://badgen.net/github/stars/us/jev-local) | 一条命令起本地 `/v1/systemone`（Docker Compose + 冒烟测试），默认 Qwen3.5-9B 按每个选项的平均 logprob 打分，16GB Mac 可切 light 档的 Qwen2.5-3B。注意默认 scorer 是确定性桩、不带智能，要真模型得设 `JEVLOCAL_SCORER=hf` |
| [**kotoba-lang/typed-decisions**](https://github.com/kotoba-lang/typed-decisions) | ![](https://badgen.net/github/stars/kotoba-lang/typed-decisions) | 同一套 Jev 形状分别做在 ModernBERT 编码器和 LLaDA-MoE 扩散语言模型两个骨干上，**速度、准确率、校准、训练成本四项并排列出来**，适合对比两条技术路线 |
| [**NullPo-jp/PocketJev**](https://github.com/NullPo-jp/PocketJev) | ![](https://badgen.net/github/stars/NullPo-jp/PocketJev) | iPhone 端侧视觉判断：MLX + Qwen3-VL 选项 logits。相机 + 三选一，约 1 秒，不存照片 |
| [**Octalab-Inc/jqv**](https://github.com/Octalab-Inc/jqv) | ![](https://badgen.net/github/stars/Octalab-Inc/jqv) | 按 [Hume 那篇架构拆解](https://archerhume.com/posts/jevs-architecture-unmasked/) 在 stock Qwen3 上复刻 Jev 的推理结构：state 预填一次、每个问题在块状注意力掩码后走独立分支、直接读选项字母 logits，单一拟合温度做校准。**五种推理结构（generate / naive / kvcache / packed / shared）可在同一模型同一提示上切换对比**，适合拿来搞清楚这套结构各步分别值多少 |
| [**isHeSatoshi/smalljev**](https://github.com/isHeSatoshi/smalljev) | ![](https://badgen.net/github/stars/isHeSatoshi/smalljev) | MiniCPM5-2B-Base + LoRA 与原生决策头，Apache-2.0，主打「在你妈的手机上也能跑」。作者主动披露：训练配方对着 JevBench 的公开题型与来源族做过 hill-climbing，读它的自测分时要记得这点 |

### 独立评测

| 项目 | Star | 结论摘要 |
| :-- | :-- | :-- |
| [**vinilana/jev-eval-agent**](https://github.com/vinilana/jev-eval-agent) | ![](https://badgen.net/github/stars/vinilana/jev-eval-agent) | 早期 Jev 测试的公开评测 harness |
| [**nekuda-ai/WindTunnel**](https://github.com/nekuda-ai/WindTunnel) | ![](https://badgen.net/github/stars/nekuda-ai/WindTunnel) | WebMCP 基准，21 种配置横向比成功率 / 成本 / 耗时。Jev + Mercury 2.5 走 WebMCP **49/49 全解**、每次中位 $0.0011、3.2 秒，排第一；同一对模型改走 ultrafast DOM 控制只剩 25/49，单次更便宜（$0.0008）但成得少。少见的第三方横向基准，成本和时延都列了 |
| [**fstandhartinger/jevbench**](https://github.com/fstandhartinger/jevbench) | ![](https://badgen.net/github/stars/fstandhartinger/jevbench) | **目前覆盖面最广的第三方横评**：每个系统跑同样的 534 道冻结决策题（其中 220 道 hard 题由 Claude Opus 5 与 GPT-5.6 写、交叉评审，开跑前就冻结并哈希，一半留出不公开）。**榜上共 42 行结果、36 个不同项目**：**38 行进榜**（Jev 本体 1、开源复现 28 行对应 23 个项目、通用分类器 5、闭源决策 API 1、LLM 基线 3），外加 1 个名誉提名（classifier.dev，fast 档本身就是 Jev，排进去等于让 Jev 跟自己比）和 3 行只跑完一部分的。按智能 / 校准 / 速度 / 成本四轴各 25% 取**几何平均**——某一轴弱会把总分拽下去。v1.2.10 榜首 Jev 1.13.0 **75.4**，SemIf 74.7、djev 74.3 紧随其后。成本列的单位是**每千次决策**而不是每千 token，作者还专门发过一版修正把这个单位写清楚。局限写得很坦白：自托管与 demo 端点的延迟统一 ×2 + 0.15s 是**假设不是实测**。一人业余项目，与 TypeSafe 无关 |
| [**iammrduncan/typesafe-ai-benchmark**](https://github.com/iammrduncan/typesafe-ai-benchmark) | ![](https://badgen.net/github/stars/iammrduncan/typesafe-ai-benchmark) | 同一套 System One 问题，对比 Jev 与 Cerebras 上的 Qwen 3.8 27B |
| [**AbdelStark/jev-benchmarks**](https://github.com/AbdelStark/jev-benchmarks) | ![](https://badgen.net/github/stars/AbdelStark/jev-benchmarks) | 面向类型化决策模型的概率感知评测框架 |
| [**mahlernim/jev-korean-benchmark**](https://github.com/mahlernim/jev-korean-benchmark) | ![](https://badgen.net/github/stars/mahlernim/jev-korean-benchmark) | 韩语理解与医学文本的可复现 early-access 评测。**非英语场景的少有数据点** |
| [**anessbelbati/jev-rerank-bench**](https://github.com/anessbelbati/jev-rerank-bench) | ![](https://badgen.net/github/stars/anessbelbati/jev-rerank-bench) | 重排序对比：原始 provider 响应、打分代码、不确定区间、写明的局限 |
| [**Gaurav-Gosain/jev-sec-bench**](https://github.com/Gaurav-Gosain/jev-sec-bench) | ![](https://badgen.net/github/stars/Gaurav-Gosain/jev-sec-bench) | 公开语料盲测：提示注入与漏洞代码检测 |
| [**anisselbd/jev-phishing-bench**](https://github.com/anisselbd/jev-phishing-bench) | ![](https://badgen.net/github/stars/anisselbd/jev-phishing-bench) | 全生态最严谨的一份评测。2000 封钓鱼邮件对比 Claude Haiku 4.5：Jev 直接问「该不该点」只有 **62.6%** 准确率（Haiku 81.3%），但**同一次调用里拆成 5 个信号问题、再做逻辑回归就到 95.0%**。作者还在被质疑后补了三组对照（非 AI 正则基线 91.8%、样本切分、同样问题问 LLM）。延迟 239ms vs 687ms，成本 $0.038 vs $0.462 / 千封 |
| [**TokenTrim/jev-agent-failure-benchmark**](https://github.com/TokenTrim/jev-agent-failure-benchmark) | ![](https://badgen.net/github/stars/TokenTrim/jev-agent-failure-benchmark) | Who&When Pro（注入的 Agent 故障）：预测是谁 / 哪一步 / 哪类错误 |
| [**lexingtonhibiki/judgekit**](https://github.com/lexingtonhibiki/judgekit) | ![](https://badgen.net/github/stars/lexingtonhibiki/judgekit) | 中文场景首批公开评测：130 条人工标注样本（工单派单/情感/垃圾评论/紧急度），Jev 原生 decisions API 实测 97.7%（Wilson 95% CI [93.4–99.2]）@ ~890ms、¥0.105/千次，关键词规则基线 91.5%；0.7 置信度门控可捕获全部 3 个误判。局限：mini 集人工构建、LLM 对照组补测中；协议与逐条误判随仓库公开 |
| [**jmanhype/jev-dspy-lab**](https://github.com/jmanhype/jev-dspy-lab) | ![](https://badgen.net/github/stars/jmanhype/jev-dspy-lab) | DSPy 配套评测：录制并重放调用，测校准、选择性风险、置信度弃权、延迟、成本 |
| [**bitnovus/jev-spam-eval**](https://github.com/bitnovus/jev-spam-eval) | ![](https://badgen.net/github/stars/bitnovus/jev-spam-eval) | 18,514 封邮件：一段**写出来的**垃圾邮件定义拿到 **98.3%**，和用 ~14,800 条标注训练的 TF-IDF（98.4%）打平，两者平均后 **99.2%**。**最关键的是分布漂移**——换到 2026 年的新邮件，同一个问题仍有 97.3%，TF-IDF 掉到 72.5%。作者自己标注了「判据是看过错误样本后写的」这一 caveat |
| [**teyhouse/jev-secret-detection**](https://github.com/teyhouse/jev-secret-detection) | ![](https://badgen.net/github/stars/teyhouse/jev-secret-detection) | 测量 Jev 在代码片段里识别真实密钥凭证的能力 |

> **中文场景的公开评测，目前只有 judgekit 一份。** 130 条自建样本、作者自己标注了「mini 集人工构建、LLM 对照组还在补」，样本量撑不起结论，只能算一个起点。谁做过更大规模的中文分类、内容审核或客服工单对比测试，欢迎把数据发过来——结论对 Jev 有利还是不利都一样有价值。这仍是这份列表最缺的一块。

---

## 🍳 Cookbook 与模式

官方整理好的、可以直接照着改的工作流。下面四个核心模式是骨架，读完基本就知道系统该怎么搭了。

| 模式 | 一句话 |
| :-- | :-- |
| [置信度门控路由](https://docs.typesafe.ai/patterns/confidence-routing) | 答案告诉你是什么，置信度告诉你要不要动手。**最重要的一条** |
| [投机扇出](https://docs.typesafe.ai/patterns/fan-out) | 一次问很多题（含用不上的），在代码里筛。输出免费，多问不花钱 |
| [组合打分](https://docs.typesafe.ai/patterns/composite-scoring) | 原子分数由模型给，权重由你的代码掌控 |
| [意图路由](https://docs.typesafe.ai/patterns/intent-routing) | 先分类，再交给确定性逻辑、专用 LLM 或人 |

<details>
<summary><b>官方 Cookbook 全表</b>（可直接照抄的工作流）</summary>

| Cookbook | 解决什么问题 |
| :-- | :-- |
| [Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions) | 对同一份 state 批量提问，一次调用代替 N 次 |
| [Line-by-line search](https://docs.typesafe.ai/cookbooks/semantic_find) | 用 Choice 给几百行 id 打分，再用 Noul 检查「到底有没有答案」 |
| [Re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe) | BM25 出短名单，再对每个 query–候选对问一次 |
| [Guardrails for LLMs](https://docs.typesafe.ai/cookbooks/llm_guardrails) | 筛 LLM 的入站/出站消息，概率阈值写在代码里 |
| [Double-checking citations](https://docs.typesafe.ai/cookbooks/citation_check) | 判断引文上下文是否支撑主张，低置信度交人工 |
| [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) | 回答之前保留 / 标记 / 丢掉检索段落（矛盾、注入等） |
| [Function calling](https://docs.typesafe.ai/cookbooks/function_calling) | 把自然语言请求映射到普通类型化函数与闭集参数 |
| [Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion) | 给 Agent 技能目录排序，只细读前几名 |
| [Hierarchical classification](https://docs.typesafe.ai/cookbooks/hierarchical_classification) | 在深层分类树上用 Choice 概率做 beam search |
| [SDE cascade](https://docs.typesafe.ai/cookbooks/sde_cascade) | 两阶段结构化抽取级联（mini → 校验 → 推理） |
| [Date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook) | 先问文档里点名的日期部件，再在代码里解析校验 |
| [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) | 正则出候选，再让 Jev 选出目标片段。**开放式抽取的标准解法** |
| [Entity alignment](https://docs.typesafe.ai/cookbooks/entity_alignment) | 知识图谱实体对齐：合并 / 不链接 / 交给策展人 |
| [Autoresearch feature discovery](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery) | 把问题当成数值特征，喂给监督学习 |
| [Classification using confidence](https://docs.typesafe.ai/cookbooks/classification_using_confidence) | 置信度够才报细分类，否则上爬一层 |
| [Structure recovery](https://docs.typesafe.ai/cookbooks/autoformat) | 从丢掉格式的纯文本重建 Markdown |
| [Self-consistency: nouls](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook) / [choices](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook) | 不确定的走人工审核，同时保留原始数值 |

完整目录：[console cookbooks](https://console.typesafe.ai/docs/cookbooks) · [llms.txt](https://docs.typesafe.ai/llms.txt)

</details>

---

## 📰 文章

媒体报道大多基于同一份发布稿，挑一篇看背景就够。下面的「技术走读」信息量大得多。

### 媒体报道

| 文章 | 来源 |
| :-- | :-- |
| [TypeSafe AI debuts model for machines that plays Doom](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711) | The Register |
| [ChatGPT pioneer launches Jev model for programmatic logic](https://www.artificialintelligence-news.com/news/chatgpt-pioneer-launches-jev-model-for-programmatic-logic/) | AI News |
| [TypeSafe AI Emerges From Stealth With $40M in Funding](https://finance.yahoo.com/technology/ai/articles/typesafe-ai-emerges-stealth-40m-190000776.html) | Yahoo Finance |
| [Jev: TypeSafe's System One Model That Never Hallucinates](https://www.datacamp.com/blog/system-one-models-jev) | DataCamp |
| [TypeSafe JEV Explained: AI Decisions Without a Chatbot](https://www.theneuron.ai/explainer-articles/typesafe-jev-system-one-models-explained/) | The Neuron |
| [AINews: a "System One Model" that only decides/classifies/routes/scores](https://www.latent.space/p/ainews-jev-a-system-one-model-that) | Latent Space |

### 技术走读

| 文章 | 说明 |
| :-- | :-- |
| [A deep dive into Jev](https://flaviocopes.com/jev/) | Flavio Copes 的技术拆解，结构清楚 |
| [How to Use Jev: A practical guide](https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e) | DEV 上的实战指南 |
| [AI That Doesn't Talk: A Plain-English Guide](https://ziplyne.agency/blog/ai-that-doesnt-talk-typesafe-jev-guide) | 从 Playground 到裸 HTTP 到 agent skill 的全路径 |
| [TypeSafe Jev: the First Decision-Only Model Class](https://www.developersdigest.tech/blog/typesafe-jev-system-one-models-release-guide-2026) | 发布周技术综述：API、评测、adapter、skill |
| [Typed Decisions, Not Chat](https://warmersun.com/jev/) | **把官方主张和公开证据分开列**，本列表最推荐的一篇冷静文 |
| [Mini-Vibe Check: Jev Judged Everything I've Written in 0.7 Seconds](https://every.to/also-true-for-humans/mini-vibe-check-typesafe-s-jev-judged-everything-i-ve-written-in-0-7-seconds) | Every 的 Mike Taylor 用 Jev 扫自己的全部写作语料 |
| [Jev: The Language Model That Won't Talk](https://anthonymaio.substack.com/p/jev-the-language-model-that-wont) | Substack 长文评论 |
| [Is the 200x Faster Decision Model Too Good to Be True?](https://flowtivity.ai/blog/jev-typesafe-ai-decision-model/) | 质疑向，和上面那篇对着读 |
| [Generating game levels in real time with Jev](https://www.spritefusion.com/blog/generating-game-level-in-real-time-with-jev) | Sprite Fusion 的实战记录：跑酷地形实时生成，Jev 只选宽度、间隔、高度和地块类型，摆放交给游戏代码 |

| [Jev in the Wild: A Data-Driven Analysis of the Jev Model's Functionality, Applications and Ecosystem](https://arxiv.org/abs/2609.30216) | 首个基于 2,170 个公开 GitHub Jev 项目的应用生态综述与分析，记录早期快速增长、应用领域和决策用途分布；论文为 arXiv 预印本。 |

### 日文

| 文章 | 说明 |
| :-- | :-- |
| [TypeSafeのJevを正しく驚く、それってLLMでできませんか？](https://zenn.dev/nwn/articles/824026c76116e0) | Jev 是什么、不是什么，边界画得很准 |
| [jev 同士に五目並べで対戦させた](https://zenn.dev/mizchi/articles/jev-plays-gomoku) | mizchi 让两个 Jev 下五子棋，带源码和耗时日志 |

> 中文一手内容目前几乎是空白，[docs/](docs/) 就是为了补这一块。写了中文实践文章的话，欢迎提 PR 进来。

---

## 💬 社区

| 渠道 | 说明 |
| :-- | :-- |
| [Discord](https://discord.gg/typesafe) | TypeSafe 官方服务器，Builder demo 集中在 Show and Tell 频道 |
| [X @typesafeai](https://x.com/typesafeai) | 官方账号，[出 stealth 那条](https://x.com/typesafeai/status/2099944756931596454) |
| [LinkedIn](https://www.linkedin.com/company/typesafe-ai/) | 公司公告与招聘 |
| [Hacker News 发布讨论](https://news.ycombinator.com/item?id=49717558) | 1500+ 分，**评论区的质疑比正文更值得读** |
| [Vercel 上线公告](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway) | AI Gateway 接入公告 |
| [OpenRouter 模型页](https://openrouter.ai/typesafe/jev-1.13) | 价格、限流、provider 状态 |

**X 上值得关注的几条**（发布周传播量最大的）：

| 推文 | 看点 |
| :-- | :-- |
| [@typesafeai 出 stealth](https://x.com/typesafeai/status/2099944756931596454) | 官方发布原帖 |
| [@stevekrouse 的 Typewriter demo](https://x.com/stevekrouse/status/2100287368221659289) | Val Town 作者，16 条判断实时更新，直观演示「并行提问」 |
| [@thdxr](https://x.com/thdxr/status/2100288951978164647) | SST 作者的上手体感 |
| [@testingcatalog 的拆解](https://x.com/testingcatalog/status/2099968075861008781) | 把「不是 LLM」这件事讲清楚了 |
| [@iamMrDuncan 的对比视频](https://x.com/iamMrDuncan/status/2100467548298899918) | Jev vs Cerebras 上的 Qwen 3.8 27B |
| [@chetaslua 的 JEVMETER](https://x.com/chetaslua/status/2100473581251748216) | 实时视频打分仪表，视觉冲击最强的一条 |

### 其他 awesome 列表

| 列表 | Star | 说明 |
| :-- | :-- | :-- |
| [**yibie/awesome-jev**](https://github.com/yibie/awesome-jev) | ![](https://badgen.net/github/stars/yibie/awesome-jev) | 收录讨论与集成，含社区争论 |
| [**Anil-matcha/awesome-jev-by-typesafe**](https://github.com/Anil-matcha/awesome-jev-by-typesafe) | ![](https://badgen.net/github/stars/Anil-matcha/awesome-jev-by-typesafe) | 偏用例、模式、prompt 与起步代码 |
| [**AbdelStark/awesome-typesafe**](https://github.com/AbdelStark/awesome-typesafe) | ![](https://badgen.net/github/stars/AbdelStark/awesome-typesafe) | 覆盖整个 TypeSafe / System One，不只 Jev |
| [**AnotiaWang/awesome-jev**](https://github.com/AnotiaWang/awesome-jev) | ![](https://badgen.net/github/stars/AnotiaWang/awesome-jev) | 结构最完整的一份，本列表的选品参考了它，[有 README_zh](https://github.com/AnotiaWang/awesome-jev/blob/main/README_zh.md) |
| [**valentynkit/awesome-jev-typesafe**](https://github.com/valentynkit/awesome-jev-typesafe) | ![](https://badgen.net/github/stars/valentynkit/awesome-jev-typesafe) | CC0 协议，按「你会安装什么」分类，开头一节讲模型局限，通过 awesome-lint |
| [**hellogumbo/awesome-jev**](https://github.com/hellogumbo/awesome-jev) | ![](https://badgen.net/github/stars/hellogumbo/awesome-jev) | 社区目录站形态 |
| [**JackZeng/Jev_apps**](https://github.com/JackZeng/Jev_apps) | ![](https://badgen.net/github/stars/JackZeng/Jev_apps) | 不是链接列表，是**案例库**：129 个应用逐个拆开讲原理，中英双语，每条带 A/B/C 证据分级和原帖溯源。「这个宣传超出证据了」标得很直接，本列表这次的补充就是对着它查的 |

---

## 🧊 冷静看待

这个生态才几天大，讨论的热度远远跑在验证的前面。下面五点是我整理这份列表时反复撞到的，放在这里供参考。

| | |
| :-- | :-- |
| **「快 193 倍」是厂商自评** | 数据出自 TypeSafe 自己的 [workflow evals](https://evals.typesafe.ai)，官方也标注了那是收益上限。[HN 讨论](https://news.ycombinator.com/item?id=49717558)里提出的质疑值得重视：拿一个只做分类的模型和一个要生成完整回答的模型比延迟，口径本身并不对等 |
| **官方公布了能力毛边** | [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) 列出了已知的失败模式。厂商愿意主动公开这些是好事，同时也说明一件事：它在不同任务上的表现并不均匀，上生产前用自己的数据跑一遍不算多余 |
| **中文场景零公开数据** | 训练语料未公开，中文任务的校准质量也还没有任何公开评测。英文场景的结论直接迁移到中文工单和内容审核上，风险是未知的 |
| **「不可能幻觉」有边界** | 它的准确含义是：输出不可能违反 schema、不可能编出你没定义的选项。这**不等于判断一定正确**——选错依然会发生，兜底要靠你的置信度门控，而不是模型本身的保证 |
| **早期生态风险** | 依赖单一新供应商、配额不稳定、API 可能随版本变化。官方的 [adapter](https://github.com/typesafe-ai/system-one-adapter-python) 可以当降级方案用，一开始就接上成本很低 |

### 两份独立评测，十分钟能读完

[**jev-phishing-bench**](https://github.com/anisselbd/jev-phishing-bench)（2000 封钓鱼邮件）是目前最严谨的一份。结论对 Jev 有不利的一面，也有有利的一面：

| 用法 | 准确率 |
| :-- | :-- |
| 直接问 Jev「该不该点这个链接」 | 62.6% |
| Claude Haiku 4.5 问同一个问题 | 81.3% |
| 两行正则规则 | 91.8% |
| **同一次调用拆成 5 个信号 + 代码里做回归** | **95.0%** |

同样的分解，Jev 便宜约 27 倍，延迟 239ms 对 687ms。作者还补了一组对照：把这 5 个问题原样拿去问 Haiku，回归后能到 93.2%，与 Jev 在统计上没有显著差异。这组对照让整份评测的可信度高了不少。

[**jev-spam-eval**](https://github.com/bitnovus/jev-spam-eval)（18,514 封邮件）展示了它擅长的一面：仅凭一段写出来的垃圾邮件定义就拿到 98.3%，和用约 14,800 条标注训练出的 TF-IDF（98.4%）基本持平。更有意思的是分布漂移那一组——换到 2026 年的新邮件，Jev 仍有 97.3%，TF-IDF 掉到 72.5%。**抗分布漂移，大概才是它真正稳定的优势。**

**这两份评测让我改变了三个原本的想法：**

1. **它不是万能判断器。** 单问一个复合问题是它最弱的用法，62.6% 就是这么来的——我原本以为「问题写清楚就行」，显然不是。
2. **拆成原子信号、组合逻辑留在自己代码里，差别比想象中大得多。** 同一个模型、同一批数据、同一次调用，62.6% 到 95.0%。[组合打分模式](https://docs.typesafe.ai/patterns/composite-scoring)讲的就是这件事，看数据之前我没当回事。
3. **传统基线依然很能打。** 两行正则 91.8% 这个结果挺让人清醒的。Jev 稳定的优势在成本、延迟和抗分布漂移，不在绝对准确率——谁要是说它在所有任务上都更准，问一句数据在哪儿是合理的。

---

## 📖 中文指南

英文资料已经相当丰富，所以这两份只补中文世界缺的那一块：怎么写第一段代码，以及怎么用自己的数据把阈值量出来。

| 文档 | 内容 |
| :-- | :-- |
| [**上手指南**](docs/quickstart.md) | 接入路径、三原语讲透、置信度门控怎么定阈值、一个能上线的工单分类器、报错对照 |
| [**图解说明**](https://code.jiangshu.ai/awesome-jev-zh/) | 16 页幻灯片：真实请求、真实返回、真实数字。转给同事看，比你解释半天管用 |
| [**概念与心法**](docs/concepts.md) | System One 新在哪、RLCD vs RLHF、为什么问题要原子、校准概率怎么读、LLM 流程改造四步法 |

---

## 🤝 贡献

欢迎 PR。三条约定：**项目确实基于 Jev、链接可以打开、用一句中文说清它做什么。** 精选表按 Star 降序，新条目插到对应位置；拿不准就跑一下 `scripts/sort_tables.py`。

暂不收录空仓库、纯 API 中转服务，以及只有 landing page、没有可读代码的项目。细则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

[CC0 1.0](LICENSE) — 本列表贡献到公有领域，随便用。

---

<div align="center">

这份列表如果帮上忙了，欢迎点个 Star

由 [云中江树](https://github.com/yzfly) 维护 · 微信公众号「云中江树」

[![Star History Chart](https://api.star-history.com/svg?repos=yzfly/awesome-jev-zh&type=Date)](https://star-history.com/#yzfly/awesome-jev-zh&Date)

</div>
