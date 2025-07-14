# 飞书消息自动翻译系统

基于n8n工作流和transformer模型的飞书消息自动翻译系统，支持中英文互译。

## 🎯 功能特性

- **自动语言检测**: 智能识别中文和英文
- **中英互译**: 中文自动翻译为英文，英文自动翻译为中文
- **飞书集成**: 无缝对接飞书机器人，实现消息自动翻译
- **工作流自动化**: 使用n8n可视化配置翻译流程
- **容器化部署**: 基于Docker的一键部署方案
- **零成本方案**: 使用开源模型和Google Colab，无需付费API

## 🏗️ 系统架构

```
飞书消息 → n8n工作流 → 翻译API → 模型推理 → 返回结果 → 飞书回复
    ↓           ↓          ↓         ↓         ↓        ↓
  Webhook → 消息处理 → HTTP请求 → MarianMT → 翻译结果 → 消息发送
```

## 📋 技术栈

### 核心组件
- **n8n**: 工作流自动化平台
- **FastAPI**: 高性能Python Web框架
- **Transformers**: Hugging Face模型库
- **MarianMT**: 神经机器翻译模型

### 基础设施
- **Docker**: 容器化部署
- **PostgreSQL**: 数据持久化
- **Redis**: 缓存和会话管理
- **ngrok**: 内网穿透工具

### 模型选择
- **中→英**: `Helsinki-NLP/opus-mt-zh-en`
- **英→中**: `Helsinki-NLP/opus-mt-en-zh`
- **语言检测**: `langdetect`

## 🚀 快速开始

### 系统要求
- Ubuntu 22.04.4 LTS
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ 磁盘空间

### 一键启动

```bash
# 克隆项目（如果需要）
cd chapter07-llm-n8n

# 运行启动脚本
./start.sh
```

启动脚本会自动：
- ✅ 检查系统要求
- ✅ 创建必要目录
- ✅ 生成环境配置
- ✅ 启动Docker服务
- ✅ 检查服务健康状态

### 手动启动

```bash
# 1. 创建环境变量文件
cp .env.example .env
nano .env  # 编辑配置

# 2. 启动服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f
```

## 🔧 配置说明

### 环境变量配置

```bash
# n8n基础配置
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_password

# 加密密钥（必须修改）
N8N_ENCRYPTION_KEY=your_encryption_key

# 数据库配置
POSTGRES_PASSWORD=your_db_password

# Redis配置
REDIS_PASSWORD=your_redis_password
```

### ngrok配置

1. 注册ngrok账号: https://ngrok.com
2. 获取认证token
3. 在Jupyter Notebook中配置token
4. 启动翻译API服务

### 飞书机器人配置

1. **创建飞书应用**
   - 登录飞书开放平台
   - 创建机器人应用
   - 获取App ID和App Secret

2. **配置事件订阅**
   - 设置请求地址: `https://your-domain.ngrok.io/webhook/feishu-webhook`
   - 订阅事件: `接收消息`
   - 配置消息推送

3. **权限配置**
   - 开通`接收消息`权限
   - 开通`发送消息`权限

## 📝 使用指南

### 1. 启动翻译API

使用Google Colab运行`feishu_translator.ipynb`:

```python
# 配置ngrok token
NGROK_TOKEN = "your_ngrok_token_here"

# 运行所有代码单元
# 获取公网地址
```

### 2. 配置n8n工作流

1. **访问n8n界面**
   ```
   http://localhost:5678
   用户名: admin
   密码: password123
   ```

2. **导入工作流**
   - 点击"Import from file"
   - 选择`workflows/feishu_translator_workflow.json`
   - 保存工作流

3. **配置API地址**
   - 在"调用翻译API"节点中
   - 更新URL为ngrok地址
   - 测试连接

### 3. 测试翻译功能

发送消息到飞书机器人:
- 中文消息 → 自动翻译为英文
- 英文消息 → 自动翻译为中文

## 📊 工作流节点说明

| 节点名称 | 功能说明 | 配置要点 |
|---------|---------|---------|
| 飞书Webhook接收器 | 接收飞书消息 | 设置webhook路径 |
| 检查消息类型 | 验证消息格式 | 过滤非文本消息 |
| 提取消息内容 | 解析消息数据 | 提取文本和用户信息 |
| 调用翻译API | 执行翻译请求 | 配置API地址和参数 |
| 处理翻译结果 | 格式化回复 | 构建回复消息格式 |
| 发送回复到飞书 | 返回翻译结果 | 配置飞书API token |

## 🔍 API接口文档

### 翻译接口

**POST** `/translate`

请求体:
```json
{
  "text": "要翻译的文本",
  "source_language": "zh-cn"  // 可选
}
```

响应:
```json
{
  "success": true,
  "original_text": "你好世界",
  "translated_text": "Hello world",
  "source_language": "zh-cn",
  "target_language": "en",
  "model_used": "Helsinki-NLP/opus-mt-zh-en"
}
```

### 飞书专用接口

**POST** `/feishu/translate`

自动处理飞书消息格式，返回适合飞书的回复格式。

## 🛠️ 管理命令

```bash
# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 清理所有数据
docker-compose down -v

# 进入n8n容器
docker-compose exec n8n bash

# 备份数据
docker-compose exec postgres pg_dump -U n8n_user n8n > backup.sql
```

## 📈 性能优化

### 模型优化
- 使用CPU优化的模型版本
- 启用模型缓存机制
- 实现批量处理

### 缓存策略
- Redis缓存翻译结果
- 避免重复翻译相同文本
- 设置合理的缓存过期时间

### 资源监控
```bash
# 查看资源使用情况
docker stats

# 查看磁盘使用
docker system df

# 清理未使用的镜像
docker system prune
```

## 🔒 安全配置

### 网络安全
- 修改默认密码
- 使用HTTPS（生产环境）
- 配置防火墙规则
- 限制访问IP范围

### 数据安全
- 定期备份数据
- 加密敏感信息
- 使用强密码
- 定期更新组件

## 🐛 故障排除

### 常见问题

1. **Docker服务启动失败**
   ```bash
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   ```

2. **n8n无法访问**
   - 检查端口是否被占用
   - 确认防火墙设置
   - 查看容器日志

3. **翻译API连接失败**
   - 验证ngrok是否正常
   - 检查API服务状态
   - 确认网络连通性

4. **飞书消息接收不到**
   - 检查webhook地址配置
   - 验证飞书应用权限
   - 确认事件订阅设置

### 日志分析

```bash
# n8n日志
docker-compose logs n8n

# 数据库日志
docker-compose logs postgres

# Redis日志
docker-compose logs redis

# 所有服务日志
docker-compose logs
```

## 📚 扩展功能

### 支持更多语言
- 添加新的翻译模型
- 扩展语言检测逻辑
- 更新工作流配置

### 集成更多平台
- 微信机器人
- 钉钉机器人
- Slack集成
- Telegram机器人

### 高级功能
- 语音消息翻译
- 图片文字识别翻译
- 实时会话翻译
- 翻译历史记录

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request

## 📄 许可证

MIT License - 详见LICENSE文件

## 📞 支持与反馈

- 提交Issue: [GitHub Issues](https://github.com/your-repo/issues)
- 讨论交流: [GitHub Discussions](https://github.com/your-repo/discussions)
- 邮件联系: your-email@example.com

## 🙏 致谢

- [n8n](https://n8n.io/) - 工作流自动化平台
- [Hugging Face](https://huggingface.co/) - 预训练模型
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [飞书开放平台](https://open.feishu.cn/) - API支持

---

**⭐ 如果这个项目对你有帮助，请给个Star！** 