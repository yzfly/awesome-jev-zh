#!/usr/bin/env python3
"""中文工单决策横评：同一份数据、同两道题，跑遍各家 Jev 类决策 API。

只用标准库。每个 provider 读自己的环境变量，没配 key 的自动跳过。

    python bench/vendor_bench.py --list                 # 看哪些 provider 可跑
    python bench/vendor_bench.py                        # 跑全部已配置的
    python bench/vendor_bench.py -p openrouter:typesafe/jev-1.14 -p bailian

每条工单一次请求，同时问两题：
  dept    choice  billing / technical / sales / account
  urgent  noul    是否紧急（>0.5 记为 true）
结果写到 bench/results/<UTC 日期>.json 和同名 .md。
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "zh_tickets.jsonl"

DEPT = {
    "billing": "支付、扣款、发票、退款、优惠券、订阅账单",
    "technical": "产品故障、Bug、接口报错、性能、集成问题",
    "sales": "价格咨询、采购、套餐、演示、商务合作",
    "account": "登录、密码、权限、账号安全、账号设置",
}
DEPT_Q = "这条客服工单应该派给哪个组"
URGENT_Q = "这条工单是否紧急：正在造成业务中断、资金损失、安全风险，或明确给出了很近的截止时间"

# OpenRouter Decisions 上的模型（2026-11-03 rankings/decisions 前列 + 大厂）
OPENROUTER_MODELS = [
    "typesafe/jev-1.14",
    "typesafe/jev-1.13",
    "openai/gpt-6-luna-decisions",
    "microsoft/microsoft-decision-1",
    "perplexity/pplx-decider-v1.2",
    "cloudflare/clef-flash",
    "inception/mercury-decide",
    "liquid/d1-ultra",
    "nace-ai/drex-v1.5",
]


def systemone_body(model: str | None, text: str) -> dict:
    body = {
        "state": {"ticket": text},
        "questions": {
            "dept": {"type": "choice", "instructions": DEPT_Q, "criteria": DEPT},
            "urgent": {"type": "noul", "instructions": URGENT_Q},
        },
    }
    if model:
        body["model"] = model
    return body


def openai_body(model: str, text: str) -> dict:
    return {
        "model": model,
        "input": text,
        "questions": [
            {
                "name": "dept",
                "type": "choice",
                "instructions": DEPT_Q,
                "choices": [{"value": k, "description": v} for k, v in DEPT.items()],
            },
            {"name": "urgent", "type": "predicate", "instructions": URGENT_Q},
        ],
    }


def parse_systemone(resp: dict) -> dict:
    a = resp["answers"]
    d, u = a["dept"], a["urgent"]
    return {
        "dept": d.get("choice"),
        "dept_conf": d.get("confidence"),
        "urgent_p": u.get("noul", u.get("probability")),
        "input_tokens": (resp.get("usage") or {}).get("input_tokens"),
        "cost": (resp.get("usage") or {}).get("cost"),
        "model_echo": resp.get("model"),
    }


def parse_openai(resp: dict) -> dict:
    a = {x["name"]: x for x in resp["answers"]}
    d, u = a["dept"], a["urgent"]
    return {
        "dept": d.get("choice"),
        "dept_conf": d.get("confidence"),
        "urgent_p": u.get("probability"),
        "input_tokens": (resp.get("usage") or {}).get("input_tokens"),
        "cost": None,
        "model_echo": resp.get("model"),
    }


def providers() -> dict:
    """name -> (needed env, url, key env, body fn, parse fn)"""
    p = {
        "typesafe": ("TYPESAFE_API_KEY", "https://api.typesafe.ai/v1/systemone", "TYPESAFE_API_KEY",
                     lambda t: systemone_body("jev-latest", t), parse_systemone),
        "openai": ("OPENAI_API_KEY", "https://api.openai.com/v1/decisions", "OPENAI_API_KEY",
                   lambda t: openai_body("gpt-6-luna", t), parse_openai),
        "perplexity": ("PERPLEXITY_API_KEY", "https://api.perplexity.ai/v1/decisions", "PERPLEXITY_API_KEY",
                       lambda t: systemone_body("pplx-decider-v1.2", t), parse_systemone),
        # 百炼：BAILIAN_BASE_URL=https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
        "bailian": ("BAILIAN_BASE_URL", os.environ.get("BAILIAN_BASE_URL", "").rstrip("/") + "/systemone",
                    "DASHSCOPE_API_KEY", lambda t: systemone_body("decision-model-preview", t), parse_systemone),
        # 火山方舟 System One API（beta），需额外请求头 ark-beta-systemone-api: true
        "volcengine": ("ARK_API_KEY", "https://ark.cn-beijing.volces.com/api/v1/systemone", "ARK_API_KEY",
                       lambda t: systemone_body("doubao-seed-2-1-lite-260915", t), parse_systemone),
        # 任意本地 /v1/systemone：kev / laya(EdgeJev) / strands-decider / Clef 自托管
        "local": ("LOCAL_SYSTEMONE_URL", os.environ.get("LOCAL_SYSTEMONE_URL", ""), None,
                  lambda t: systemone_body(os.environ.get("LOCAL_SYSTEMONE_MODEL"), t), parse_systemone),
    }
    for m in OPENROUTER_MODELS:
        p[f"openrouter:{m}"] = ("OPENROUTER_API_KEY", "https://openrouter.ai/api/alpha/decisions",
                                "OPENROUTER_API_KEY", (lambda mm: lambda t: systemone_body(mm, t))(m),
                                parse_systemone)
    return p


def call(url: str, key_env: str | None, body: dict, timeout: float = 60) -> tuple[dict, float]:
    headers = {"Content-Type": "application/json", "User-Agent": "awesome-jev-zh-bench/1.0"}
    if key_env:
        headers["Authorization"] = f"Bearer {os.environ[key_env]}"
    if "volces.com" in url:
        headers["ark-beta-systemone-api"] = "true"
    req = urllib.request.Request(url, json.dumps(body, ensure_ascii=False).encode(), headers)
    for attempt in range(4):
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.load(r)
            return data, (time.perf_counter() - t0) * 1000
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 529) and attempt < 3:
                time.sleep(2 ** attempt * 2)
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}") from None
    raise RuntimeError("unreachable")


def ece(confs: list[float], hits: list[bool], bins: int = 5) -> float:
    total, err = len(confs), 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, c in enumerate(confs) if lo <= c < hi or (b == bins - 1 and c == 1.0)]
        if idx:
            acc = sum(hits[i] for i in idx) / len(idx)
            conf = sum(confs[i] for i in idx) / len(idx)
            err += len(idx) / total * abs(acc - conf)
    return err


def run(name: str, spec, rows: list[dict]) -> dict:
    _, url, key_env, body_fn, parse_fn = spec
    recs, errors = [], []
    for r in rows:
        try:
            resp, ms = call(url, key_env, body_fn(r["text"]))
            out = parse_fn(resp)
            out.update(id=r["id"], ms=ms, dept_gold=r["dept"], urgent_gold=r["urgent"])
            recs.append(out)
        except Exception as e:  # noqa: BLE001 — 记录后继续跑下一条
            errors.append({"id": r["id"], "error": str(e)[:300]})
        print(f"\r{name}: {len(recs) + len(errors)}/{len(rows)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    if not recs:
        return {"provider": name, "n": 0, "errors": errors}
    dept_hit = [x["dept"] == x["dept_gold"] for x in recs]
    urg_hit = [(x["urgent_p"] is not None and x["urgent_p"] > 0.5) == x["urgent_gold"] for x in recs]
    confs = [x["dept_conf"] for x in recs if x["dept_conf"] is not None]
    ms = sorted(x["ms"] for x in recs)
    costs = [x["cost"] for x in recs if x["cost"] is not None]
    return {
        "provider": name,
        "model_echo": recs[0].get("model_echo"),
        "n": len(recs),
        "errors": errors,
        "dept_acc": sum(dept_hit) / len(recs),
        "urgent_acc": sum(urg_hit) / len(recs),
        "dept_conf_mean": statistics.mean(confs) if confs else None,
        "dept_ece": ece(confs, [h for h, x in zip(dept_hit, recs) if x["dept_conf"] is not None]) if confs else None,
        "p50_ms": statistics.median(ms),
        "p95_ms": ms[min(len(ms) - 1, int(len(ms) * 0.95))],
        "input_tokens_mean": statistics.mean([x["input_tokens"] for x in recs if x["input_tokens"]] or [0]),
        "cost_per_1k_req": (sum(costs) / len(costs) * 1000) if costs else None,
        "misses": [{"id": x["id"], "gold": x["dept_gold"], "got": x["dept"], "conf": x["dept_conf"]}
                   for x, h in zip(recs, dept_hit) if not h],
        "records": recs,
    }


def to_md(results: list[dict], date: str) -> str:
    f = lambda v, p="{:.1%}": "—" if v is None else p.format(v)  # noqa: E731
    lines = [f"# 中文工单决策横评 · {date} (UTC)", "",
             "| Provider | 实际模型 | n | 路由准确率 | 紧急度准确率 | 平均置信度 | ECE | p50 | p95 | 每千次成本 | 错误 |",
             "| :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: |"]
    for r in results:
        if not r["n"]:
            lines.append(f"| {r['provider']} | — | 0 | — | — | — | — | — | — | — | {len(r['errors'])} |")
            continue
        lines.append(
            f"| {r['provider']} | `{r['model_echo']}` | {r['n']} | {f(r['dept_acc'])} | {f(r['urgent_acc'])} | "
            f"{f(r['dept_conf_mean'], '{:.2f}')} | {f(r['dept_ece'], '{:.3f}')} | {r['p50_ms']:.0f} ms | "
            f"{r['p95_ms']:.0f} ms | {f(r['cost_per_1k_req'], '${:.4f}')} | {len(r['errors'])} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--provider", action="append", help="只跑指定 provider，可重复")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    specs = providers()
    ready = {k: v for k, v in specs.items() if os.environ.get(v[0]) and (not v[2] or os.environ.get(v[2]))}
    if a.list:
        for k, v in specs.items():
            print(("✓ " if k in ready else "· ") + k + ("" if k in ready else f"  (需要 {v[0]}{'' if not v[2] or v[2] == v[0] else ' + ' + v[2]})"))
        return
    chosen = a.provider or list(ready)
    missing = [c for c in chosen if c not in ready]
    if missing:
        sys.exit(f"未配置：{missing}，先 --list 看需要哪些环境变量")
    rows = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]
    results = [run(c, specs[c], rows) for c in chosen]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / f"{date}.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))
    md = to_md(results, date)
    (out / f"{date}.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
