"""
LLM 提供商统一接口
支持 OpenAI 兼容格式的所有 API
"""

import os
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class LLMProvider(Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ZHIPU = "zhipu"        # 智谱 GLM
    ALI = "ali"             # 阿里通义千问
    BAIDU = "baidu"         # 百度文心一言
    MINIMAX = "minimax"
    SILICONFLOW = "siliconflow"
    GROQ = "groq"
    GEMINI = "gemini"


@dataclass
class LLMConfig:
    provider: LLMProvider
    api_key: str
    base_url: str
    model: str


# 各 provider 配置
PROVIDER_CONFIGS = {
    LLMProvider.OPENAI: {
        "name": "OpenAI",
        "default_model": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
    },
    LLMProvider.DEEPSEEK: {
        "name": "DeepSeek",
        "default_model": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1",
        "models": ["deepseek-chat", "deepseek-coder"]
    },
    LLMProvider.ZHIPU: {
        "name": "智谱 GLM",
        "default_model": "glm-4",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "models": ["glm-4", "glm-4-flash", "glm-3-turbo"]
    },
    LLMProvider.ALI: {
        "name": "阿里通义千问",
        "default_model": "qwen-turbo",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": ["qwen-turbo", "qwen-plus", "qwen-max"]
    },
    LLMProvider.BAIDU: {
        "name": "百度文心一言",
        "default_model": "ernie-4.0-8k-latest",
        "base_url": "https://qianfan.baidubce.com/v2",
        "models": ["ernie-4.0-8k-latest", "ernie-3.5-8k", "ernie-speed-128k"]
    },
    LLMProvider.MINIMAX: {
        "name": "MiniMax",
        "default_model": "MiniMax-Text-01",
        "base_url": "https://api.minimax.chat/v1",
        "models": ["MiniMax-Text-01", "abab6.5s-chat"]
    },
    LLMProvider.SILICONFLOW: {
        "name": "SiliconFlow",
        "default_model": "Qwen/Qwen2.5-72B-Instruct",
        "base_url": "https://api.siliconflow.cn/v1",
        "models": ["Qwen/Qwen2.5-72B-Instruct", "deepseek-ai/DeepSeek-V2.5", "anthropic/claude-3.5-sonnet"]
    },
    LLMProvider.GROQ: {
        "name": "Groq",
        "default_model": "llama-3.1-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1",
        "models": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    },
    LLMProvider.GEMINI: {
        "name": "Google Gemini",
        "default_model": "gemini-2.0-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
    },
}


def get_llm_config(provider: str, api_key: str, model: Optional[str] = None) -> LLMConfig:
    """获取 LLM 配置"""
    provider_enum = LLMProvider(provider.lower())

    if provider_enum not in PROVIDER_CONFIGS:
        raise ValueError(f"不支持的 provider: {provider}")

    config = PROVIDER_CONFIGS[provider_enum]
    selected_model = model or config["default_model"]

    # 特殊处理：MiniMax API key 格式
    if provider_enum == LLMProvider.MINIMAX:
        # MiniMax 需要 group_id
        base_url = config["base_url"]
    elif provider_enum == LLMProvider.GEMINI:
        # Gemini 的 API key 是放在 URL 里的
        base_url = f"{config['base_url']}/models?key={api_key}"
    else:
        base_url = config["base_url"]

    return LLMConfig(
        provider=provider_enum,
        api_key=api_key,
        base_url=config["base_url"],
        model=selected_model
    )


def create_llm_client(config: LLMConfig):
    """创建 LLM 客户端（使用 OpenAI 兼容格式）"""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("请安装 openai 包: pip install openai")

    return OpenAI(
        api_key=config.api_key,
        base_url=config.base_url
    )


def call_llm(client, model: str, system: str, user_message: str, max_tokens: int = 8192) -> str:
    """调用 LLM"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def list_providers():
    """列出所有支持的 provider"""
    result = []
    for provider, config in PROVIDER_CONFIGS.items():
        result.append({
            "id": provider.value,
            "name": config["name"],
            "models": config["models"],
            "default": config["default_model"]
        })
    return result
