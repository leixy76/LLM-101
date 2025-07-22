# 基于LangGraph的智能RAG系统：AI博客搜索

## 项目概述
AI博客搜索是一个智能RAG（检索增强生成）应用程序，专门用于增强AI相关博客文章的信息检索能力。该系统利用LangChain、LangGraph和Google的Gemini模型来获取、处理和分析博客内容，为用户提供准确且上下文相关的答案。

## LangGraph工作流程图
![LangGraph-Workflow](https://github.com/user-attachments/assets/07d8a6b5-f1ef-4b7e-b47a-4f14a192bd8a)

## 演示视频
https://github.com/user-attachments/assets/cee07380-d3dc-45f4-ad26-7d944ba9c32b

## 核心功能特性

### 🔍 文档检索系统
- **向量数据库存储**：使用Qdrant作为向量数据库，基于嵌入向量存储和检索博客内容
- **语义搜索**：通过向量相似度匹配实现精准的语义搜索

### 🤖 智能Agent查询处理
- **决策智能**：使用AI驱动的智能体来判断查询是否需要重写、直接回答或需要更多检索
- **自适应处理**：根据查询复杂度自动选择最佳处理策略

### ⚖️ 相关性评估系统
- **自动评分**：使用Google Gemini模型实现自动化的相关性评分系统
- **质量控制**：确保检索到的文档与用户查询高度相关

### 🔄 查询优化重写
- **智能重写**：对结构不良的查询进行优化，提升检索效果
- **语义理解**：深度理解用户意图，生成更精确的查询语句

### 🖥️ Streamlit用户界面
- **友好交互**：提供直观的用户界面，支持博客URL输入和查询操作
- **实时反馈**：即时显示搜索结果和系统状态

### 📊 基于图的工作流
- **状态图管理**：使用LangGraph实现结构化的状态图，提升决策效率
- **流程可视化**：清晰的工作流程，便于理解和调试

## 技术架构栈

### 编程语言与框架
- **编程语言**: [Python 3.10+](https://www.python.org/downloads/release/python-31011/)
- **核心框架**: [LangChain](https://www.langchain.com/) 和 [LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

### 数据库与存储
- **向量数据库**: [Qdrant](https://qdrant.tech/) - 高性能向量搜索引擎

### AI模型服务
- **嵌入模型**: [Google Gemini API (embedding-001)](https://ai.google.dev/gemini-api/docs/embeddings) - 文本向量化
- **对话模型**: [Google Gemini API (gemini-2.0-flash)](https://ai.google.dev/gemini-api/docs/models/gemini#gemini-2.0-flash) - 智能对话生成

### 数据处理工具
- **网页加载器**: [LangChain WebBaseLoader](https://python.langchain.com/docs/integrations/document_loaders/web_base/) - 博客内容抓取
- **文档分割器**: [RecursiveCharacterTextSplitter](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/recursive_text_splitter/) - 智能文本分块

### 用户界面
- **前端框架**: [Streamlit](https://docs.streamlit.io/) - 快速构建Web应用

## LangChain Agent核心概念详解

### 什么是Agent（智能体）？
Agent是一个能够自主决策和执行任务的AI系统。在本项目中，Agent负责：
1. **理解用户查询**：分析用户输入的问题意图
2. **制定执行计划**：决定是否需要检索、重写查询或直接回答
3. **调用工具**：使用检索工具获取相关文档
4. **生成回答**：基于检索到的信息生成准确回答

### LangGraph状态图工作原理
LangGraph使用状态图来管理Agent的决策流程：

```
用户查询 → Agent决策 → 条件分支
                    ├── 需要检索 → 文档检索 → 相关性评估
                    │                      ├── 相关 → 生成答案
                    │                      └── 不相关 → 重写查询
                    └── 直接回答 → 结束
```

### 核心组件说明

#### 1. 状态管理（AgentState）
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```
- 维护对话历史和状态信息
- 确保信息在不同节点间正确传递

#### 2. 文档评分器（grade_documents）
- 评估检索到的文档与查询的相关性
- 返回"generate"（生成答案）或"rewrite"（重写查询）

#### 3. 查询重写器（rewrite）
- 分析原始查询的语义意图
- 生成更精确的查询表述

#### 4. 答案生成器（generate）
- 基于相关文档生成最终答案
- 使用RAG模式确保答案准确性

## 快速开始指南

### 环境准备
1. **安装Python依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **启动应用程序**：
   ```bash
   streamlit run app.py
   ```

### 使用步骤
1. **配置API密钥**：
   - 在侧边栏输入Qdrant主机URL
   - 输入Qdrant API密钥
   - 输入Google Gemini API密钥

2. **添加博客内容**：
   - 粘贴博客文章链接
   - 系统自动抓取并处理内容

3. **开始查询**：
   - 输入关于博客内容的问题
   - 获取智能化的回答

## 项目文件结构
```
ai_blog_search/
├── app.py              # 主应用程序文件
├── README.md           # 英文说明文档
├── README_CN.md        # 中文说明文档
└── requirements.txt    # Python依赖包列表
```

## 学习建议

### 初学者学习路径
1. **理解RAG概念**：先了解检索增强生成的基本原理
2. **学习LangChain基础**：掌握文档加载、分割、嵌入等基本操作
3. **理解Agent概念**：学习智能体的决策机制
4. **实践LangGraph**：通过本项目理解状态图的工作方式

### 进阶学习方向
1. **自定义工具开发**：为Agent添加更多功能工具
2. **优化检索策略**：改进文档检索和相关性评估算法
3. **多模态扩展**：支持图片、视频等多媒体内容
4. **部署优化**：学习生产环境部署和性能优化

## 常见问题解答

### Q: 为什么选择Qdrant作为向量数据库？
A: Qdrant提供高性能的向量搜索能力，支持实时索引更新，适合动态内容检索场景。

### Q: Agent如何决定是否需要重写查询？
A: 通过相关性评分机制，如果检索到的文档相关性低，Agent会自动触发查询重写流程。

### Q: 如何提高检索准确性？
A: 可以通过调整文档分块大小、优化嵌入模型选择、改进相关性评估标准等方式提升准确性。

## 联系方式
<img align="right" src="https://media.giphy.com/media/2HtWpp60NQ9CU/giphy.gif" alt="handshake gif" width="150">

<p align="left">
  <a href="https://linkedin.com/in/codewithcharan" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="codewithcharan" height="30" width="40" style="margin-right: 10px" /></a>
  <a href="https://instagram.com/joyboy._.ig" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="__mr.__.unique" height="30" width="40" /></a>
  <a href="https://twitter.com/Joyboy_x_" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="codewithcharan" height="30" width="40" style="margin-right: 10px" /></a>
</p>

<img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&center=true&vCenter=true&width=500&height=70&duration=4000&lines=感谢您的访问！+👋;+欢迎在LinkedIn联系我!;+期待与您合作交流+:)"/>