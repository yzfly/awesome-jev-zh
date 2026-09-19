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

**入门** — [官方资源](#-官方资源) · [Jev 是什么](#-jev-是什么) · [上手](#-上手) · [规格与定价](#-规格与定价) · [该用与不该用](#-该用与不该用) · [中文指南](#-中文指南)

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

## 🧠 Jev 是什么

它针对一份 state——一封邮件、一行日志、一个工单、一坨游戏坐标 JSON——评估一组带类型的问题，返回代码能直接 `if`、能排序、能路由的值。就这么简单。

TypeSafe 管这类模型叫 System One，取自卡尼曼的「系统一」，快速直觉的那套。训练方法叫 RLCD，优化目标是概率诚实而不是人类偏好——RLHF 那套「让人满意」的训练会毁掉校准，因为犹豫的回答不讨喜。对聊天这是优点，对自动化这是灾难：你没法拿一个假的 90% 去写门控。

**这套说法目前没有公开论文。** 校准好不好，在你自己的数据上量，别信任何人的 slide。

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

## ⚡ 上手

官方直连需要排 waitlist，不过不必干等——下面几条路现在就能动手：

| 路径 | 模型 ID | 要不要 waitlist | 适合谁 |
| :-- | :-- | :-- | :-- |
| [Vercel AI Gateway](https://vercel.com/ai-gateway/models/jev) | `typesafe-ai/jev` | 不用 | 最省事，[已官方上线](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)，走 AI SDK 的 `experimental_evaluate` |
| [官方 adapter](https://github.com/typesafe-ai/system-one-adapter-python) | — | 不用 | 没 key 也能先写代码：接口一致的替身，后端换成普通 LLM |
| [TypeSafe 官方 API](https://console.typesafe.ai/settings/keys) | `jev-latest` / `jev-1.13.0` | 要排队 | 完整 SDK、最低延迟、企业配额 |
| [Playground](https://console.typesafe.ai/playground) | — | 看账号 | 不写代码，粘一段 state 点几下 |
| [OpenRouter](https://openrouter.ai/typesafe/jev-1.13) | `typesafe/jev-1.13` | 待确认 | 有模型页，但其 `/api/v1/models` 尚未列出，调用前请自行确认 |

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
> 🤖 由 [`scripts/collect_hot.py`](scripts/collect_hot.py) 每日自动抓取并排序，最后更新：**2026-09-19**（UTC）。收录规则：2026-09-10 之后创建、名称/描述/README 命中 Jev 生态关键词、Star ≥ 3，外加 [`typesafe-ai`](https://github.com/typesafe-ai) 官方组织全量。`🆕` = 本周新进榜，`▲` = 相比上次抓取的 Star 增量。

| # | 项目 | Star | 变化 | 语言 | 一句话 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | [**browser-use/jev-ultrafast**](https://github.com/browser-use/jev-ultrafast) `🆕` | ![](https://badgen.net/github/stars/browser-use/jev-ultrafast) | ▲ 2480 | Python | i. am. speed. |
| 2 | [**tamaratran/fast-jev-compaction**](https://github.com/tamaratran/fast-jev-compaction) `🆕` | ![](https://badgen.net/github/stars/tamaratran/fast-jev-compaction) | ▲ 1843 | TS | Claude Code plugin that replaces the compaction summary with Jev decisions: every tool call and… |
| 3 | [**TheoLeeCJ/SemIf**](https://github.com/TheoLeeCJ/SemIf) `🆕` | ![](https://badgen.net/github/stars/TheoLeeCJ/SemIf) | — | Python | Semantic ifs from open models, on a 3090 at home. Independent; not affiliated with Jev or TypeS… |
| 4 | [**vinnylarouge/jevlike**](https://github.com/vinnylarouge/jevlike) `🆕` | ![](https://badgen.net/github/stars/vinnylarouge/jevlike) | ▲ 150 | Python | — |
| 5 | [**jarrodwatts/jev-trader**](https://github.com/jarrodwatts/jev-trader) `🆕` | ![](https://badgen.net/github/stars/jarrodwatts/jev-trader) | ▲ 258 | TS | One AI trade decision every Monad block. Jev on Kuru MON-USDC. |
| 6 | [**TianyuCodings/NanoJev**](https://github.com/TianyuCodings/NanoJev) `🆕` | ![](https://badgen.net/github/stars/TianyuCodings/NanoJev) | ▲ 339 | Python | A nano replica of Jev: parallel decisions, dynamic candidates, and an end-to-end training pipel… |
| 7 | [**thruwire/foreman**](https://github.com/thruwire/foreman) `🆕` | ![](https://badgen.net/github/stars/thruwire/foreman) | ▲ 66 | Python | Software factory foreman based on TypeSafe's Jev model |
| 8 | [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) `官方` `🆕` | ![](https://badgen.net/github/stars/typesafe-ai/skills) | ▲ 140 | — | Agent skills for building with TypeSafe's System One API |
| 9 | [**devagrawal09/jev-review**](https://github.com/devagrawal09/jev-review) `🆕` | ![](https://badgen.net/github/stars/devagrawal09/jev-review) | ▲ 78 | TS | A staged code-review workflow and local dashboard built with TypeSafe Jev. |
| 10 | [**fhshaik/typesafe-mario**](https://github.com/fhshaik/typesafe-mario) `🆕` | ![](https://badgen.net/github/stars/fhshaik/typesafe-mario) | ▲ 24 | Python | A TypeSafe/Jev agent that plays Super Mario Bros. from structured emulator state. |
| 11 | [**AbdelStark/awesome-typesafe**](https://github.com/AbdelStark/awesome-typesafe) `🆕` | ![](https://badgen.net/github/stars/AbdelStark/awesome-typesafe) | ▲ 139 | CSS | A curated list of official resources and community projects for TypeSafe, System One models, an… |
| 12 | [**dabit3/jev-experiments**](https://github.com/dabit3/jev-experiments) `🆕` | ![](https://badgen.net/github/stars/dabit3/jev-experiments) | ▲ 173 | TS | — |
| 13 | [**awlevin/typesafe-computer-use**](https://github.com/awlevin/typesafe-computer-use) `🆕` | ![](https://badgen.net/github/stars/awlevin/typesafe-computer-use) | ▲ 46 | Python | Computer use for about $0.0002 a step: OCR the screen, classify the next action with TypeSafe,… |
| 14 | [**yibie/awesome-jev**](https://github.com/yibie/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/yibie/awesome-jev) | ▲ 112 | Python | A curated list of public projects, integrations, and discussions built on Jev — TypeSafe AI's S… |
| 15 | [**realZachi/pg-jev**](https://github.com/realZachi/pg-jev) `🆕` | ![](https://badgen.net/github/stars/realZachi/pg-jev) | ▲ 97 | Shell | Ask your Postgres tables questions in plain language. A PostgreSQL extension powered by TypeSaf… |
| 16 | [**kitze/skillbox**](https://github.com/kitze/skillbox) `🆕` | ![](https://badgen.net/github/stars/kitze/skillbox) | ▲ 42 | TS | Self-hosted, versioned skills library for AI agents. MCP, scoped clients, and optional Jev reco… |
| 17 | [**ekzhang/openjev-sglang**](https://github.com/ekzhang/openjev-sglang) `🆕` | ![](https://badgen.net/github/stars/ekzhang/openjev-sglang) | ▲ 78 | Python | Jev-compatible API endpoint based on open models (prefill-only) |
| 18 | [**jaredpalmer/kev**](https://github.com/jaredpalmer/kev) `🆕` | ![](https://badgen.net/github/stars/jaredpalmer/kev) | — | Python | tiny Jev-like model built on top of Qwen2.5-0.5B you can train and run on your MacBook |
| 19 | [**gargpratyush/jev-router**](https://github.com/gargpratyush/jev-router) `🆕` | ![](https://badgen.net/github/stars/gargpratyush/jev-router) | ▲ 55 | JS | Route to the cheapest model in claude code for your task using jev-router |
| 20 | [**droidrun/mobile-jev**](https://github.com/droidrun/mobile-jev) `🆕` | ![](https://badgen.net/github/stars/droidrun/mobile-jev) | ▲ 82 | JS | — |
| 21 | [**typesafe-ai/typesafe-sdk-js**](https://github.com/typesafe-ai/typesafe-sdk-js) `官方` `🆕` | ![](https://badgen.net/github/stars/typesafe-ai/typesafe-sdk-js) | ▲ 38 | TS | The official TypeScript/JavaScript library for the TypeSafe API |
| 22 | [**kyotofin/tax-doc-classifier**](https://github.com/kyotofin/tax-doc-classifier) `🆕` | ![](https://badgen.net/github/stars/kyotofin/tax-doc-classifier) | — | TS | Tax document page classifier built on Jev decisions. 100% strict accuracy across 261 IRS forms,… |
| 23 | [**NiazMorshed2007/jev-review**](https://github.com/NiazMorshed2007/jev-review) `🆕` | ![](https://badgen.net/github/stars/NiazMorshed2007/jev-review) | ▲ 30 | TS | Local-first MCP plugin for continuous software-quality review by AI coding agents, powered by J… |
| 24 | [**typesafe-ai/system-one-adapter-python**](https://github.com/typesafe-ai/system-one-adapter-python) `官方` `🆕` | ![](https://badgen.net/github/stars/typesafe-ai/system-one-adapter-python) | ▲ 30 | Python | Drop-in TypeSafeClient replacement backed by LLM APIs |
| 25 | [**cobanov/awesome-jev**](https://github.com/cobanov/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/cobanov/awesome-jev) | — | — | A curated, source-backed list of projects built with Jev, TypeSafe AI's System One model for ty… |
| 26 | [**superagents-lab/jev-search**](https://github.com/superagents-lab/jev-search) `🆕` | ![](https://badgen.net/github/stars/superagents-lab/jev-search) | ▲ 112 | TS | Search the web with TypeSafe's Jev: source selection, query understanding and relevance ranking… |
| 27 | [**fatwang2/awesome-jev**](https://github.com/fatwang2/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/fatwang2/awesome-jev) | — | JS | A source-backed Jev project directory with a reusable Jev-only GitHub review workflow. |
| 28 | [**hr98w/jev-visual**](https://github.com/hr98w/jev-visual) `🆕` | ![](https://badgen.net/github/stars/hr98w/jev-visual) | ▲ 58 | Python | An educational Jev-like visual inference experiment on Apple Silicon: shared context, direct ca… |
| 29 | [**jkudish/jev-browser**](https://github.com/jkudish/jev-browser) `🆕` | ![](https://badgen.net/github/stars/jkudish/jev-browser) | ▲ 77 | TS | Browser use using Typesafe's Jev model |
| 30 | [**dbreunig/building-with-jev-skill**](https://github.com/dbreunig/building-with-jev-skill) `🆕` | ![](https://badgen.net/github/stars/dbreunig/building-with-jev-skill) | ▲ 65 | — | A skill for writing and improving programs that call Jev, TypeSafe's System One model |
| 31 | [**wy-coliney/jev-browser-use**](https://github.com/wy-coliney/jev-browser-use) `🆕` | ![](https://badgen.net/github/stars/wy-coliney/jev-browser-use) | — | JS | 5–10x faster browser operations: Jev clicks, Codex thinks and verifies. Built at EZCollegeApp. |
| 32 | [**kitze/unclutter**](https://github.com/kitze/unclutter) `🆕` | ![](https://badgen.net/github/stars/kitze/unclutter) | ▲ 46 | TS | WXT browser extension: Jev-powered page clutter removal with reusable template rules. |
| 33 | [**typesafe-ai/typesafe-sdk-python**](https://github.com/typesafe-ai/typesafe-sdk-python) `官方` `🆕` | ![](https://badgen.net/github/stars/typesafe-ai/typesafe-sdk-python) | ▲ 29 | Python | The official Python library for the TypeSafe API |
| 34 | [**vinilana/jev-eval-agent**](https://github.com/vinilana/jev-eval-agent) `🆕` | ![](https://badgen.net/github/stars/vinilana/jev-eval-agent) | ▲ 11 | HTML | — |
| 35 | [**giuliosmall/pg_typesafe**](https://github.com/giuliosmall/pg_typesafe) `🆕` | ![](https://badgen.net/github/stars/giuliosmall/pg_typesafe) | — | C | Pre-alpha PostgreSQL extension for TypeSafe AI (Jev) categorical classification |
| 36 | [**moritzkremb/jev-voice-browser**](https://github.com/moritzkremb/jev-voice-browser) `🆕` | ![](https://badgen.net/github/stars/moritzkremb/jev-voice-browser) | — | JS | Control a real browser by voice. Jev (TypeSafe System One) decides intent + target in ~300 ms p… |
| 37 | [**pithings/advocaat**](https://github.com/pithings/advocaat) `🆕` | ![](https://badgen.net/github/stars/pithings/advocaat) | ▲ 21 | TS | A small, type-safe client for asking AI questions about your data, powered by TypeSafe Jev. |
| 38 | [**jkudish/jev-mcp**](https://github.com/jkudish/jev-mcp) `🆕` | ![](https://badgen.net/github/stars/jkudish/jev-mcp) | ▲ 19 | TS | Fast, cheap, typed judgments from TypeSafe's Jev model, as MCP tools. |
| 39 | [**lakeday-org/perch**](https://github.com/lakeday-org/perch) `🆕` | ![](https://badgen.net/github/stars/lakeday-org/perch) | ▲ 68 | JS | Semantic code linting with Jev |
| 40 | [**standardagents/jevpilot**](https://github.com/standardagents/jevpilot) `🆕` | ![](https://badgen.net/github/stars/standardagents/jevpilot) | ▲ 37 | JS | A playable Three.js driving simulator with Jev-powered autopilot |
| 41 | [**itsmostafa/typesafe-mcp**](https://github.com/itsmostafa/typesafe-mcp) `🆕` | ![](https://badgen.net/github/stars/itsmostafa/typesafe-mcp) | ▲ 34 | Go | mcp connector to give your AI agent direct access to typesafe ai's jev model |
| 42 | [**AnotiaWang/awesome-jev**](https://github.com/AnotiaWang/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/AnotiaWang/awesome-jev) | ▲ 36 | — | A curated list of awesome Jev / TypeSafe System One applications, libraries, and resources. |
| 43 | [**y0usaf/pi-jev**](https://github.com/y0usaf/pi-jev) `🆕` | ![](https://badgen.net/github/stars/y0usaf/pi-jev) | ▲ 38 | TS | TypeSafe Jev as a decision layer for the Pi coding agent: a measured tool-call gate plus jev_as… |
| 44 | [**featherless-ai/simple-jev**](https://github.com/featherless-ai/simple-jev) `🆕` | ![](https://badgen.net/github/stars/featherless-ai/simple-jev) | — | Python | Turn any open model into a classifier/jev endpoint |
| 45 | [**DevMortimer/pi-warden**](https://github.com/DevMortimer/pi-warden) `🆕` | ![](https://badgen.net/github/stars/DevMortimer/pi-warden) | ▲ 17 | TS | Guardrails for Pi built on pi-typesafe that steer the agent instead of interrupting you: Jev ju… |
| 46 | [**kshetrajna12/reflex**](https://github.com/kshetrajna12/reflex) `🆕` | ![](https://badgen.net/github/stars/kshetrajna12/reflex) | ▲ 29 | Python | A small open decision model: state + typed questions -> calibrated probabilities. A Jev / Syste… |
| 47 | [**RomanSlack/jev-drone**](https://github.com/RomanSlack/jev-drone) `🆕` | ![](https://badgen.net/github/stars/RomanSlack/jev-drone) | ▲ 7 | Python | Camera-only autonomous drone in MuJoCo with a small judgment model (TypeSafe Jev) in the loop a… |
| 48 | [**ChetasLua/jevmeter**](https://github.com/ChetasLua/jevmeter) `🆕` | ![](https://badgen.net/github/stars/ChetasLua/jevmeter) | ▲ 14 | Python | Put a live Jev (TypeSafe) meter on any video: every sentence scored, rendered as a 16:9 edit |
| 49 | [**trungdq88/youtube-sponsor-detection**](https://github.com/trungdq88/youtube-sponsor-detection) `🆕` | ![](https://badgen.net/github/stars/trungdq88/youtube-sponsor-detection) | ▲ 48 | JS | Detect youtube sponsor segment with live audio and transcript powered by Jev |
| 50 | [**kunchenguid/compact-adviser**](https://github.com/kunchenguid/compact-adviser) `🆕` | ![](https://badgen.net/github/stars/kunchenguid/compact-adviser) | — | TS | "Work appears completed or recorded. Run /compact to save tokens." |
| 51 | [**realZachi/typesafe-adblock**](https://github.com/realZachi/typesafe-adblock) `🆕` | ![](https://badgen.net/github/stars/realZachi/typesafe-adblock) | ▲ 21 | JS | Fun project: a Chrome extension that asks a tiny AI decision model (TypeSafe Jev) "is this DOM… |
| 52 | [**Dicklesworthstone/skillranker**](https://github.com/Dicklesworthstone/skillranker) `🆕` | ![](https://badgen.net/github/stars/Dicklesworthstone/skillranker) | ▲ 12 | Rust | Rust CLI powered by Jev from TypeSafe.ai that ranks agent skills for the next step using live s… |
| 53 | [**0xNatoshi/jev-codex-router**](https://github.com/0xNatoshi/jev-codex-router) `🆕` | ![](https://badgen.net/github/stars/0xNatoshi/jev-codex-router) | ▲ 31 | Python | Per-turn model & reasoning routing for Codex, driven by Jev (TypeSafe System One): picks the mo… |
| 54 | [**mrnugget/jev-shell-history**](https://github.com/mrnugget/jev-shell-history) `🆕` | ![](https://badgen.net/github/stars/mrnugget/jev-shell-history) | — | TS | Fish-style zsh history autosuggestions ranked by Jev (TypeSafe) |
| 55 | [**IAmUnbounded/save-token-jev-clean**](https://github.com/IAmUnbounded/save-token-jev-clean) `🆕` | ![](https://badgen.net/github/stars/IAmUnbounded/save-token-jev-clean) | — | TS | — |
| 56 | [**razorback16/openjev**](https://github.com/razorback16/openjev) `🆕` | ![](https://badgen.net/github/stars/razorback16/openjev) | — | Python | Open, Jev-compatible System One decision server on DiffusionGemma |
| 57 | [**hellogumbo/awesome-jev**](https://github.com/hellogumbo/awesome-jev) `🆕` | ![](https://badgen.net/github/stars/hellogumbo/awesome-jev) | ▲ 21 | JS | A community directory of projects built on Jev, TypeSafe AI's System One model. |
| 58 | [**daseinlabs/open-jev**](https://github.com/daseinlabs/open-jev) `🆕` | ![](https://badgen.net/github/stars/daseinlabs/open-jev) | ▲ 14 | Python | — |
| 59 | [**iammrduncan/typesafe-ai-benchmark**](https://github.com/iammrduncan/typesafe-ai-benchmark) `🆕` | ![](https://badgen.net/github/stars/iammrduncan/typesafe-ai-benchmark) | ▲ 3 | TS | This is a LLM Gateway that mimics typesafe ai structured output. Like an imposter Jev. |
| 60 | [**logicrw/awesome-jev-projects**](https://github.com/logicrw/awesome-jev-projects) `🆕` | ![](https://badgen.net/github/stars/logicrw/awesome-jev-projects) | — | JS | Awesome Jev: source-backed open-source ecosystem radar, plain-language project discovery, and a… |
<!-- HOT:END -->

---

## 🧰 SDK 与客户端

多数情况下官方那两个 SDK 就够用。社区版本主要补官方还没覆盖的语言，质量参差不齐，接入前翻一下源码比较稳妥。

### 官方

| 项目 | Star | 安装 | 说明 |
| :-- | :-- | :-- | :-- |
| [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) | ![](https://badgen.net/github/stars/typesafe-ai/skills) | `claude plugin install typesafe@typesafe-ai` | 官方 Agent 技能包：原语、模式、怎么组织 evaluation |
| [**typesafe-ai/typesafe-sdk-js**](https://github.com/typesafe-ai/typesafe-sdk-js) | ![](https://badgen.net/github/stars/typesafe-ai/typesafe-sdk-js) | `npm i @typesafe-ai/sdk` | 官方 TS/JS 客户端，类型定义完整 |
| [**typesafe-ai/system-one-adapter-python**](https://github.com/typesafe-ai/system-one-adapter-python) | ![](https://badgen.net/github/stars/typesafe-ai/system-one-adapter-python) | `pip install system-one-adapter` | 官方出的 `TypeSafeClient` 替身，后端走普通 LLM API。**没拿到 waitlist 也能先写代码**，还能用同一套问题横向对比 Jev 与聊天模型 |
| [**typesafe-ai/typesafe-sdk-python**](https://github.com/typesafe-ai/typesafe-sdk-python) | ![](https://badgen.net/github/stars/typesafe-ai/typesafe-sdk-python) | `pip install typesafe-sdk` | 官方 Python 客户端，同步/异步双版本，自带重试 |
| [Vercel AI SDK provider](https://ai-sdk.dev/providers/ai-sdk-providers/typesafe-ai) | — | `npm i @ai-sdk/typesafe-ai` | `experimental_evaluate` + `typeSafeAi.evaluationModel('jev-latest')` |

### 社区

| 语言 | 项目 | Star | 说明 |
| :-- | :-- | :-- | :-- |
| TypeScript | [**pithings/advocaat**](https://github.com/pithings/advocaat) | ![](https://badgen.net/github/stars/pithings/advocaat) | 小而美的 TS 客户端，给三原语打了 tagged helper |
| Ruby | [**kieranklaassen/ruby_llm-typesafe**](https://github.com/kieranklaassen/ruby_llm-typesafe) | ![](https://badgen.net/github/stars/kieranklaassen/ruby_llm-typesafe) | RubyLLM 2 的 TypeSafe provider，带离线模型元数据 |
| Rust | [**Twister915/typesafe-ai**](https://github.com/Twister915/typesafe-ai) | ![](https://badgen.net/github/stars/Twister915/typesafe-ai) | 另一个 Rust 客户端，异步 + 阻塞传输、可观测重试 |
| Erlang/OTP | [**dannote/jev**](https://github.com/dannote/jev) | ![](https://badgen.net/github/stars/dannote/jev) | 从 GenServer 回复 Jev，直接模式匹配答案 |
| Shell | [**shiftynick/jev-axi**](https://github.com/shiftynick/jev-axi) | ![](https://badgen.net/github/stars/shiftynick/jev-axi) | 面向 Agent 的 CLI：pick / rate / check / rank / triage |
| .NET | [**saibimajdi/typesafeai-dotnet-sdk**](https://github.com/saibimajdi/typesafeai-dotnet-sdk) | ![](https://badgen.net/github/stars/saibimajdi/typesafeai-dotnet-sdk) | 类型化问题 + 带置信度的答案 |
| Ruby | [**joshmn/typesafe-sdk**](https://github.com/joshmn/typesafe-sdk) | ![](https://badgen.net/github/stars/joshmn/typesafe-sdk) | Ruby 3.1+ 客户端，线程安全连接池；无异步客户端 |
| Shell | [**y0usaf/typesafe-cli**](https://github.com/y0usaf/typesafe-cli) | ![](https://badgen.net/github/stars/y0usaf/typesafe-cli) | 命令行直接问 noul/choice/score，返回数字不返回废话 |
| Rust | [**gilljon/typesafe-ai-rs**](https://github.com/gilljon/typesafe-ai-rs) | ![](https://badgen.net/github/stars/gilljon/typesafe-ai-rs) | 独立的异步 / 阻塞 System One 客户端 |
| Go | [**Gaurav-Gosain/jev-go**](https://github.com/Gaurav-Gosain/jev-go) | ![](https://badgen.net/github/stars/Gaurav-Gosain/jev-go) | `go get github.com/Gaurav-Gosain/jev-go`，返回类型化判断与校准概率 |
| Rails | [**GenieRobot/typesafe-ai-rails**](https://github.com/GenieRobot/typesafe-ai-rails) | ![](https://badgen.net/github/stars/GenieRobot/typesafe-ai-rails) | Rails 集成：配置、用量/成本遥测、可选置信度策略 |
| PHP | [**Butochnikov/typesafe-sdk-php**](https://github.com/Butochnikov/typesafe-sdk-php) | ![](https://badgen.net/github/stars/Butochnikov/typesafe-sdk-php) | 类型化 DTO、Promise 与异常 |
| Laravel | [**Butochnikov/laravel-typesafe-jev**](https://github.com/Butochnikov/laravel-typesafe-jev) | ![](https://badgen.net/github/stars/Butochnikov/laravel-typesafe-jev) | Laravel 12/13 集成：Facade、scoped DI、recording fake |
| Elixir | [**nshkrdotcom/typesafe_sdk**](https://github.com/nshkrdotcom/typesafe_sdk) | ![](https://badgen.net/github/stars/nshkrdotcom/typesafe_sdk) | Hex 包，支持 `system_one` 与模型列表 |
| Scala/ZIO | [**jamesward/zio-typesafe-ai**](https://github.com/jamesward/zio-typesafe-ai) | ![](https://badgen.net/github/stars/jamesward/zio-typesafe-ai) | ZIO 客户端，带 noul/choice/score 小 DSL |
| Python | [**AboveColin/jevclient**](https://github.com/AboveColin/jevclient) | ![](https://badgen.net/github/stars/AboveColin/jevclient) | 非官方异步 Python 客户端 `pip install jevclient` |
| Rust | [**AbdelStark/s1-rs**](https://github.com/AbdelStark/s1-rs) | ![](https://badgen.net/github/stars/AbdelStark/s1-rs) | derive 宏层：Choice/Score/Noul、类型化问题集、置信度门控、无网络测试 |

> **包名容易看错**：PyPI 上要装的是 `typesafe-sdk`。[`typesafe-ai`](https://pypi.org/project/typesafe-ai/) 是社区注册的占位包，用来挡蹭名字的恶意包，本身不是官方 SDK。

---

## 🛠 应用

这些项目已经把 Jev 放进了真实的循环里。整份列表我自己读得最久的就是这一栏——别人踩过的坑，可以直接绕开。

| 项目 | Star | 说明 |
| :-- | :-- | :-- |
| [**browser-use/jev-ultrafast**](https://github.com/browser-use/jev-ultrafast) | ![](https://badgen.net/github/stars/browser-use/jev-ultrafast) | 全生态第一爆款。Browser Use 官方出品的浏览器 Agent：一次请求里让 Jev 同时选出「做什么操作」和「操作哪个 DOM 元素」，只有真要打字时才叫小模型。Google Flights 苏黎世→伦敦订票 **7 秒 / $0.0039**。附库、本地 inspector 与测时 |
| [**tamaratran/fast-jev-compaction**](https://github.com/tamaratran/fast-jev-compaction) | ![](https://badgen.net/github/stars/tamaratran/fast-jev-compaction) | Claude Code 插件：把上下文压缩的「总结」换成 Jev 判断——每次工具调用和结果都打分，决定留不留。**上下文工程的新范式** |
| [**jarrodwatts/jev-trader**](https://github.com/jarrodwatts/jev-trader) | ![](https://badgen.net/github/stars/jarrodwatts/jev-trader) | 每个 Monad 区块对 Kuru 的 MON-USDC 做一次买卖决策。在线：[jev-trader.vercel.app](https://jev-trader.vercel.app/) |
| [**thruwire/foreman**](https://github.com/thruwire/foreman) | ![](https://badgen.net/github/stars/thruwire/foreman) | 软件工厂循环：Codex 负责写，Jev 独立判断「做完没 / 测试够不够 / 要不要叫人」。把「谁来验收」这件事从 LLM 手里拿走 |
| [**devagrawal09/jev-review**](https://github.com/devagrawal09/jev-review) | ![](https://badgen.net/github/stars/devagrawal09/jev-review) | 分阶段代码审查工作流 + 本地 dashboard，由一串聚焦的 Jev 调用驱动 |
| [**awlevin/typesafe-computer-use**](https://github.com/awlevin/typesafe-computer-use) | ![](https://badgen.net/github/stars/awlevin/typesafe-computer-use) | macOS computer-use：OCR 屏幕 → Jev 分类下一步动作 → 点击。约 **$0.0002/步** |
| [**kitze/skillbox**](https://github.com/kitze/skillbox) | ![](https://badgen.net/github/stars/kitze/skillbox) | 自托管、带版本的 Agent 技能库，MCP + 作用域客户端，可选用 Jev 做技能推荐 |
| [**realZachi/pg-jev**](https://github.com/realZachi/pg-jev) | ![](https://badgen.net/github/stars/realZachi/pg-jev) | PostgreSQL 扩展：**直接在 SQL 里用自然语言问你的表**。`WHERE jev_noul(comment, '这是投诉') > 0.8` 这种写法 |
| [**droidrun/mobile-jev**](https://github.com/droidrun/mobile-jev) | ![](https://badgen.net/github/stars/droidrun/mobile-jev) | Android Agent，每次点击由 Jev 决定。打开 Uber、旧金山机场→金门大桥，**21 秒 / 9 步**到支付页，**不需要 ADB** |
| [**RomanSlack/jev-drone**](https://github.com/RomanSlack/jev-drone) | ![](https://badgen.net/github/stars/RomanSlack/jev-drone) | MuJoCo 四旋翼：控制与安全留在代码里，Jev 只做 2.5Hz 的战术判断 |
| [**kitze/unclutter**](https://github.com/kitze/unclutter) | ![](https://badgen.net/github/stars/kitze/unclutter) | Chrome / Firefox 扩展：Jev 标出页面上不重要的元素，本地按页面模板记住，下次访问直接藏 |
| [**ChetasLua/jevmeter**](https://github.com/ChetasLua/jevmeter) | ![](https://badgen.net/github/stars/ChetasLua/jevmeter) | 给任意视频挂实时 Jev 仪表：逐句打分，导出 16:9 成片 |
| [**realZachi/typesafe-adblock**](https://github.com/realZachi/typesafe-adblock) | ![](https://badgen.net/github/stars/realZachi/typesafe-adblock) | Chrome 扩展，逐个 DOM 元素问「这是广告吗」。规则库可以退休了 |
| [**devanshbatham/commit-miner**](https://github.com/devanshbatham/commit-miner) | ![](https://badgen.net/github/stars/devanshbatham/commit-miner) | Rust CLI，给 commit diff 分类：修 bug、安全/CWE、变更类型，出 HTML/CSV 报告 |
| [**ellipsis-dev/blink**](https://github.com/ellipsis-dev/blink) | ![](https://badgen.net/github/stars/ellipsis-dev/blink) | 代码库语义搜索，Jev 驱动。不用向量库 |
| [**monteduro/killmyidea**](https://github.com/monteduro/killmyidea) | ![](https://badgen.net/github/stars/monteduro/killmyidea) | 描述你的创业点子，Jev 判决：毙掉、改改、还是发。玩法很毒但很有代表性 |
| [**jexp/neo4jev**](https://github.com/jexp/neo4jev) | ![](https://badgen.net/github/stars/jexp/neo4jev) | 让 Jev 在 Neo4j 图上导航：对邻居节点做分类，一步步走过去 |
| [**AboveColin/HA-Jev**](https://github.com/AboveColin/HA-Jev) | ![](https://badgen.net/github/stars/AboveColin/HA-Jev) | Home Assistant 集成：把「关于家里状态的类型化提问」变成传感器与自动化动作，带每日 token 预算实体 |
| [**reachjalil/jevlogs**](https://github.com/reachjalil/jevlogs) | ![](https://badgen.net/github/stars/reachjalil/jevlogs) | OpenTelemetry 日志分流：先让 Jev 打诊断价值和优先级，再决定要不要花钱叫 LLM |
| [**lakeday-org/perch**](https://github.com/lakeday-org/perch) | ![](https://badgen.net/github/stars/lakeday-org/perch) | AST 驱动的语义 code lint |
| [**sufianetaouil/every**](https://github.com/sufianetaouil/every) | ![](https://badgen.net/github/stars/sufianetaouil/every) | 语义代码搜索 CLI：对每个函数问一个是非题，按 Noul 概率排序 |
| [**asfarsadewa/human-compiler**](https://github.com/asfarsadewa/human-compiler) | ![](https://badgen.net/github/stars/asfarsadewa/human-compiler) | 粘贴职场废话，Jev 给「被动攻击 / 紧急感 / 信息密度」打分，代码按 rustc 风格报诊断。在线：[human-compiler.asfarlab.fun](https://human-compiler.asfarlab.fun) |
| [**santos-sanz/jev-audio-beeper**](https://github.com/santos-sanz/jev-audio-beeper) | ![](https://badgen.net/github/stars/santos-sanz/jev-audio-beeper) | 低延迟脏话检测：Jev 判定后 ffmpeg 在约 466ms 内叠一声 beep |
| [**TarunTomar122/jev-askable-arm**](https://github.com/TarunTomar122/jev-askable-arm) | ![](https://badgen.net/github/stars/TarunTomar122/jev-askable-arm) | 仿真 Franka 机械臂：英文目标 zero-shot，Jev 把硬编码原语串起来 |
| [**valentynkit/jev-commit**](https://github.com/valentynkit/jev-commit) | ![](https://badgen.net/github/stars/valentynkit/jev-commit) | pre-commit hook：一次 Jev 调用判断提交信息是否对得上暂存的 diff，顺带查调试残留、未提及的改动，撞到密钥直接拦截，其余只警告 |
| [**valentynkit/jev.nvim**](https://github.com/valentynkit/jev.nvim) | ![](https://badgen.net/github/stars/valentynkit/jev.nvim) | Neovim 插件：用大白话问当前 buffer 一个问题，Treesitter 拆出函数，Jev 逐个打分，答案按概率排进 quickfix |
| [**valentynkit/jev-skip**](https://github.com/valentynkit/jev-skip) | ![](https://badgen.net/github/stars/valentynkit/jev-skip) | 浏览器扩展：读字幕轨，在片头结束前就把每段赞助概率画上 YouTube 进度条，不依赖众包数据库。23 个视频上测得赞助时长命中率是 SponsorBlock 的 77%，每个视频 $0.0008 |

---

## 🎮 Demo

发布 48 小时内涌现出来的小玩具。我是挑了两三个跑完之后，才真正对它的能力边界有了感觉——比读十页文档快得多。

| 项目 | Star / 链接 | 说明 |
| :-- | :-- | :-- |
| [**fhshaik/typesafe-mario**](https://github.com/fhshaik/typesafe-mario) | ![](https://badgen.net/github/stars/fhshaik/typesafe-mario) | 从结构化模拟器状态玩超级马里奥 |
| [**standardagents/jevpilot**](https://github.com/standardagents/jevpilot) | ![](https://badgen.net/github/stars/standardagents/jevpilot) | Three.js 驾驶模拟器 + Jev 自动驾驶，可直接玩 |
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
| [官方智能家居 demo](https://docs.typesafe.ai/demos/smart-home) | 🔗 官方 | 演示**投机扇出**：一次问很多题，代码留下有用的，LLM 只管拆复合指令和闲聊 |
| [**valentynkit/jev-plays-pokemon-red**](https://github.com/valentynkit/jev-plays-pokemon-red) | ![](https://badgen.net/github/stars/valentynkit/jev-plays-pokemon-red) | PyBoy 上打宝可梦红：路线和数值算法都在代码里，Jev 只在分支点选，每回合战斗都用 Brier 分数把「会不会昏厥」的预测拿 RAM 里的实际结果打分 |

---

## 🤖 Agent 工具

把 Jev 接进 Claude Code、Codex、Cursor、MCP 的工具。这个方向的项目出得最快，原因也不难理解：编程 Agent 的每一步——路由到哪个模型、加载哪个技能、这条工具结果该不该留在上下文里——本质上都是选择题。

| 项目 | Star | 说明 |
| :-- | :-- | :-- |
| [**vercel/eve**](https://github.com/vercel/eve) | ![](https://badgen.net/github/stars/vercel/eve) | Vercel 的 Agent 框架，实验性 `autoModel` 默认用 Gateway 上的 `typesafe-ai/jev` 从白名单里挑语言模型 |
| [**typesafe-ai/skills**](https://github.com/typesafe-ai/skills) | ![](https://badgen.net/github/stars/typesafe-ai/skills) | **官方技能包**。Claude Code：`claude plugin marketplace add typesafe-ai/skills` → `claude plugin install typesafe@typesafe-ai`；其他 Agent：`npx skills add typesafe-ai/skills --skill typesafe-ai` |
| [**NiazMorshed2007/jev-review**](https://github.com/NiazMorshed2007/jev-review) | ![](https://badgen.net/github/stars/NiazMorshed2007/jev-review) | 本地优先 MCP：Claude Code / Codex / Cursor / OpenCode 边写边拿结构化质量审查 |
| [**gargpratyush/jev-router**](https://github.com/gargpratyush/jev-router) | ![](https://badgen.net/github/stars/gargpratyush/jev-router) | Claude Code 与 Codex 的每轮路由：简单活走快档，难活走强档。`npm i -g jev-router` |
| [**vlad-terin/jev-use**](https://github.com/vlad-terin/jev-use) | ![](https://badgen.net/github/stars/vlad-terin/jev-use) | Agent skill + 运行时：Codex 规划，Jev 选元素，runner 执行并逐步校验；已扩到桌面工作流，主打「少跑几轮 Codex」 |
| [**jkudish/jev-mcp**](https://github.com/jkudish/jev-mcp) | ![](https://badgen.net/github/stars/jkudish/jev-mcp) | Node MCP，封装三条 cookbook：`jev_verify` 引文核验、`jev_screen` 注入护栏、`jev_find` 无 embedding 语义排序。`npx -y github:jkudish/jev-mcp` |
| [**DevMortimer/pi-warden**](https://github.com/DevMortimer/pi-warden) | ![](https://badgen.net/github/stars/DevMortimer/pi-warden) | Pi 护栏：把判决当成 held tool result 而不是弹窗；对照项目规则文件检查写入 |
| [**dbreunig/building-with-jev-skill**](https://github.com/dbreunig/building-with-jev-skill) | ![](https://badgen.net/github/stars/dbreunig/building-with-jev-skill) | 一个专门教 Agent「怎么写调用 Jev 的程序」的 Skill |
| [**itsmostafa/typesafe-mcp**](https://github.com/itsmostafa/typesafe-mcp) | ![](https://badgen.net/github/stars/itsmostafa/typesafe-mcp) | Go 写的 CLI + 单二进制 MCP，适配 Claude Desktop / Claude Code / Codex |
| [**Dicklesworthstone/skillranker**](https://github.com/Dicklesworthstone/skillranker) | ![](https://badgen.net/github/stars/Dicklesworthstone/skillranker) | Rust CLI，用实时会话上下文给 Agent 技能排序，只加载最该加载的那个 |
| [**y0usaf/pi-jev**](https://github.com/y0usaf/pi-jev) | ![](https://badgen.net/github/stars/y0usaf/pi-jev) | Pi 扩展：影子模式工具调用门控、输出评判、类型化 `jev_ask` |
| [**shantanugoel/ask-jev-skill**](https://github.com/shantanugoel/ask-jev-skill) | ![](https://badgen.net/github/stars/shantanugoel/ask-jev-skill) | Hermes Skill：Agent 需要有界决策时去问 Jev |
| [**0xNatoshi/jev-codex-router**](https://github.com/0xNatoshi/jev-codex-router) | ![](https://badgen.net/github/stars/0xNatoshi/jev-codex-router) | Codex 每轮路由：Jev 选模型、思考深度和速度模式 |
| [**nidhi-singh02/agent-router**](https://github.com/nidhi-singh02/agent-router) | ![](https://badgen.net/github/stars/nidhi-singh02/agent-router) | CLI 按任务挑 Cursor / Claude Code / Codex / OpenCode + 模型档位，然后直接启动 |
| [**GhalebDweikat/winnow**](https://github.com/GhalebDweikat/winnow) | ![](https://badgen.net/github/stars/GhalebDweikat/winnow) | Claude Code 的校准上下文筛子：每个工具结果都被判一次再决定留不留 |
| [**blakestone-x/jev-mcp**](https://github.com/blakestone-x/jev-mcp) | ![](https://badgen.net/github/stars/blakestone-x/jev-mcp) | Python MCP：classify / score / check / match / screen |
| [**compozy/yoshi**](https://github.com/compozy/yoshi) | ![](https://badgen.net/github/stars/compozy/yoshi) | Claude Code / Codex 的上下文剪枝代理：Jev 判断哪些历史还需要，可量化 |
| [**jomatsu/pi-jev-auto-mode**](https://github.com/jomatsu/pi-jev-auto-mode) | ![](https://badgen.net/github/stars/jomatsu/pi-jev-auto-mode) | Pi 自动模式：Jev 按语义批准 `bash` / `write` / `edit`，判断不了就拒绝 |
| [**Ying-Kai-Liao/jev-browser**](https://github.com/Ying-Kai-Liao/jev-browser) | ![](https://badgen.net/github/stars/Ying-Kai-Liao/jev-browser) | LLM 规划、Jev 在 Playwright 快照上决定每次点击（约 300ms/次）。含 MCP：`npx -y -p jev-browser jev-browser-mcp` |
| [**sharziki/semdecide**](https://github.com/sharziki/semdecide) | ![](https://badgen.net/github/stars/sharziki/semdecide) | 给 Unix 管道和 CI 用的类型化语义决策，`cat log \| semdecide ...` |
| [**romaluev/jev-ego**](https://github.com/romaluev/jev-ego) | ![](https://badgen.net/github/stars/romaluev/jev-ego) | [ego lite](https://lite.ego.app/) 上的浏览器 Agent，observe / act / suggest / step CLI |
| [**samtay32/jev-system-architect**](https://github.com/samtay32/jev-system-architect) | ![](https://badgen.net/github/stars/samtay32/jev-system-architect) | 专找代码里脆弱的语义逻辑，改写成 Choice / Score / Noul 边界 |
| [**AbdelStark/bicameral**](https://github.com/AbdelStark/bicameral) | ![](https://badgen.net/github/stars/AbdelStark/bicameral) | Pi 编程 harness：LLM 写代码，Jev 提供策略、循环检测与 review 的类型化反射。**明确不是沙箱** |
| [**valentynkit/jev-belay**](https://github.com/valentynkit/jev-belay) | ![](https://badgen.net/github/stars/valentynkit/jev-belay) | Claude Code 的 Stop hook：读 transcript 找证据，只有文件改了且没有通过检查时才花一次四问 Jev 调用判断是否真的做完了，出错一律放行 |

---

## 🔬 复现与评测

这些是受 Jev 接口启发的独立工作，**都不是 TypeSafe 的模型**。想弄明白它在技术上怎么做到的，这些复现比官方博文讲得清楚。

### 开源复现

| 项目 | Star | 说明 |
| :-- | :-- | :-- |
| [**TheoLeeCJ/openjev**](https://github.com/TheoLeeCJ/openjev) | ![](https://badgen.net/github/stars/TheoLeeCJ/openjev) | 最受关注的复现：一张 RTX 3090 能不能跑 Jev 风格的东西？直接读选项 logits，不生成文本 |
| [**vinnylarouge/jevlike**](https://github.com/vinnylarouge/jevlike) | ![](https://badgen.net/github/stars/vinnylarouge/jevlike) | 训练一个小的单次 scorer：上下文 + N 个文本选项 → 每个选项一个概率。含 Doom / 国际象棋视觉 demo 与 Wikispeedia 下一跳例子。**明确声明不是 TypeSafe 架构或 RLCD 的复现** |
| [**ekzhang/openjev-sglang**](https://github.com/ekzhang/openjev-sglang) | ![](https://badgen.net/github/stars/ekzhang/openjev-sglang) | 基于开源模型的 Jev 兼容 API 端点（prefill-only） |
| [**hr98w/jev-visual**](https://github.com/hr98w/jev-visual) | ![](https://badgen.net/github/stars/hr98w/jev-visual) | Apple Silicon 上的 Jev 风格视觉推理教学实验：共享上下文、直接给候选打分 |
| [**TianyuCodings/NanoJev**](https://github.com/TianyuCodings/NanoJev) | ![](https://badgen.net/github/stars/TianyuCodings/NanoJev) | nano 版 Jev：并行决策、动态候选、端到端训练流水线。**想搞懂训练的从这个读** |
| [**kshetrajna12/reflex**](https://github.com/kshetrajna12/reflex) | ![](https://badgen.net/github/stars/kshetrajna12/reflex) | 小型开放决策模型：state + 类型化问题 → 校准概率 |
| [**bnsd55/jevmlx**](https://github.com/bnsd55/jevmlx) | ![](https://badgen.net/github/stars/bnsd55/jevmlx) | Apple Silicon 上给任意 MLX 模型做 Jev 式并行受限决策 |
| [**rorshopping/jev-on-a-laptop**](https://github.com/rorshopping/jev-on-a-laptop) | ![](https://badgen.net/github/stars/rorshopping/jev-on-a-laptop) | 非官方研究：1.5B–8B 现成模型在 Apple Silicon 上做并行类型化决策 |
| [**r-ms/mini-jev**](https://github.com/r-ms/mini-jev) | ![](https://badgen.net/github/stars/r-ms/mini-jev) | 冻结的 Qwen3-4B 上，Jev 式类型化决策接口长什么样 |
| [**Mapika/decider**](https://github.com/Mapika/decider) | ![](https://badgen.net/github/stars/Mapika/decider) | 基于 Qwen3.5-2B 微调：一次前向给出类型化决策和校准概率 |
| [**siliconkernel/vllm-jev-decison**](https://github.com/siliconkernel/vllm-jev-decison) | ![](https://badgen.net/github/stars/siliconkernel/vllm-jev-decison) | 给 vLLM 加「只分类」模式：有限 schema 候选打分 + 概率 |
| [**genai-craft/openvons**](https://github.com/genai-craft/openvons) | ![](https://badgen.net/github/stars/genai-craft/openvons) | 日文向 open-Jev：文本 / 图像 / 日语语音命令的概率判断层 |
| [**stephanj/parallelConstraintDecoding**](https://github.com/stephanj/parallelConstraintDecoding) | ![](https://badgen.net/github/stars/stephanj/parallelConstraintDecoding) | Java + Python 双版本的并行受限解码实现 |
| [**NullPo-jp/PocketJev**](https://github.com/NullPo-jp/PocketJev) | ![](https://badgen.net/github/stars/NullPo-jp/PocketJev) | iPhone 端侧视觉判断：MLX + Qwen3-VL 选项 logits。相机 + 三选一，约 1 秒，不存照片 |

### 独立评测

| 项目 | Star | 结论摘要 |
| :-- | :-- | :-- |
| [**vinilana/jev-eval-agent**](https://github.com/vinilana/jev-eval-agent) | ![](https://badgen.net/github/stars/vinilana/jev-eval-agent) | 早期 Jev 测试的公开评测 harness |
| [**iammrduncan/typesafe-ai-benchmark**](https://github.com/iammrduncan/typesafe-ai-benchmark) | ![](https://badgen.net/github/stars/iammrduncan/typesafe-ai-benchmark) | 同一套 System One 问题，对比 Jev 与 Cerebras 上的 Qwen 3.8 27B |
| [**AbdelStark/jev-benchmarks**](https://github.com/AbdelStark/jev-benchmarks) | ![](https://badgen.net/github/stars/AbdelStark/jev-benchmarks) | 面向类型化决策模型的概率感知评测框架 |
| [**mahlernim/jev-korean-benchmark**](https://github.com/mahlernim/jev-korean-benchmark) | ![](https://badgen.net/github/stars/mahlernim/jev-korean-benchmark) | 韩语理解与医学文本的可复现 early-access 评测。**非英语场景的少有数据点** |
| [**anessbelbati/jev-rerank-bench**](https://github.com/anessbelbati/jev-rerank-bench) | ![](https://badgen.net/github/stars/anessbelbati/jev-rerank-bench) | 重排序对比：原始 provider 响应、打分代码、不确定区间、写明的局限 |
| [**Gaurav-Gosain/jev-sec-bench**](https://github.com/Gaurav-Gosain/jev-sec-bench) | ![](https://badgen.net/github/stars/Gaurav-Gosain/jev-sec-bench) | 公开语料盲测：提示注入与漏洞代码检测 |
| [**TokenTrim/jev-agent-failure-benchmark**](https://github.com/TokenTrim/jev-agent-failure-benchmark) | ![](https://badgen.net/github/stars/TokenTrim/jev-agent-failure-benchmark) | Who&When Pro（注入的 Agent 故障）：预测是谁 / 哪一步 / 哪类错误 |
| [**anisselbd/jev-phishing-bench**](https://github.com/anisselbd/jev-phishing-bench) | ![](https://badgen.net/github/stars/anisselbd/jev-phishing-bench) | 全生态最严谨的一份评测。2000 封钓鱼邮件对比 Claude Haiku 4.5：Jev 直接问「该不该点」只有 **62.6%** 准确率（Haiku 81.3%），但**同一次调用里拆成 5 个信号问题、再做逻辑回归就到 95.0%**。作者还在被质疑后补了三组对照（非 AI 正则基线 91.8%、样本切分、同样问题问 LLM）。延迟 239ms vs 687ms，成本 $0.038 vs $0.462 / 千封 |
| [**bitnovus/jev-spam-eval**](https://github.com/bitnovus/jev-spam-eval) | ![](https://badgen.net/github/stars/bitnovus/jev-spam-eval) | 18,514 封邮件：一段**写出来的**垃圾邮件定义拿到 **98.3%**，和用 ~14,800 条标注训练的 TF-IDF（98.4%）打平，两者平均后 **99.2%**。**最关键的是分布漂移**——换到 2026 年的新邮件，同一个问题仍有 97.3%，TF-IDF 掉到 72.5%。作者自己标注了「判据是看过错误样本后写的」这一 caveat |
| [**teyhouse/jev-secret-detection**](https://github.com/teyhouse/jev-secret-detection) | ![](https://badgen.net/github/stars/teyhouse/jev-secret-detection) | 测量 Jev 在代码片段里识别真实密钥凭证的能力 |
| [**jmanhype/jev-dspy-lab**](https://github.com/jmanhype/jev-dspy-lab) | ![](https://badgen.net/github/stars/jmanhype/jev-dspy-lab) | DSPy 配套评测：录制并重放调用，测校准、选择性风险、置信度弃权、延迟、成本 |

> **中文场景至今没有公开评测。** 谁做过中文分类、内容审核或客服工单的对比测试，欢迎把数据发过来——结论对 Jev 有利还是不利都一样有价值。这是这份列表目前最缺的一块。

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
| [**Anil-matcha/awesome-jev-by-typesafe**](https://github.com/Anil-matcha/awesome-jev-by-typesafe) | ![](https://badgen.net/github/stars/Anil-matcha/awesome-jev-by-typesafe) | 偏用例、模式、prompt 与起步代码 |
| [**AbdelStark/awesome-typesafe**](https://github.com/AbdelStark/awesome-typesafe) | ![](https://badgen.net/github/stars/AbdelStark/awesome-typesafe) | 覆盖整个 TypeSafe / System One，不只 Jev |
| [**yibie/awesome-jev**](https://github.com/yibie/awesome-jev) | ![](https://badgen.net/github/stars/yibie/awesome-jev) | 收录讨论与集成，含社区争论 |
| [**AnotiaWang/awesome-jev**](https://github.com/AnotiaWang/awesome-jev) | ![](https://badgen.net/github/stars/AnotiaWang/awesome-jev) | 结构最完整的一份，本列表的选品参考了它，[有 README_zh](https://github.com/AnotiaWang/awesome-jev/blob/main/README_zh.md) |
| [**hellogumbo/awesome-jev**](https://github.com/hellogumbo/awesome-jev) | ![](https://badgen.net/github/stars/hellogumbo/awesome-jev) | 社区目录站形态 |

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
