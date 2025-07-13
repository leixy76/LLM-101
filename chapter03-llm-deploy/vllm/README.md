# VLLM DeepSeek 谷歌 Colab 实验场

一个用于在 Google Colab 中使用 VLLM 运行 DeepSeek 模型的简化实现。这个实验场允许您在 Colab 环境中轻松部署和交互 DeepSeek-R1-Distill-Qwen-1.5B 和其他 DeepSeek 模型。

## 🚀 特性

- 在 Google Colab 中轻松部署 DeepSeek 模型
- 实时服务器监控和状态检查
- 针对 Colab 的 GPU 环境进行优化
- 模型交互的交互式界面
- 使用 VLLM 进行内存高效的模型服务
- 支持各种 DeepSeek 模型变体

## 📋 前置条件

在运行实验场之前，请确保您具备：
- 能够访问 Google Colab 的 Google 账户
- 在 Colab notebook 中启用 GPU 运行时

## 🛠️ 快速开始

1. **在 Colab 中打开**
   ```
   [在此处添加 Colab 徽章/链接]
   ```

2. **安装依赖**
   ```python
   !pip install fastapi nest-asyncio pyngrok uvicorn

   !pip install vllm
   ```

3. **启动服务器**
   ```python
   import subprocess
   model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B' # 在此处指定您的模型

   
   vllm_process = subprocess.Popen([
       'vllm',
       'serve',
       'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B',
       '--trust-remote-code',
       '--dtype', 'half',
       '--max-model-len', '16384',
       '--enable-chunked-prefill', 'false',
       '--tensor-parallel-size', '1'
   ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
   ```

4. **监控服务器状态**
   ```python
   # [包含之前实现的监控代码]
   ```

## ⚙️ 配置选项

### 模型参数
- `--dtype`: 设置为 'half' 以获得最佳 Colab 性能
- `--max-model-len`: 最大序列长度（默认：16384）
- `--tensor-parallel-size`: GPU 并行设置
- `--enable-chunked-prefill`: 预填充优化设置

### 服务器设置
- 默认端口：8000
- 健康检查端点：`/health`
- 生成端点：`/generate`

## 🔍 监控和调试

实验场包含内置的监控功能：
- 实时服务器状态检查
- 输出日志记录（stdout/stderr）
- 错误处理和恢复
- 进程管理

## 📊 性能提示

1. **内存管理**
   - 使用 `dtype=half` 进行高效内存使用
   - 根据需要调整 `max-model-len`
   - 监控 Colab GPU 内存使用情况

2. **优化**
   - 尽可能批处理请求
   - 使用适当的温度设置
   - 监控令牌使用情况

## 🚧 故障排除

常见问题和解决方案：

1. **服务器无法启动**
   - 检查 Colab 中的 GPU 可用性
   - 验证 VLLM 安装
   - 检查内存使用情况

2. **响应时间慢**
   - 减少 `max_tokens`
   - 调整批处理大小
   - 检查网络连接

3. **内存不足**
   - 减少模型参数
   - 清除 Colab 运行时
   - 使用 GPU 重启运行时

## 📝 许可证

本项目基于 MIT 许可证 - 详情请参阅 LICENSE 文件。

## 🙏 致谢

- [VLLM 项目](https://github.com/vllm-project/vllm)
- [DeepSeek AI](https://github.com/deepseek-ai)
- Google Colab 团队

## 🤝 贡献

欢迎贡献！请随时提交问题和拉取请求。