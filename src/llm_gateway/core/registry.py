from typing import Dict, Any, Optional

class ProviderConfig:
    """定义一个模型厂商的基本配置"""
    def __init__(self, name: str, base_url: str, default_model: str, env_key_name: Optional[str] = None):
        self.name = name.lower()
        self.base_url = base_url
        self.default_model = default_model
        # 如果没有指定环境变量名，默认按大写厂商名 + _API_KEY 的规则，例如 OPENAI_API_KEY
        self.env_key_name = env_key_name or f"{self.name.upper()}_API_KEY"

# 全局注册表，存放所有支持的厂商
_PROVIDERS: Dict[str, ProviderConfig] = {}

def register_provider(config: ProviderConfig):
    """注册一个新的模型厂商"""
    _PROVIDERS[config.name] = config

def get_provider(name: str) -> Optional[ProviderConfig]:
    """获取厂商配置"""
    return _PROVIDERS.get(name.lower())

def get_all_providers() -> list[str]:
    """获取所有已注册的厂商名称"""
    return list(_PROVIDERS.keys())
