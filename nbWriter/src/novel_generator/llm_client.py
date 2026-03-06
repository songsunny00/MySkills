from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .config import LLMConfig
import asyncio

DEFAULT_TIMEOUT = 180

class LLMClient(ABC):
    """LLM客户端抽象基类"""

    def __init__(self, config: LLMConfig, timeout: int = DEFAULT_TIMEOUT):
        self.config = config
        self.timeout = timeout

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文本"""
        pass

    @abstractmethod
    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """流式生成文本"""
        pass


class AnthropicClient(LLMClient):
    """Anthropic Claude客户端"""

    def __init__(self, config: LLMConfig, timeout: int = DEFAULT_TIMEOUT):
        super().__init__(config, timeout)
        try:
            from anthropic import AsyncAnthropic
            kwargs = {"api_key": config.api_key}
            if config.base_url:
                kwargs["base_url"] = config.base_url
            kwargs["timeout"] = timeout
            self.client = AsyncAnthropic(**kwargs)
        except ImportError:
            raise ImportError("请安装 anthropic 包: pip install anthropic")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文本"""
        messages = [{"role": "user", "content": prompt}]

        response = await asyncio.wait_for(
            self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt or "",
                messages=messages
            ),
            timeout=self.timeout
        )

        return response.content[0].text

    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """流式生成文本"""
        messages = [{"role": "user", "content": prompt}]

        async with self.client.messages.stream(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt or "",
            messages=messages
        ) as stream:
            async for text in stream.text_stream:
                yield text


class OpenAIClient(LLMClient):
    """OpenAI客户端"""

    def __init__(self, config: LLMConfig, timeout: int = DEFAULT_TIMEOUT):
        super().__init__(config, timeout)
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                api_key=config.api_key,
                timeout=timeout
            )
        except ImportError:
            raise ImportError("请安装 openai 包: pip install openai")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文本"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await asyncio.wait_for(
            self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            ),
            timeout=self.timeout
        )

        return response.choices[0].message.content

    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """流式生成文本"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content




class DeepSeekClient(LLMClient):
    """DeepSeek客户端（兼容OpenAI接口）"""

    def __init__(self, config: LLMConfig, timeout: int = DEFAULT_TIMEOUT):
        super().__init__(config, timeout)
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                api_key=config.api_key,
                base_url=config.base_url or "https://api.deepseek.com",
                timeout=timeout
            )
        except ImportError:
            raise ImportError("请安装 openai 包: pip install openai")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文本"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await asyncio.wait_for(
            self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            ),
            timeout=self.timeout
        )

        return response.choices[0].message.content

    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None):
        """流式生成文本"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
def create_llm_client(config: LLMConfig) -> LLMClient:
    """工厂函数：根据配置创建LLM客户端"""
    if config.provider == "anthropic":
        return AnthropicClient(config)
    elif config.provider == "openai":
        return OpenAIClient(config)
    elif config.provider == "deepseek":
        return DeepSeekClient(config)
    else:
        raise ValueError(f"不支持的LLM提供商: {config.provider}，支持: anthropic / openai / deepseek")