# LLM Gateway Lite (轻量级大模型统一接入网关)

一个极简、开箱即用的 Python 大模型网关。灵感来源于 LiteLLM，但更加轻量，专注于将不同厂商的大模型 API 统一封装为标准接口，极大降低开发者的接入成本。

## 🌟 核心特性

- **一键统一调用**：屏蔽了不同厂商（OpenAI, DeepSeek, Qwen, Claude 等）的 Base URL 和参数差异。
- **LangChain 原生兼容**：无缝对接 `langchain-openai`，一行代码获取标准 `ChatOpenAI` 实例，方便后续绑定 Tool 或构建 Agent。
- **开闭原则设计**：通过 Registry 模式，您可以随时在 `providers` 目录中注册自己公司内部的私有模型或新的中转代理。
- **原生支持流式输出**：完美支持 Generator 流式打字机效果。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填入你需要使用的厂商 API Key。

```bash
cp .env.example .env
```

例如，如果你只使用 OpenAI 格式的中转服务：
```env
OPENAI_API_KEY="你的中转Key"
OPENAI_BASE_URL="https://api.your-proxy.com/v1"
```

### 3. 使用方法

**场景 A：我只想要个最简单的纯文本对话**

```python
from src.llm_gateway import chat_with_llm

# 直接提问，默认使用 openai 供应商
reply = chat_with_llm(prompt="讲个笑话", provider="openai")
print(reply)

# 开启打字机效果 (流式输出)
stream = chat_with_llm(prompt="写一首诗", provider="deepseek", stream=True)
for chunk in stream:
    print(chunk, end="", flush=True)
```

**场景 B：我是高级玩家，需要做 Agent 开发**

```python
from src.llm_gateway import get_model

# 获取一个标准的 LangChain ChatModel
llm = get_model(provider="local_qwen")

# 接下来你可以随意使用 .bind_tools(), .invoke() 等高级功能
response = llm.invoke("你好")
print(response.content)
```

## 🛠️ 如何添加新的模型厂商？

如果你有一个特殊的本地模型或新的中转服务，只需要在 `src/llm_gateway/providers/defaults.py` 中注册它即可：

```python
from ..core.registry import ProviderConfig, register_provider

register_provider(ProviderConfig(
    name="my_company_model",
    base_url="http://internal.company.com/v1",
    default_model="custom-llama-3",
    env_key_name="MY_COMPANY_KEY"
))
```
然后你就可以直接在代码里使用 `provider="my_company_model"` 啦！

## 📄 测试

你可以直接运行项目根目录下的 `demo.py` 来体验效果：

```bash
python demo.py
```
