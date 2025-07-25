# AI旅行规划智能体

基于Ubuntu22.04.4和Python3.10开发的个人旅行规划智能体，集成大模型提示词工程、上下文工程、MCP、RAG、vLLM推理、n8n工作流和LangChain多角色智能体技术。

## 项目结构

```
ai-travel-planner/
├── services/                 # 微服务目录
│   ├── api-gateway/         # API网关服务
│   ├── chat-service/        # 对话管理服务
│   ├── agent-service/       # 智能体服务
│   ├── vllm-service/        # vLLM推理服务
│   ├── rag-service/         # RAG检索服务
│   └── workflow-service/    # n8n工作流服务
├── shared/                  # 共享代码库
│   ├── models/             # 数据模型
│   ├── utils/              # 工具函数
│   └── config/             # 配置管理
├── frontend/               # 前端应用
├── docker/                 # Docker配置文件
├── scripts/                # 部署和管理脚本
├── tests/                  # 测试文件
├── docs/                   # 文档
└── requirements/           # 依赖管理
```

## 技术栈

- **Python**: 3.10
- **框架**: FastAPI, LangChain
- **AI推理**: vLLM, Qwen2.5-7B-Instruct
- **数据库**: PostgreSQL, Redis, Qdrant
- **工作流**: n8n
- **容器化**: Docker, Docker Compose
- **前端**: React/Vue.js

## 快速开始

1. 克隆项目
```bash
git clone <repository-url>
cd ai-travel-planner
```

2. 设置Python环境
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt
```

3. 启动开发环境
```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```

## 开发指南

详细的开发指南请参考 [docs/development.md](docs/development.md)