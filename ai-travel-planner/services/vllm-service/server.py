"""
vLLM服务器启动模块
vLLM server startup module
"""

import asyncio
import logging
import signal
import sys
from typing import Optional
from contextlib import asynccontextmanager

from vllm import LLM, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.utils import random_uuid
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import VLLMConfig, DEFAULT_VLLM_CONFIG
from .models import ChatCompletionRequest, ChatCompletionResponse, ModelInfo
from .prompt_manager import PromptManager

logger = logging.getLogger(__name__)


class VLLMServer:
    """vLLM服务器类"""
    
    def __init__(self, config: Optional[VLLMConfig] = None):
        self.config = config or DEFAULT_VLLM_CONFIG
        self.engine: Optional[AsyncLLMEngine] = None
        self.prompt_manager = PromptManager()
        self.app: Optional[FastAPI] = None
        self._shutdown_event = asyncio.Event()
        
    async def initialize_engine(self):
        """初始化vLLM引擎"""
        try:
            logger.info(f"正在初始化vLLM引擎，模型: {self.config.model_name}")
            
            # 构建引擎参数
            engine_args = AsyncEngineArgs(
                model=self.config.model_path or self.config.model_name,
                tensor_parallel_size=self.config.tensor_parallel_size,
                pipeline_parallel_size=self.config.pipeline_parallel_size,
                max_model_len=self.config.max_model_len,
                max_num_seqs=self.config.max_num_seqs,
                gpu_memory_utilization=self.config.gpu_memory_utilization,
                enable_prefix_caching=self.config.enable_prefix_caching,
                swap_space=self.config.swap_space,
                cpu_offload_gb=self.config.cpu_offload_gb,
                disable_log_stats=self.config.disable_log_stats,
                trust_remote_code=self.config.trust_remote_code,
                served_model_name=self.config.served_model_name or self.config.model_name,
            )
            
            # 创建异步引擎
            self.engine = AsyncLLMEngine.from_engine_args(engine_args)
            logger.info("vLLM引擎初始化成功")
            
        except Exception as e:
            logger.error(f"vLLM引擎初始化失败: {e}")
            raise
    
    async def shutdown_engine(self):
        """关闭vLLM引擎"""
        if self.engine:
            logger.info("正在关闭vLLM引擎...")
            # vLLM引擎没有显式的关闭方法，设置shutdown事件
            self._shutdown_event.set()
            self.engine = None
            logger.info("vLLM引擎已关闭")
    
    def create_app(self) -> FastAPI:
        """创建FastAPI应用"""
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # 启动时初始化引擎
            await self.initialize_engine()
            yield
            # 关闭时清理引擎
            await self.shutdown_engine()
        
        app = FastAPI(
            title="vLLM推理服务",
            description="基于vLLM的大语言模型推理服务",
            version="1.0.0",
            lifespan=lifespan
        )
        
        # 添加CORS中间件
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 注册路由
        self._register_routes(app)
        
        self.app = app
        return app
    
    def _register_routes(self, app: FastAPI):
        """注册API路由"""
        
        @app.get("/health")
        async def health_check():
            """健康检查"""
            return {
                "status": "healthy",
                "model": self.config.model_name,
                "engine_ready": self.engine is not None
            }
        
        @app.get("/v1/models")
        async def list_models():
            """列出可用模型"""
            return {
                "object": "list",
                "data": [
                    ModelInfo(
                        id=self.config.served_model_name or self.config.model_name,
                        object="model",
                        created=0,
                        owned_by="vllm"
                    ).dict()
                ]
            }
        
        @app.post("/v1/chat/completions")
        async def chat_completions(request: ChatCompletionRequest):
            """聊天完成接口"""
            if not self.engine:
                raise HTTPException(status_code=503, detail="引擎未就绪")
            
            try:
                # 处理提示词
                prompt = self.prompt_manager.format_chat_prompt(request.messages)
                
                # 构建采样参数
                sampling_params = SamplingParams(
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    top_k=request.top_k or -1,
                    frequency_penalty=request.frequency_penalty,
                    presence_penalty=request.presence_penalty,
                    repetition_penalty=request.repetition_penalty,
                    stop=request.stop,
                    use_beam_search=request.use_beam_search,
                    best_of=request.best_of,
                    length_penalty=request.length_penalty,
                    early_stopping=request.early_stopping,
                )
                
                # 生成请求ID
                request_id = random_uuid()
                
                if request.stream:
                    # 流式响应
                    return await self._handle_streaming_request(
                        prompt, sampling_params, request_id, request
                    )
                else:
                    # 非流式响应
                    return await self._handle_non_streaming_request(
                        prompt, sampling_params, request_id, request
                    )
                    
            except Exception as e:
                logger.error(f"聊天完成请求处理失败: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def _handle_non_streaming_request(
        self, 
        prompt: str, 
        sampling_params: SamplingParams, 
        request_id: str,
        request: ChatCompletionRequest
    ):
        """处理非流式请求"""
        try:
            # 生成响应
            results = []
            async for request_output in self.engine.generate(
                prompt, sampling_params, request_id
            ):
                results.append(request_output)
            
            if not results:
                raise HTTPException(status_code=500, detail="生成失败")
            
            final_output = results[-1]
            
            # 构建响应
            response = ChatCompletionResponse.from_vllm_output(
                final_output, request.model
            )
            
            return response.dict()
            
        except Exception as e:
            logger.error(f"非流式请求处理失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _handle_streaming_request(
        self, 
        prompt: str, 
        sampling_params: SamplingParams, 
        request_id: str,
        request: ChatCompletionRequest
    ):
        """处理流式请求"""
        from fastapi.responses import StreamingResponse
        import json
        
        async def generate_stream():
            try:
                async for request_output in self.engine.generate(
                    prompt, sampling_params, request_id
                ):
                    # 构建流式响应
                    response = ChatCompletionResponse.from_vllm_output(
                        request_output, request.model, stream=True
                    )
                    
                    # 发送数据
                    yield f"data: {json.dumps(response.dict())}\n\n"
                
                # 发送结束标记
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.error(f"流式请求处理失败: {e}")
                error_response = {
                    "error": {
                        "message": str(e),
                        "type": "internal_error"
                    }
                }
                yield f"data: {json.dumps(error_response)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    async def start_server(self):
        """启动服务器"""
        app = self.create_app()
        
        # 设置信号处理
        def signal_handler(signum, frame):
            logger.info(f"收到信号 {signum}，正在关闭服务器...")
            asyncio.create_task(self.shutdown_engine())
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # 启动服务器
        config = uvicorn.Config(
            app,
            host=self.config.host,
            port=self.config.port,
            log_level="info",
            access_log=True,
        )
        
        server = uvicorn.Server(config)
        logger.info(f"vLLM服务器启动在 {self.config.host}:{self.config.port}")
        await server.serve()


async def main():
    """主函数"""
    # 从环境变量加载配置
    config = VLLMConfig.from_env()
    
    # 创建并启动服务器
    server = VLLMServer(config)
    await server.start_server()


if __name__ == "__main__":
    asyncio.run(main())