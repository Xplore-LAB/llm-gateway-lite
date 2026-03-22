"""
大模型统一接入网关 (LLM Gateway)

核心功能：
1. 统一接口：将各大厂商的 API 统一封装。
2. 简易调用：提供简单的 get_model 和 chat_with_llm 接口。
3. 易于扩展：通过 providers 目录轻松添加新厂商支持。

使用方法：
from src.llm_gateway import chat_with_llm, get_model
"""

from .core.factory import LLMFactory

# 暴露快捷接口
chat_with_llm = LLMFactory.chat
get_model = LLMFactory.get_model

__all__ = ["LLMFactory", "chat_with_llm", "get_model"]
