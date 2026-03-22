from ..core.registry import ProviderConfig, register_provider

# ==========================================
# 注册所有主流大模型厂商
# 参考 LiteLLM 架构，我们将各厂商独立注册，便于扩展
# ==========================================

# 1. OpenAI (官方)
register_provider(ProviderConfig(
    name="openai",
    base_url="https://api.openai.com/v1",
    default_model="gpt-4o"
))

# 2. DeepSeek (深度求索)
register_provider(ProviderConfig(
    name="deepseek",
    base_url="https://api.deepseek.com",
    default_model="deepseek-chat"
))

# 3. Qwen (阿里通义千问)
register_provider(ProviderConfig(
    name="qwen",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    default_model="qwen-plus"
))

# 4. Zhipu (智谱 GLM)
register_provider(ProviderConfig(
    name="zhipu",
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    default_model="glm-4"
))

# 5. Moonshot (月之暗面 Kimi)
register_provider(ProviderConfig(
    name="moonshot",
    base_url="https://api.moonshot.cn/v1",
    default_model="moonshot-v1-8k"
))

# 6. SiliconFlow (硅基流动 - 聚合平台)
register_provider(ProviderConfig(
    name="siliconflow",
    base_url="https://api.siliconflow.cn/v1",
    default_model="Qwen/Qwen2.5-7B-Instruct"
))

# 7. Ollama (本地离线部署)
register_provider(ProviderConfig(
    name="ollama",
    base_url="http://localhost:11434/v1",
    default_model="llama3",
    env_key_name="OLLAMA_DUMMY_KEY" # 本地不需要真实 Key
))

# 8. Anthropic (Claude) - 兼容第三方代理中转
register_provider(ProviderConfig(
    name="anthropic",
    base_url="https://api.anthropic.com/v1",  # 默认官方地址，可通过 ANTHROPIC_BASE_URL 覆盖
    default_model="claude-3-5-sonnet-20241022",
    env_key_name="ANTHROPIC_API_KEY"
))

# 9. Local Qwen (内网穿透自建模型)
register_provider(ProviderConfig(
    name="local_qwen",
    base_url="http://localhost/v1",  # 兜底地址，实际从 env 读取
    default_model="/data/models/Qwen/Qwen3-32B",
    env_key_name="LOCAL_QWEN_API_KEY"
))
