"""
vLLM客户端封装类和连接管理
vLLM client wrapper and connection management
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List, AsyncGenerator, Union
import httpx
import json
from contextlib import asynccontextmanager

from .config import VLLMConfig, GenerationConfig
from .models import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    ChatMessage,
    GenerationRequest,
    GenerationResponse,
    ModelInfo,
    HealthResponse
)

logger = logging.getLogger(__name__)


class VLLMConnectionError(Exception):
    """vLLM连接错误"""
    pass


class VLLMTimeoutError(Exception):
    """vLLM超时错误"""
    pass


class VLLMClient:
    """vLLM客户端类"""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:8001",
        api_key: Optional[str] = None,
        timeout: float = 300.0,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # HTTP客户端配置
        self._client: Optional[httpx.AsyncClient] = None
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": "vLLM-Client/1.0.0"
        }
        
        if self.api_key:
            self._headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
    
    async def _ensure_client(self):
        """确保HTTP客户端已初始化"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers=self._headers,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
            )
    
    async def close(self):
        """关闭客户端连接"""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Union[Dict[str, Any], AsyncGenerator[str, None]]:
        """发送HTTP请求"""
        await self._ensure_client()
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries + 1):
            try:
                if stream:
                    # 流式请求
                    async with self._client.stream(
                        method, url, json=data
                    ) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                yield line[6:]  # 移除"data: "前缀
                    return
                else:
                    # 普通请求
                    response = await self._client.request(method, url, json=data)
                    response.raise_for_status()
                    return response.json()
                    
            except httpx.TimeoutException as e:
                if attempt == self.max_retries:
                    raise VLLMTimeoutError(f"请求超时: {e}")
                logger.warning(f"请求超时，重试 {attempt + 1}/{self.max_retries}")
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.max_retries:
                    logger.warning(f"服务器错误，重试 {attempt + 1}/{self.max_retries}: {e}")
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                raise VLLMConnectionError(f"HTTP错误 {e.response.status_code}: {e.response.text}")
                
            except Exception as e:
                if attempt == self.max_retries:
                    raise VLLMConnectionError(f"连接错误: {e}")
                logger.warning(f"连接错误，重试 {attempt + 1}/{self.max_retries}: {e}")
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
    
    async def health_check(self) -> HealthResponse:
        """健康检查"""
        try:
            response = await self._make_request("GET", "/health")
            return HealthResponse(**response)
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            raise
    
    async def list_models(self) -> List[ModelInfo]:
        """列出可用模型"""
        try:
            response = await self._make_request("GET", "/v1/models")
            return [ModelInfo(**model) for model in response.get("data", [])]
        except Exception as e:
            logger.error(f"获取模型列表失败: {e}")
            raise
    
    async def chat_completion(
        self, 
        messages: List[ChatMessage],
        model: str = "default",
        **kwargs
    ) -> ChatCompletionResponse:
        """聊天完成（非流式）"""
        request = ChatCompletionRequest(
            model=model,
            messages=messages,
            stream=False,
            **kwargs
        )
        
        try:
            response = await self._make_request(
                "POST", "/v1/chat/completions", request.dict()
            )
            return ChatCompletionResponse(**response)
        except Exception as e:
            logger.error(f"聊天完成请求失败: {e}")
            raise
    
    async def chat_completion_stream(
        self, 
        messages: List[ChatMessage],
        model: str = "default",
        **kwargs
    ) -> AsyncGenerator[ChatCompletionResponse, None]:
        """聊天完成（流式）"""
        request = ChatCompletionRequest(
            model=model,
            messages=messages,
            stream=True,
            **kwargs
        )
        
        try:
            async for line in self._make_request(
                "POST", "/v1/chat/completions", request.dict(), stream=True
            ):
                if line.strip() == "[DONE]":
                    break
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "error" in data:
                            raise VLLMConnectionError(f"流式响应错误: {data['error']}")
                        yield ChatCompletionResponse(**data)
                    except json.JSONDecodeError:
                        logger.warning(f"无法解析流式响应: {line}")
                        continue
        except Exception as e:
            logger.error(f"流式聊天完成请求失败: {e}")
            raise
    
    async def generate(
        self, 
        prompt: str,
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> GenerationResponse:
        """通用文本生成"""
        generation_config = config or GenerationConfig()
        
        # 转换为聊天格式
        messages = [ChatMessage(role="user", content=prompt)]
        
        # 合并配置
        params = generation_config.to_dict()
        params.update(kwargs)
        
        try:
            response = await self.chat_completion(messages, **params)
            
            if response.choices:
                choice = response.choices[0]
                return GenerationResponse(
                    text=choice.message.content if choice.message else "",
                    finish_reason=choice.finish_reason,
                    usage=response.usage,
                    request_id=response.id
                )
            else:
                raise VLLMConnectionError("生成响应为空")
                
        except Exception as e:
            logger.error(f"文本生成失败: {e}")
            raise
    
    async def generate_stream(
        self, 
        prompt: str,
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """流式文本生成"""
        generation_config = config or GenerationConfig()
        
        # 转换为聊天格式
        messages = [ChatMessage(role="user", content=prompt)]
        
        # 合并配置
        params = generation_config.to_dict()
        params.update(kwargs)
        
        try:
            async for response in self.chat_completion_stream(messages, **params):
                if response.choices:
                    choice = response.choices[0]
                    if choice.delta and choice.delta.content:
                        yield choice.delta.content
        except Exception as e:
            logger.error(f"流式文本生成失败: {e}")
            raise


class VLLMConnectionPool:
    """vLLM连接池"""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:8001",
        api_key: Optional[str] = None,
        pool_size: int = 10,
        timeout: float = 300.0,
        max_retries: int = 3
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.pool_size = pool_size
        self.timeout = timeout
        self.max_retries = max_retries
        
        self._pool: List[VLLMClient] = []
        self._available: asyncio.Queue = asyncio.Queue(maxsize=pool_size)
        self._initialized = False
    
    async def initialize(self):
        """初始化连接池"""
        if self._initialized:
            return
        
        for _ in range(self.pool_size):
            client = VLLMClient(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
            self._pool.append(client)
            await self._available.put(client)
        
        self._initialized = True
        logger.info(f"vLLM连接池初始化完成，池大小: {self.pool_size}")
    
    @asynccontextmanager
    async def get_client(self) -> VLLMClient:
        """获取客户端连接"""
        if not self._initialized:
            await self.initialize()
        
        # 从池中获取客户端
        client = await self._available.get()
        try:
            yield client
        finally:
            # 归还客户端到池中
            await self._available.put(client)
    
    async def close(self):
        """关闭连接池"""
        for client in self._pool:
            await client.close()
        self._pool.clear()
        self._initialized = False
        logger.info("vLLM连接池已关闭")


# 全局连接池实例
_global_pool: Optional[VLLMConnectionPool] = None


async def get_vllm_client() -> VLLMClient:
    """获取全局vLLM客户端"""
    global _global_pool
    
    if _global_pool is None:
        _global_pool = VLLMConnectionPool()
        await _global_pool.initialize()
    
    return _global_pool.get_client()


async def close_global_pool():
    """关闭全局连接池"""
    global _global_pool
    
    if _global_pool:
        await _global_pool.close()
        _global_pool = None