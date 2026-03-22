import os
from typing import Optional, Any, AsyncGenerator, Iterator
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

# 修复相对导入：直接使用相对路径，避免从项目根目录找 src
from ..providers import defaults
from .registry import get_provider, get_all_providers

class LLMFactory:
    """
    大模型接入网关核心工厂类
    参考 LiteLLM 架构，提供统一入口，支持同步/异步、流式输出等高级特性。
    """
    
    @staticmethod
    def _resolve_credentials(provider_name: str, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """内部方法：解析厂商凭证，处理兜底逻辑"""
        config = get_provider(provider_name)
        if not config:
            raise ValueError(f"❌ 不支持的模型提供商: '{provider_name}'。当前支持列表: {get_all_providers()}")

        # 1. 解析 Base URL
        resolved_base_url = base_url or os.getenv(f"{provider_name.upper()}_BASE_URL") or config.base_url
        
        # 2. 解析 API Key
        if provider_name == "ollama":
            resolved_api_key = "ollama-local" # 伪造的 key，Ollama 本地不需要
        else:
            # 优先级: 传参 > 厂商专属环境变量 > 全局 OPENAI_API_KEY
            resolved_api_key = api_key or os.getenv(config.env_key_name) or os.getenv("OPENAI_API_KEY")
            
        if not resolved_api_key:
            raise ValueError(
                f"❌ 缺少 {provider_name} 的 API Key！\n"
                f"💡 解决方法：\n"
                f"1. 在 .env 文件中设置 {config.env_key_name}=你的key\n"
                f"2. 或设置全局的 OPENAI_API_KEY=你的key\n"
                f"3. 或通过代码传参 api_key='...'"
            )
            
        return resolved_api_key, resolved_base_url, config.default_model

    @classmethod
    def get_model(
        cls, 
        provider: str = "openai", 
        model_name: Optional[str] = None, 
        temperature: float = 0.1,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        streaming: bool = False,
        **kwargs
    ) -> BaseChatModel:
        """
        获取一个标准的 LangChain ChatModel 对象
        
        Args:
            provider: 厂商名称 (e.g., 'deepseek', 'qwen', 'openai')
            model_name: 具体的模型名。如果不传，则使用厂商的默认模型
            temperature: 生成随机性
            api_key: 优先使用此 key
            base_url: 优先使用此 url
            streaming: 是否开启流式输出
            **kwargs: 传递给 ChatOpenAI 的其他参数 (如 max_tokens 等)
        """
        resolved_api_key, resolved_base_url, default_model = cls._resolve_credentials(provider, api_key, base_url)
        final_model_name = model_name or default_model

        # 统一使用 ChatOpenAI 类（目前国内 99% 的大模型都已兼容此协议）
        return ChatOpenAI(
            model=final_model_name,
            api_key=resolved_api_key,
            base_url=resolved_base_url,
            temperature=temperature,
            streaming=streaming,
            **kwargs
        )

    @classmethod
    def chat(
        cls, 
        prompt: str, 
        provider: str = "openai", 
        model_name: Optional[str] = None, 
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs
    ) -> Any:
        """
        一句话快速调用接口
        
        Args:
            prompt: 用户输入
            provider: 厂商
            stream: 如果为 True，将返回一个生成器，实现打字机效果
        
        Returns:
            如果 stream=False，返回完整的字符串回复。
            如果 stream=True，返回一个生成器(Iterator[str])，用于流式输出。
        """
        model = cls.get_model(
            provider=provider, 
            model_name=model_name, 
            temperature=temperature, 
            streaming=stream,
            **kwargs
        )
        
        if stream:
            # 流式返回
            def generator() -> Iterator[str]:
                for chunk in model.stream(prompt):
                    yield chunk.content
            return generator()
        else:
            # 阻塞返回
            response = model.invoke(prompt)
            return response.content
