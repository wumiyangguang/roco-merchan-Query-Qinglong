"""API 数据获取模块。"""
import requests


def fetch_merchant_data(api_url: str, api_key: str, timeout: int = 30) -> dict:
    """获取远行商人 API 数据。

    Args:
        api_url: API 地址
        api_key: X-API-Key 鉴权密钥
        timeout: 请求超时秒数

    Returns:
        {"code": int, "message": str, "data": dict}

    Raises:
        requests.RequestException: 网络/HTTP 错误
    """
    resp = requests.get(
        api_url,
        headers={"X-API-Key": api_key},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()
