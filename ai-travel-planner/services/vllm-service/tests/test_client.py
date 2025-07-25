"""
vLLM客户端测试
vLLM client tests
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, Mock, patch
import httpx

from ..client import (
    VLLMClient, 
    VLLMConnectionPool, 
    VLLMConnectionError, 
    VLLMTimeoutError,
    get_vllm_client,
    close_global_pool
)
from ..models import ChatMessage, ChatCompletionResponse, ModelInfo, HealthResponse


class TestVLLMClient:
    """vLLM客户端测试类"""
    
    @pytest.fixture
    def client(self):
        """客户端fixture"""
        return VLLMClient(
            base_url="http://localhost:8001",
            timeout=30.0,
            max_retries=2
        )
    
    @pytest.fixture
    def mock_response(self):
        """模拟响应fixture"""
        return {
            "id": "test-id",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "test-model",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "测试响应"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """测试客户端初始化"""
        assert client.base_url == "http://localhost:8001"
        assert client.timeout == 30.0
        assert client.max_retries == 2
        assert client._client is None
    
    @pytest.mark.asyncio
    async def test_ensure_client(self, client):
        """测试确保客户端初始化"""
        await client._ensure_client()
        assert client._client is not None
        assert isinstance(client._client, httpx.AsyncClient)
        
        await client.close()
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """测试异步上下文管理器"""
        async with VLLMClient() as client:
            assert client._client is not None
        # 客户端应该已经关闭
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, client, mock_response):
        """测试健康检查成功"""
        health_response = {
            "status": "healthy",
            "model": "test-model",
            "engine_ready": True
        }
        
        with patch.object(client, '_make_request', return_value=health_response):
            result = await client.health_check()
            assert isinstance(result, HealthResponse)
            assert result.status == "healthy"
            assert result.model == "test-model"
            assert result.engine_ready is True
    
    @pytest.mark.asyncio
    async def test_list_models_success(self, client):
        """测试列出模型成功"""
        models_response = {
            "object": "list",
            "data": [{
                "id": "test-model",
                "object": "model",
                "created": 1234567890,
                "owned_by": "vllm"
            }]
        }
        
        with patch.object(client, '_make_request', return_value=models_response):
            result = await client.list_models()
            assert len(result) == 1
            assert isinstance(result[0], ModelInfo)
            assert result[0].id == "test-model"
    
    @pytest.mark.asyncio
    async def test_chat_completion_success(self, client, mock_response):
        """测试聊天完成成功"""
        messages = [ChatMessage(role="user", content="你好")]
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = await client.chat_completion(messages)
            assert isinstance(result, ChatCompletionResponse)
            assert result.id == "test-id"
            assert len(result.choices) == 1
            assert result.choices[0].message.content == "测试响应"
    
    @pytest.mark.asyncio
    async def test_chat_completion_stream(self, client):
        """测试流式聊天完成"""
        messages = [ChatMessage(role="user", content="你好")]
        
        # 模拟流式响应
        stream_data = [
            '{"id": "test-id", "choices": [{"delta": {"content": "你"}}]}',
            '{"id": "test-id", "choices": [{"delta": {"content": "好"}}]}',
            '[DONE]'
        ]
        
        async def mock_stream():
            for data in stream_data:
                yield data
        
        with patch.object(client, '_make_request', return_value=mock_stream()):
            responses = []
            async for response in client.chat_completion_stream(messages):
                responses.append(response)
            
            assert len(responses) == 2
            assert all(isinstance(r, ChatCompletionResponse) for r in responses)
    
    @pytest.mark.asyncio
    async def test_generate_success(self, client, mock_response):
        """测试文本生成成功"""
        with patch.object(client, 'chat_completion', return_value=ChatCompletionResponse(**mock_response)):
            result = await client.generate("测试提示词")
            assert result.text == "测试响应"
            assert result.request_id == "test-id"
    
    @pytest.mark.asyncio
    async def test_connection_error_retry(self, client):
        """测试连接错误重试"""
        with patch.object(client, '_ensure_client'):
            with patch.object(client, '_client') as mock_client:
                # 模拟连接错误
                mock_client.request.side_effect = [
                    httpx.ConnectError("连接失败"),
                    httpx.ConnectError("连接失败"),
                    Mock(status_code=200, json=lambda: {"status": "ok"})
                ]
                
                with pytest.raises(VLLMConnectionError):
                    await client._make_request("GET", "/test")
    
    @pytest.mark.asyncio
    async def test_timeout_error(self, client):
        """测试超时错误"""
        with patch.object(client, '_ensure_client'):
            with patch.object(client, '_client') as mock_client:
                mock_client.request.side_effect = httpx.TimeoutException("超时")
                
                with pytest.raises(VLLMTimeoutError):
                    await client._make_request("GET", "/test")


class TestVLLMConnectionPool:
    """vLLM连接池测试类"""
    
    @pytest.fixture
    def pool(self):
        """连接池fixture"""
        return VLLMConnectionPool(
            base_url="http://localhost:8001",
            pool_size=3,
            timeout=30.0
        )
    
    @pytest.mark.asyncio
    async def test_pool_initialization(self, pool):
        """测试连接池初始化"""
        assert pool.pool_size == 3
        assert not pool._initialized
        
        await pool.initialize()
        assert pool._initialized
        assert len(pool._pool) == 3
        
        await pool.close()
    
    @pytest.mark.asyncio
    async def test_get_client_context_manager(self, pool):
        """测试获取客户端上下文管理器"""
        await pool.initialize()
        
        async with pool.get_client() as client:
            assert isinstance(client, VLLMClient)
        
        await pool.close()
    
    @pytest.mark.asyncio
    async def test_pool_reuse(self, pool):
        """测试连接池复用"""
        await pool.initialize()
        
        clients = []
        
        # 获取多个客户端
        async with pool.get_client() as client1:
            clients.append(client1)
            async with pool.get_client() as client2:
                clients.append(client2)
                async with pool.get_client() as client3:
                    clients.append(client3)
        
        # 所有客户端应该不同
        assert len(set(id(c) for c in clients)) == 3
        
        await pool.close()
    
    @pytest.mark.asyncio
    async def test_pool_close(self, pool):
        """测试连接池关闭"""
        await pool.initialize()
        assert pool._initialized
        
        await pool.close()
        assert not pool._initialized
        assert len(pool._pool) == 0


class TestGlobalFunctions:
    """全局函数测试类"""
    
    @pytest.mark.asyncio
    async def test_get_vllm_client(self):
        """测试获取全局vLLM客户端"""
        # 清理全局状态
        await close_global_pool()
        
        async with get_vllm_client() as client:
            assert isinstance(client, VLLMClient)
        
        await close_global_pool()
    
    @pytest.mark.asyncio
    async def test_close_global_pool(self):
        """测试关闭全局连接池"""
        # 先获取客户端以初始化全局池
        async with get_vllm_client() as client:
            pass
        
        # 关闭全局池
        await close_global_pool()
        
        # 验证可以重新初始化
        async with get_vllm_client() as client:
            assert isinstance(client, VLLMClient)
        
        await close_global_pool()


@pytest.mark.integration
class TestVLLMClientIntegration:
    """vLLM客户端集成测试"""
    
    @pytest.mark.asyncio
    async def test_real_server_connection(self):
        """测试真实服务器连接（需要运行vLLM服务器）"""
        client = VLLMClient(base_url="http://localhost:8001")
        
        try:
            # 测试健康检查
            health = await client.health_check()
            assert health.status == "healthy"
            
            # 测试模型列表
            models = await client.list_models()
            assert len(models) > 0
            
            # 测试聊天完成
            messages = [ChatMessage(role="user", content="你好，请简单回复")]
            response = await client.chat_completion(messages, max_tokens=50)
            assert response.choices[0].message.content
            
        except VLLMConnectionError:
            pytest.skip("vLLM服务器未运行，跳过集成测试")
        finally:
            await client.close()