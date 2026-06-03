"""配置加载与自动生成模块。"""
import os
import sys

try:
    import yaml
except ImportError:
    print("缺少 PyYAML 依赖，请在青龙面板执行: pip install pyyaml")
    sys.exit(1)

_CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG_PATH = os.path.join(_CONFIG_DIR, "roco-merchant.yaml")

DEFAULT_CONFIG = """\
# ===== API 配置 =====
api:
  url: https://wegame.shallow.ink/api/v1/games/rocom/merchant/info
  key: ""

# ===== 推送配置 =====
push:
  title: "📢 远行商人"
  # 启用一言（随机句子），设为 false 关闭
  hitokoto: false
"""


def _generate_config():
    """生成默认配置文件并退出。"""
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(DEFAULT_CONFIG)
    print(f"配置文件已生成: {_CONFIG_PATH}")
    print("请编辑配置文件填写 api.key，然后重新运行脚本。")
    sys.exit(0)


def load_config():
    """加载配置，不存在则自动生成。"""
    if not os.path.exists(_CONFIG_PATH):
        _generate_config()

    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"配置文件格式错误: {e}")
        sys.exit(1)

    if config is None:
        config = {}

    api_config = config.get("api", {})
    if not api_config.get("key"):
        print(f"api.key 未填写，请编辑 {_CONFIG_PATH} 填入 X-API-Key")
        sys.exit(1)

    return config


def get_api_config(config):
    """提取 API 配置，返回 (url, key)。"""
    api = config.get("api", {})
    return api.get("url", ""), api.get("key", "")


def get_push_config(config):
    """提取推送配置。"""
    push = config.get("push", {})
    return {
        "title": push.get("title", "📢 远行商人"),
        "hitokoto": push.get("hitokoto", False),
    }
