"""LLM服务模块"""
from ..config import get_settings
from langchain.chat_models import init_chat_model


# 全局LLM实例
_llm_instance = None

def get_llm(model_provider, model, api_key, base_url):
    """
    获取LLM实例(单例模式)
    
    Returns:
        LangchainModel实例
    """
    global _llm_instance
    
    if _llm_instance is None:
        _llm_instance =  init_chat_model(
            model_provider=model_provider or "openai",
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        print(f"✅ LLM服务初始化成功")
        # print(f"   提供商: {_llm_instance.model_pro}")
        print(f"   模型: {_llm_instance.model}")
    return _llm_instance


def reset_llm():
    """重置LLM实例(用于测试或重新配置)"""
    global _llm_instance
    _llm_instance = None
