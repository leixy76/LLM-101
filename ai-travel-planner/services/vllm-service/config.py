"""
vLLM服务配置模块
Configuration module for vLLM service
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os


class VLLMConfig(BaseModel):
    """vLLM服务配置类"""
    
    # 模型配置
    model_name: str = Field(
        default="Qwen/Qwen2.5-7B-Instruct",
        description="模型名称或路径"
    )
    model_path: Optional[str] = Field(
        default=None,
        description="本地模型路径"
    )
    
    # 服务配置
    host: str = Field(default="0.0.0.0", description="服务监听地址")
    port: int = Field(default=8001, description="服务端口")
    
    # 推理配置
    tensor_parallel_size: int = Field(
        default=1,
        description="张量并行大小"
    )
    pipeline_parallel_size: int = Field(
        default=1,
        description="流水线并行大小"
    )
    max_model_len: int = Field(
        default=4096,
        description="最大模型长度"
    )
    max_num_seqs: int = Field(
        default=256,
        description="最大序列数"
    )
    
    # GPU配置
    gpu_memory_utilization: float = Field(
        default=0.8,
        description="GPU内存使用率"
    )
    enable_prefix_caching: bool = Field(
        default=True,
        description="启用前缀缓存"
    )
    
    # 性能优化
    swap_space: int = Field(
        default=4,
        description="交换空间大小(GB)"
    )
    cpu_offload_gb: int = Field(
        default=0,
        description="CPU卸载内存大小(GB)"
    )
    
    # 安全配置
    disable_log_stats: bool = Field(
        default=False,
        description="禁用日志统计"
    )
    trust_remote_code: bool = Field(
        default=True,
        description="信任远程代码"
    )
    
    # API配置
    api_key: Optional[str] = Field(
        default=None,
        description="API密钥"
    )
    served_model_name: Optional[str] = Field(
        default=None,
        description="服务模型名称"
    )
    
    @classmethod
    def from_env(cls) -> "VLLMConfig":
        """从环境变量创建配置"""
        return cls(
            model_name=os.getenv("VLLM_MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct"),
            model_path=os.getenv("VLLM_MODEL_PATH"),
            host=os.getenv("VLLM_HOST", "0.0.0.0"),
            port=int(os.getenv("VLLM_PORT", "8001")),
            tensor_parallel_size=int(os.getenv("VLLM_TENSOR_PARALLEL_SIZE", "1")),
            max_model_len=int(os.getenv("VLLM_MAX_MODEL_LEN", "4096")),
            max_num_seqs=int(os.getenv("VLLM_MAX_NUM_SEQS", "256")),
            gpu_memory_utilization=float(os.getenv("VLLM_GPU_MEMORY_UTILIZATION", "0.8")),
            enable_prefix_caching=os.getenv("VLLM_ENABLE_PREFIX_CACHING", "true").lower() == "true",
            api_key=os.getenv("VLLM_API_KEY"),
            served_model_name=os.getenv("VLLM_SERVED_MODEL_NAME"),
        )


class GenerationConfig(BaseModel):
    """生成配置类"""
    
    max_tokens: int = Field(default=1024, description="最大生成token数")
    temperature: float = Field(default=0.7, description="温度参数")
    top_p: float = Field(default=0.9, description="top_p参数")
    top_k: int = Field(default=50, description="top_k参数")
    frequency_penalty: float = Field(default=0.0, description="频率惩罚")
    presence_penalty: float = Field(default=0.0, description="存在惩罚")
    repetition_penalty: float = Field(default=1.0, description="重复惩罚")
    stop: Optional[List[str]] = Field(default=None, description="停止词列表")
    stream: bool = Field(default=False, description="是否流式输出")
    
    # 高级参数
    best_of: Optional[int] = Field(default=None, description="最佳候选数")
    use_beam_search: bool = Field(default=False, description="使用束搜索")
    length_penalty: float = Field(default=1.0, description="长度惩罚")
    early_stopping: bool = Field(default=False, description="早停")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {k: v for k, v in self.dict().items() if v is not None}


# 默认配置实例
DEFAULT_VLLM_CONFIG = VLLMConfig()
DEFAULT_GENERATION_CONFIG = GenerationConfig()