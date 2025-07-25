"""
流式响应处理和错误重试机制
Streaming response handling and error retry mechanism
"""

import asyncio
import logging
import json
import time
from typing import AsyncGenerator, Optional, Dict, Any, Callable, List
from dataclasses import dataclass
from enum import Enum
import httpx

from .models import ChatCompletionResponse, ChatMessage
from .client import VLLMConnectionError, VLLMTimeoutError

logger = logging.getLogger(__name__)


class RetryStrategy(Enum):
    """重试策略枚举"""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_DELAY = "fixed_delay"
    LINEAR_BACKOFF = "linear_backoff"


@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retry_on_timeout: bool = True
    retry_on_connection_error: bool = True
    retry_on_server_error: bool = True
    backoff_multiplier: float = 2.0


@dataclass
class StreamingStats:
    """流式统计信息"""
    start_time: float
    end_time: Optional[float] = None
    total_tokens: int = 0
    chunks_received: int = 0
    errors_count: int = 0
    retries_count: int = 0
    
    @property
    def duration(self) -> Optional[float]:
        """获取持续时间"""
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    @property
    def tokens_per_second(self) -> Optional[float]:
        """获取每秒token数"""
        if self.duration and self.duration > 0:
            return self.total_tokens / self.duration
        return None


class StreamingError(Exception):
    """流式处理错误"""
    pass


class StreamingTimeoutError(StreamingError):
    """流式超时错误"""
    pass


class StreamingConnectionError(StreamingError):
    """流式连接错误"""
    pass


