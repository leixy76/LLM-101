"""
流式处理测试
Streaming processing tests
"""

import pytest
import asyncio
import json
import time
from unittest.mock import AsyncMock, Mock, patch
import httpx

from ..streaming import (
    RetryStrategy,
    RetryConfig,
    StreamingStats,
    StreamingHandler,
    StreamingResponseProcessor,
    StreamingManager,
    StreamingError,
    StreamingTimeoutError,
    StreamingConnectionError,
    get_streaming_manager
)
from ..client import VLLMTimeoutError, VLLMConnectionError


class TestRetryConfig:
    """重试配置测试类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = RetryConfig()
        
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF
        assert config.retry_on_timeout is True
        assert config.retry_on_connection_error is True
        assert config.retry_on_server_error is True
        assert config.backoff_multiplier == 2.0
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = RetryConfig(
            max_retries=5,
            base_delay=2.0,
            strategy=RetryStrategy.LINEAR_BACKOFF,
            retry_on_timeout=False
        )
        
        assert config.max_retries == 5
        assert config.base_delay == 2.0
        assert config.strategy == RetryStrategy.LINEAR_BACKOFF
        assert config.retry_on_timeout is False


class TestStreamingStats:
    """流式统计测试类"""
    
    def test_stats_creation(self):
        """测试统计创建"""
        start_time = time.time()
        stats = StreamingStats(start_time=start_time)
        
        assert stats.start_time == start_time
        assert stats.end_time is None
        assert stats.total_tokens == 0
        assert stats.chunks_received == 0
        assert stats.errors_count == 0
        assert stats.retries_count == 0
    
    def test_duration_calculation(self):
        """测试持续时间计算"""
        start_time = time.time()
        stats = StreamingStats(start_time=start_time)
        
        # 未结束时应该返回None
        assert stats.duration is None
        
        # 设置结束时间
        stats.end_time = start_time + 5.0
        assert abs(stats.duration - 5.0) < 0.1
    
    def test_tokens_per_second(self):
        """测试每秒token数计算"""
        start_time = time.time()
        stats = StreamingStats(
            start_time=start_time,
            end_time=start_time + 2.0,
            total_tokens=100
        )
        
        assert abs(stats.tokens_per_second - 50.0) < 0.1
        
        # 持续时间为0时应该返回None
        stats.end_time = start_time
        assert stats.tokens_per_second is None


class TestStreamingHandler:
    """流式处理器测试类"""
    
    @pytest.fixture
    def handler(self):
        """处理器fixture"""
        return StreamingHandler(
            retry_config=RetryConfig(max_retries=2, base_delay=0.1),
            timeout=5.0,
            chunk_timeout=1.0
        )
    
    def test_handler_initialization(self, handler):
        """测试处理器初始化"""
        assert handler.retry_config.max_retries == 2
        assert handler.timeout == 5.0
        assert handler.chunk_timeout == 1.0
        assert isinstance(handler.stats, StreamingStats)
    
    def test_calculate_delay_exponential(self, handler):
        """测试指数退避延迟计算"""
        handler.retry_config.strategy = RetryStrategy.EXPONENTIAL_BACKOFF
        handler.retry_config.base_delay = 1.0
        handler.retry_config.backoff_multiplier = 2.0
        
        assert handler._calculate_delay(0) == 1.0
        assert handler._calculate_delay(1) == 2.0
        assert handler._calculate_delay(2) == 4.0
    
    def test_calculate_delay_linear(self, handler):
        """测试线性退避延迟计算"""
        handler.retry_config.strategy = RetryStrategy.LINEAR_BACKOFF
        handler.retry_config.base_delay = 1.0
        
        assert handler._calculate_delay(0) == 1.0
        assert handler._calculate_delay(1) == 2.0
        assert handler._calculate_delay(2) == 3.0
    
    def test_calculate_delay_fixed(self, handler):
        """测试固定延迟计算"""
        handler.retry_config.strategy = RetryStrategy.FIXED_DELAY
        handler.retry_config.base_delay = 2.0
        
        assert handler._calculate_delay(0) == 2.0
        assert handler._calculate_delay(1) == 2.0
        assert handler._calculate_delay(2) == 2.0
    
    def test_calculate_delay_max_limit(self, handler):
        """测试最大延迟限制"""
        handler.retry_config.strategy = RetryStrategy.EXPONENTIAL_BACKOFF
        handler.retry_config.base_delay = 10.0
        handler.retry_config.max_delay = 20.0
        handler.retry_config.backoff_multiplier = 3.0
        
        # 10 * 3^2 = 90, 但应该被限制为20
        assert handler._calculate_delay(2) == 20.0
    
    def test_should_retry_timeout(self, handler):
        """测试超时重试判断"""
        error = VLLMTimeoutError("超时")
        
        # 启用超时重试
        handler.retry_config.retry_on_timeout = True
        assert handler._should_retry(error, 0) is True
        assert handler._should_retry(error, 2) is False  # 超过最大重试次数
        
        # 禁用超时重试
        handler.retry_config.retry_on_timeout = False
        assert handler._should_retry(error, 0) is False
    
    def test_should_retry_connection_error(self, handler):
        """测试连接错误重试判断"""
        error = VLLMConnectionError("连接失败")
        
        # 启用连接错误重试
        handler.retry_config.retry_on_connection_error = True
        assert handler._should_retry(error, 0) is True
        
        # 禁用连接错误重试
        handler.retry_config.retry_on_connection_error = False
        assert handler._should_retry(error, 0) is False
    
    def test_should_retry_server_error(self, handler):
        """测试服务器错误重试判断"""
        response = Mock()
        response.status_code = 500
        error = httpx.HTTPStatusError("服务器错误", request=Mock(), response=response)
        
        # 启用服务器错误重试
        handler.retry_config.retry_on_server_error = True
        assert handler._should_retry(error, 0) is True
        
        # 4xx错误不应该重试
        response.status_code = 400
        assert handler._should_retry(error, 0) is False
    
    @pytest.mark.asyncio
    async def test_handle_stream_chunk_success(self, handler):
        """测试处理流式数据块成功"""
        chunk = '{"id": "test", "choices": [{"delta": {"content": "hello"}}]}'
        
        result = await handler._handle_stream_chunk(chunk)
        
        assert result is not None
        assert result["id"] == "test"
        assert handler.stats.chunks_received == 1
    
    @pytest.mark.asyncio
    async def test_handle_stream_chunk_done(self, handler):
        """测试处理完成标记"""
        result = await handler._handle_stream_chunk("[DONE]")
        
        assert result == {"done": True}
    
    @pytest.mark.asyncio
    async def test_handle_stream_chunk_empty(self, handler):
        """测试处理空数据块"""
        result = await handler._handle_stream_chunk("")
        assert result is None
        
        result = await handler._handle_stream_chunk("   ")
        assert result is None
        
        result = await handler._handle_stream_chunk("# comment")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_handle_stream_chunk_invalid_json(self, handler):
        """测试处理无效JSON"""
        result = await handler._handle_stream_chunk("invalid json")
        assert result is None
        assert handler.stats.chunks_received == 1  # 仍然计数
    
    @pytest.mark.asyncio
    async def test_handle_stream_chunk_error_response(self, handler):
        """测试处理错误响应"""
        chunk = '{"error": {"message": "服务器错误"}}'
        
        with pytest.raises(StreamingError, match="服务器返回错误"):
            await handler._handle_stream_chunk(chunk)
        
        assert handler.stats.errors_count == 1
    
    @pytest.mark.asyncio
    async def test_callback_functions(self, handler):
        """测试回调函数"""
        chunk_received = Mock()
        error_callback = Mock()
        retry_callback = Mock()
        complete_callback = Mock()
        
        handler.on_chunk_received = chunk_received
        handler.on_error = error_callback
        handler.on_retry = retry_callback
        handler.on_complete = complete_callback
        
        # 测试chunk回调
        await handler._handle_stream_chunk('{"test": "data"}')
        chunk_received.assert_called_once()
        
        # 测试错误回调
        try:
            await handler._handle_stream_chunk('{"error": {"message": "test error"}}')
        except StreamingError:
            pass
        error_callback.assert_called_once()


class TestStreamingResponseProcessor:
    """流式响应处理器测试类"""
    
    @pytest.fixture
    def processor(self):
        """处理器fixture"""
        return StreamingResponseP