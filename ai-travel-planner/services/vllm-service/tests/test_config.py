"""
vLLM配置测试
vLLM configuration tests
"""

import pytest
import os
from unittest.mock import patch

from ..config import VLLMConfig, GenerationConfig, DEFAULT_VLLM_CONFIG, DEFAULT_GENERATION_CONFIG


class TestVLLMConfig:
    """vLLM配置测试类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = VLLMConfig()
        
        assert config.model_name == "Qwen/Qwen2.5-7B-Instruct"
        assert config.host == "0.0.0.0"
        assert config.port == 8001
        assert config.tensor_parallel_size == 1
        assert config.max_model_len == 4096
        assert config.gpu_memory_utilization == 0.8
        assert config.enable_prefix_caching is True
        assert config.trust_remote_code is True
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = VLLMConfig(
            model_name="custom-model",
            host="127.0.0.1",
            port=8002,
            tensor_parallel_size=2,
            max_model_len=8192,
            gpu_memory_utilization=0.9
        )
        
        assert config.model_name == "custom- 0.9
    
    @patch.dict(os.environ, {
        'VLLM_MODEL_NAME': 'test-model',
        'VLLM_HOST': '192.168.1.100',
        'VLLM_PORT': '9000',
        'VLLM_TENSOR_PARALLEL_SIZE': '4',
        'VLLM_MAX_MODEL_LEN': '16384',
        'VLLM_GPU_MEMORY_UTILIZATION': '0.95',
        'VLLM_API_KEY': 'test-key'
    })
    def test_from_env(self):
        """测试从环境变量创建配置"""
        config = VLLMConfig.from_env()
        
        assert config.model_name == "test-model"
        assert config.host == "192.168.1.100"
        assert config.port == 9000
        assert config.tensor_parallel_size == 4
        assert config.max_model_len == 16384
        assert config.gpu_memory_utilization == 0.95
        assert config.api_key == "test-key"
    
    def test_validation(self):
        """测试配置验证"""
        # 测试有效配置
        config = VLLMConfig(
            port=8001,
            tensor_parallel_size=1,
            max_model_len=4096,
            gpu_memory_utilization=0.8
        )
        assert config.port == 8001
        
        # 测试边界值
        config = VLLMConfig(gpu_memory_utilization=1.0)
        assert config.gpu_memory_utilization == 1.0


class TestGenerationConfig:
    """生成配置测试类"""
    
    def test_default_generation_config(self):
        """测试默认生成配置"""
        config = GenerationConfig()
        
        assert config.max_tokens == 1024
        assert config.temperature == 0.7
        assert config.top_p == 0.9
        assert config.top_k == 50
        assert config.frequency_penalty == 0.0
        assert config.presence_penalty == 0.0
        assert config.repetition_penalty == 1.0
        assert config.stop is None
        assert config.stream is False
    
    def test_custom_generation_config(self):
        """测试自定义生成配置"""
        config = GenerationConfig(
            max_tokens=2048,
            temperature=0.5,
            top_p=0.95,
            top_k=100,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            repetition_penalty=1.1,
            stop=["<|endoftext|>", "\n\n"],
            stream=True
        )
        
        assert config.max_tokens == 2048
        assert config.temperature == 0.5
        assert config.top_p == 0.95
        assert config.top_k == 100
        assert config.frequency_penalty == 0.1
        assert config.presence_penalty == 0.1
        assert config.repetition_penalty == 1.1
        assert config.stop == ["<|endoftext|>", "\n\n"]
        assert config.stream is True
    
    def test_to_dict(self):
        """测试转换为字典"""
        config = GenerationConfig(
            max_tokens=1024,
            temperature=0.7,
            stop=["stop1", "stop2"]
        )
        
        config_dict = config.to_dict()
        
        assert config_dict["max_tokens"] == 1024
        assert config_dict["temperature"] == 0.7
        assert config_dict["stop"] == ["stop1", "stop2"]
        assert "best_of" not in config_dict  # None值应该被过滤
    
    def test_validation_ranges(self):
        """测试参数范围验证"""
        # 测试有效范围
        config = GenerationConfig(
            temperature=0.1,
            top_p=0.1,
            frequency_penalty=-1.0,
            presence_penalty=1.0
        )
        
        assert config.temperature == 0.1
        assert config.top_p == 0.1
        assert config.frequency_penalty == -1.0
        assert config.presence_penalty == 1.0


class TestDefaultConfigs:
    """默认配置测试类"""
    
    def test_default_vllm_config_instance(self):
        """测试默认vLLM配置实例"""
        assert isinstance(DEFAULT_VLLM_CONFIG, VLLMConfig)
        assert DEFAULT_VLLM_CONFIG.model_name == "Qwen/Qwen2.5-7B-Instruct"
    
    def test_default_generation_config_instance(self):
        """测试默认生成配置实例"""
        assert isinstance(DEFAULT_GENERATION_CONFIG, GenerationConfig)
        assert DEFAULT_GENERATION_CONFIG.max_tokens == 1024