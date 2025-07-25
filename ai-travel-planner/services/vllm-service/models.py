"""
vLLM服务API模型定义
API models for vLLM service
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import time


class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str = Field(..., description="消息角色: system, user, assistant")
    content: str = Field(..., description="消息内容")
    name: Optional[str] = Field(None, description="消息发送者名称")


class ChatCompletionRequest(BaseModel):
    """聊天完成请求模型"""
    model: str = Field(..., description="模型名称")
    messages: List[ChatMessage] = Field(..., description="消息列表")
    
    # 生成参数
    max_tokens: int = Field(default=1024, description="最大生成token数")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度参数")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="top_p参数")
    top_k: Optional[int] = Field(default=50, ge=1, description="top_k参数")
    
    # 惩罚参数
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="频率惩罚")
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="存在惩罚")
    repetition_penalty: float = Field(default=1.0, ge=0.0, le=2.0, description="重复惩罚")
    
    # 停止条件
    stop: Optional[Union[str, List[str]]] = Field(default=None, description="停止词")
    
    # 流式输出
    stream: bool = Field(default=False, description="是否流式输出")
    
    # 高级参数
    n: int = Field(default=1, ge=1, le=10, description="生成候选数")
    best_of: Optional[int] = Field(default=None, ge=1, description="最佳候选数")
    use_beam_search: bool = Field(default=False, description="使用束搜索")
    length_penalty: float = Field(default=1.0, description="长度惩罚")
    early_stopping: bool = Field(default=False, description="早停")
    
    # 其他参数
    user: Optional[str] = Field(default=None, description="用户标识")
    logit_bias: Optional[Dict[str, float]] = Field(default=None, description="logit偏置")


class ChatCompletionChoice(BaseModel):
    """聊天完成选择模型"""
    index: int = Field(..., description="选择索引")
    message: Optional[ChatMessage] = Field(None, description="完成消息")
    delta: Optional[ChatMessage] = Field(None, description="增量消息(流式)")
    finish_reason: Optional[str] = Field(None, description="完成原因")
    logprobs: Optional[Dict[str, Any]] = Field(None, description="对数概率")


class Usage(BaseModel):
    """使用统计模型"""
    prompt_tokens: int = Field(..., description="提示词token数")
    completion_tokens: int = Field(..., description="完成token数")
    total_tokens: int = Field(..., description="总token数")


class ChatCompletionResponse(BaseModel):
    """聊天完成响应模型"""
    id: str = Field(..., description="响应ID")
    object: str = Field(default="chat.completion", description="对象类型")
    created: int = Field(default_factory=lambda: int(time.time()), description="创建时间")
    model: str = Field(..., description="模型名称")
    choices: List[ChatCompletionChoice] = Field(..., description="选择列表")
    usage: Optional[Usage] = Field(None, description="使用统计")
    system_fingerprint: Optional[str] = Field(None, description="系统指纹")
    
    @classmethod
    def from_vllm_output(
        cls, 
        request_output, 
        model_name: str, 
        stream: bool = False
    ) -> "ChatCompletionResponse":
        """从vLLM输出创建响应"""
        from vllm.outputs import RequestOutput
        
        if not isinstance(request_output, RequestOutput):
            raise ValueError("Invalid request output type")
        
        choices = []
        for i, output in enumerate(request_output.outputs):
            if stream:
                # 流式响应使用delta
                choice = ChatCompletionChoice(
                    index=i,
                    delta=ChatMessage(
                        role="assistant",
                        content=output.text
                    ),
                    finish_reason=output.finish_reason
                )
            else:
                # 非流式响应使用message
                choice = ChatCompletionChoice(
                    index=i,
                    message=ChatMessage(
                        role="assistant",
                        content=output.text
                    ),
                    finish_reason=output.finish_reason
                )
            choices.append(choice)
        
        # 计算使用统计
        usage = None
        if hasattr(request_output, 'usage') and request_output.usage:
            usage = Usage(
                prompt_tokens=request_output.usage.prompt_tokens,
                completion_tokens=request_output.usage.completion_tokens,
                total_tokens=request_output.usage.total_tokens
            )
        
        return cls(
            id=request_output.request_id,
            object="chat.completion.chunk" if stream else "chat.completion",
            model=model_name,
            choices=choices,
            usage=usage
        )


class ModelInfo(BaseModel):
    """模型信息模型"""
    id: str = Field(..., description="模型ID")
    object: str = Field(default="model", description="对象类型")
    created: int = Field(default_factory=lambda: int(time.time()), description="创建时间")
    owned_by: str = Field(..., description="拥有者")
    permission: Optional[List[Dict[str, Any]]] = Field(default=None, description="权限")
    root: Optional[str] = Field(default=None, description="根模型")
    parent: Optional[str] = Field(default=None, description="父模型")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: Dict[str, Any] = Field(..., description="错误信息")
    
    @classmethod
    def create(cls, message: str, error_type: str = "internal_error") -> "ErrorResponse":
        """创建错误响应"""
        return cls(
            error={
                "message": message,
                "type": error_type,
                "code": None
            }
        )


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    model: str = Field(..., description="当前模型")
    engine_ready: bool = Field(..., description="引擎是否就绪")
    timestamp: int = Field(default_factory=lambda: int(time.time()), description="时间戳")
    version: str = Field(default="1.0.0", description="服务版本")


class GenerationRequest(BaseModel):
    """通用生成请求模型"""
    prompt: str = Field(..., description="输入提示词")
    max_tokens: int = Field(default=1024, description="最大生成token数")
    temperature: float = Field(default=0.7, description="温度参数")
    top_p: float = Field(default=0.9, description="top_p参数")
    top_k: Optional[int] = Field(default=50, description="top_k参数")
    stop: Optional[List[str]] = Field(default=None, description="停止词列表")
    stream: bool = Field(default=False, description="是否流式输出")


class GenerationResponse(BaseModel):
    """通用生成响应模型"""
    text: str = Field(..., description="生成文本")
    finish_reason: Optional[str] = Field(None, description="完成原因")
    usage: Optional[Usage] = Field(None, description="使用统计")
    request_id: str = Field(..., description="请求ID")