class StreamingHandler:
    """流式响应处理器"""
    
    def __init__(
        self,
        retry_config: Optional[RetryConfig] = None,
        timeout: float = 300.0,
        chunk_timeout: float = 30.0
    ):
        self.retry_config = retry_config or RetryConfig()
        self.timeout = timeout
        self.chunk_timeout = chunk_timeout
        self.stats = StreamingStats(start_time=time.time())
        
        # 回调函数
        self.on_chunk_received: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        self.on_retry: Optional[Callable[[int, Exception], None]] = None
        self.on_complete: Optional[Callable[[StreamingStats], None]] = None
    
    def _calculate_delay(self, attempt: int) -> float:
        """计算重试延迟"""
        if self.retry_config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = self.retry_config.base_delay * (
                self.retry_config.backoff_multiplier ** attempt
            )
        elif self.retry_config.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = self.retry_config.base_delay * (attempt + 1)
        else:  # FIXED_DELAY
            delay = self.retry_config.base_delay
        
        return min(delay, self.retry_config.max_delay)
    
    def _should_retry(self, error: Exception, attempt: int) -> bool:
        """判断是否应该重试"""
        if attempt >= self.retry_config.max_retries:
            return False
        
        if isinstance(error, VLLMTimeoutError):
            return self.retry_config.retry_on_timeout
        elif isinstance(error, VLLMConnectionError):
            return self.retry_config.retry_on_connection_error
        elif isinstance(error, httpx.HTTPStatusError):
            return (
                self.retry_config.retry_on_server_error and 
                error.response.status_code >= 500
            )
        
        return False
    
    async def _handle_stream_chunk(self, chunk: str) -> Optional[Dict[str, Any]]:
        """处理流式数据块"""
        try:
            # 更新统计信息
            self.stats.chunks_received += 1
            
            # 跳过空行和注释
            chunk = chunk.strip()
            if not chunk or chunk.startswith('#'):
                return None
            
            # 处理结束标记
            if chunk == "[DONE]":
                return {"done": True}
            
            # 解析JSON数据
            try:
                data = json.loads(chunk)
            except json.JSONDecodeError as e:
                logger.warning(f"无法解析流式数据块: {chunk}, 错误: {e}")
                return None
            
            # 检查错误
            if "error" in data:
                error_msg = data["error"].get("message", "未知错误")
                raise StreamingError(f"服务器返回错误: {error_msg}")
            
            # 调用回调函数
            if self.on_chunk_received:
                self.on_chunk_received(chunk)
            
            return data
            
        except Exception as e:
            self.stats.errors_count += 1
            if self.on_error:
                self.on_error(e)
            raise
    
    async def process_stream(
        self, 
        stream_generator: AsyncGenerator[str, None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """处理流式数据"""
        attempt = 0
        
        while attempt <= self.retry_config.max_retries:
            try:
                # 设置超时
                timeout_task = asyncio.create_task(
                    asyncio.sleep(self.timeout)
                )
                stream_task = asyncio.create_task(
                    self._process_stream_internal(stream_generator)
                )
                
                try:
                    async for chunk_data in stream_task:
                        # 检查是否完成
                        if chunk_data.get("done"):
                            break
                        
                        yield chunk_data
                        
                        # 重置chunk超时
                        if not timeout_task.done():
                            timeout_task.cancel()
                            timeout_task = asyncio.create_task(
                                asyncio.sleep(self.chunk_timeout)
                            )
                    
                    # 成功完成
                    break
                    
                except asyncio.TimeoutError:
                    raise StreamingTimeoutError("流式处理超时")
                finally:
                    if not timeout_task.done():
                        timeout_task.cancel()
                    if not stream_task.done():
                        stream_task.cancel()
                
            except Exception as e:
                if not self._should_retry(e, attempt):
                    raise
                
                # 执行重试
                attempt += 1
                self.stats.retries_count += 1
                
                if self.on_retry:
                    self.on_retry(attempt, e)
                
                delay = self._calculate_delay(attempt - 1)
                logger.warning(
                    f"流式处理失败，{delay}秒后重试 ({attempt}/{self.retry_config.max_retries}): {e}"
                )
                await asyncio.sleep(delay)
        
        # 更新完成时间
        self.stats.end_time = time.time()
        
        if self.on_complete:
            self.on_complete(self.stats)
    
    async def _process_stream_internal(
        self, 
        stream_generator: AsyncGenerator[str, None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """内部流式处理逻辑"""
        async for chunk in stream_generator:
            chunk_data = await self._handle_stream_chunk(chunk)
            if chunk_data:
                yield chunk_data


class StreamingResponseProcessor:
    """流式响应处理器"""
    
    def __init__(
        self,
        retry_config: Optional[RetryConfig] = None,
        buffer_size: int = 1024,
        enable_stats: bool = True
    ):
        self.retry_config = retry_config or RetryConfig()
        self.buffer_size = buffer_size
        self.enable_stats = enable_stats
        
        # 缓冲区
        self._buffer: List[str] = []
        self._buffer_size = 0
        
        # 统计信息
        self.stats = StreamingStats(start_time=time.time()) if enable_stats else None
    
    async def process_chat_stream(
        self,
        stream_generator: AsyncGenerator[str, None],
        model_name: str = "default"
    ) -> AsyncGenerator[ChatCompletionResponse, None]:
        """处理聊天流式响应"""
        handler = StreamingHandler(
            retry_config=self.retry_config,
            timeout=300.0,
            chunk_timeout=30.0
        )
        
        # 设置回调函数
        if self.enable_stats:
            handler.on_chunk_received = self._on_chunk_received
            handler.on_error = self._on_error
            handler.on_complete = self._on_complete
        
        try:
            async for chunk_data in handler.process_stream(stream_generator):
                if chunk_data.get("done"):
                    break
                
                # 转换为ChatCompletionResponse
                try:
                    response = ChatCompletionResponse(**chunk_data)
                    yield response
                except Exception as e:
                    logger.warning(f"无法解析响应数据: {chunk_data}, 错误: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"流式响应处理失败: {e}")
            raise StreamingError(f"流式响应处理失败: {e}")
    
    async def process_text_stream(
        self,
        stream_generator: AsyncGenerator[str, None]
    ) -> AsyncGenerator[str, None]:
        """处理文本流式响应"""
        handler = StreamingHandler(
            retry_config=self.retry_config,
            timeout=300.0,
            chunk_timeout=30.0
        )
        
        try:
            async for chunk_data in handler.process_stream(stream_generator):
                if chunk_data.get("done"):
                    break
                
                # 提取文本内容
                if "choices" in chunk_data:
                    choices = chunk_data["choices"]
                    if choices and len(choices) > 0:
                        choice = choices[0]
                        if "delta" in choice and "content" in choice["delta"]:
                            content = choice["delta"]["content"]
                            if content:
                                yield content
                                
        except Exception as e:
            logger.error(f"文本流式处理失败: {e}")
            raise StreamingError(f"文本流式处理失败: {e}")
    
    def _on_chunk_received(self, chunk: str):
        """处理接收到的数据块"""
        if self.stats:
            # 更新缓冲区
            self._buffer.append(chunk)
            self._buffer_size += len(chunk)
            
            # 清理缓冲区
            if self._buffer_size > self.buffer_size:
                self._buffer = self._buffer[-self.buffer_size//2:]
                self._buffer_size = sum(len(chunk) for chunk in self._buffer)
    
    def _on_error(self, error: Exception):
        """处理错误"""
        if self.stats:
            self.stats.errors_count += 1
        logger.error(f"流式处理错误: {error}")
    
    def _on_complete(self, stats: StreamingStats):
        """处理完成"""
        if self.enable_stats:
            self.stats = stats
            logger.info(
                f"流式处理完成 - "
                f"持续时间: {stats.duration:.2f}s, "
                f"数据块: {stats.chunks_received}, "
                f"错误: {stats.errors_count}, "
                f"重试: {stats.retries_count}"
            )
    
    def get_buffer_content(self) -> str:
        """获取缓冲区内容"""
        return "".join(self._buffer)
    
    def clear_buffer(self):
        """清空缓冲区"""
        self._buffer.clear()
        self._buffer_size = 0


class StreamingManager:
    """流式管理器"""
    
    def __init__(self):
        self.active_streams: Dict[str, StreamingHandler] = {}
        self.default_retry_config = RetryConfig()
    
    def create_handler(
        self, 
        stream_id: str,
        retry_config: Optional[RetryConfig] = None
    ) -> StreamingHandler:
        """创建流式处理器"""
        handler = StreamingHandler(
            retry_config=retry_config or self.default_retry_config
        )
        
        self.active_streams[stream_id] = handler
        return handler
    
    def get_handler(self, stream_id: str) -> Optional[StreamingHandler]:
        """获取流式处理器"""
        return self.active_streams.get(stream_id)
    
    def remove_handler(self, stream_id: str):
        """移除流式处理器"""
        if stream_id in self.active_streams:
            del self.active_streams[stream_id]
    
    def get_active_streams(self) -> List[str]:
        """获取活跃流列表"""
        return list(self.active_streams.keys())
    
    def cleanup_completed_streams(self):
        """清理已完成的流"""
        completed_streams = []
        for stream_id, handler in self.active_streams.items():
            if handler.stats.end_time is not None:
                completed_streams.append(stream_id)
        
        for stream_id in completed_streams:
            self.remove_handler(stream_id)
        
        logger.info(f"清理了 {len(completed_streams)} 个已完成的流")


# 全局流式管理器实例
_global_streaming_manager: Optional[StreamingManager] = None


def get_streaming_manager() -> StreamingManager:
    """获取全局流式管理器"""
    global _global_streaming_manager
    
    if _global_streaming_manager is None:
        _global_streaming_manager = StreamingManager()
    
    return _global_streaming_manager