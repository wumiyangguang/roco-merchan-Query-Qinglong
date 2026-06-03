#!/usr/bin/env python3
"""远行商人查询 — 青龙面板脚本入口。"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from core.config import load_config, get_api_config, get_push_config
from core.fetcher import fetch_merchant_data
from core.processor import process_merchant_data
from notify import send


def build_message(processed: dict) -> str:
    """将结构化数据组装为纯文本推送内容。"""
    round_info = processed.get("round_info", {})
    products = processed.get("products", [])

    lines = [
        f"第 {round_info.get('current', '?')}/{round_info.get('total', '?')} 轮 "
        f"| 剩余 {round_info.get('countdown', '未知')}",
        "",
    ]

    if products:
        names = []
        for p in products:
            name = p["name"]
            price = p.get("price")
            if price is not None and price != "":
                names.append(f"{name}({price}金币)")
            else:
                names.append(name)
        lines.append(f"当前售卖: {'、'.join(names)}")
    else:
        lines.append("当前暂无商品")

    return "\n".join(lines)


def main():
    cfg = load_config()
    api_url, api_key = get_api_config(cfg)
    push_cfg = get_push_config(cfg)

    try:
        raw = fetch_merchant_data(api_url, api_key)
    except Exception as e:
        send(f"{push_cfg['title']} 监控异常", f"请求失败: {e}")
        return

    if raw.get("code") != 0:
        send(
            f"{push_cfg['title']} API 错误",
            raw.get("message", "未知错误"),
        )
        return

    data = raw.get("data")
    if not data:
        send(f"{push_cfg['title']} 数据为空", "API 返回的 data 字段为空")
        return

    processed = process_merchant_data(data)
    body = build_message(processed)
    send(push_cfg["title"], body)


if __name__ == "__main__":
    main()
