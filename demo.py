import os
import sys
from dotenv import load_dotenv

# 确保能找到 src 目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.llm_gateway import chat_with_llm, get_model

def demo_simple_io():
    """演示场景 1：最简单的纯文本 IO"""
    print("\n--- 场景 1: 简单的纯文本聊天 ---")
    prompt = "请用一句话解释什么是大语言模型？"
    print(f"🧑 提问: {prompt}")
    
    try:
        # 演示使用本地内网穿透 Qwen 接口 (或者改为 openai, deepseek 等)
        reply = chat_with_llm(
            prompt=prompt, 
            provider="local_qwen"
        )
        print(f"🤖 回复: {reply}")
    except Exception as e:
        print(f"❌ 调用失败: {e}")

def demo_streaming_io():
    """演示场景 2：流式输出 (打字机效果)"""
    print("\n--- 场景 2: 流式打字机效果 ---")
    prompt = "写一首关于春天的短诗（4行即可）"
    print(f"🧑 提问: {prompt}\n🤖 回复: ", end="", flush=True)
    
    try:
        # 开启 stream=True，返回的是一个生成器
        stream_generator = chat_with_llm(
            prompt=prompt, 
            provider="local_qwen",
            stream=True
        )
        for chunk in stream_generator:
            print(chunk, end="", flush=True)
        print() # 换行
    except Exception as e:
        print(f"\n❌ 调用失败: {e}")

def demo_agent_usage():
    """演示场景 3：获取标准 LangChain 模型用于高级开发"""
    print("\n--- 场景 3: 获取 LangChain 模型用于复杂开发 ---")
    try:
        llm = get_model(provider="local_qwen")
        
        messages = [
            ("system", "你是一个幽默的助手。"),
            ("human", "写一个关于程序员的笑话。")
        ]
        response = llm.invoke(messages)
        print(f"🤖 幽默回复: {response.content}")
        
    except Exception as e:
        print(f"❌ 调用失败: {e}")

if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    print("🚀 欢迎使用【大模型统一接入网关】测试程序！")
    print("💡 提示：请确保您已经在项目根目录的 .env 文件中配置了相应的 API_KEY\n")
    
    demo_simple_io()
    demo_streaming_io()
    demo_agent_usage()
