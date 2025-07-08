# 🎯 模块二：大模型基础推理与提示词工程

## 📚 课程概览

本模块深入探讨大模型的核心推理机制和提示词工程的艺术。你将理解大模型如何生成文本，掌握各种解码策略，并学习如何设计高效、精准的提示词，以最大化模型的性能。

### 🎯 学习目标

- 理解大模型文本生成的基本原理和解码策略
- 掌握基础提示词设计原则，能够有效引导模型完成任务
- 熟练运用CoT、自我反思等高级提示词技巧
- 理解并实践大模型函数调用（Function Calling）机制
- 学会提示词的管理、优化和版本控制

## 📖 理论基础

### 1. 大模型推理基础

#### 文本生成原理
- **自回归生成**：逐个token预测的工作机制
- **条件生成**：基于上下文的文本生成
- **Tokenization**：文本到数字的转换过程
- **Embedding**：词向量表示和语义空间

#### 解码策略详解
- **贪婪解码**：每次选择概率最高的token
- **束搜索(Beam Search)**：维护多个候选序列
- **Top-k采样**：从前k个最可能的token中随机选择
- **Top-p采样**：核采样，动态调整候选token数量
- **温度参数(Temperature)**：控制生成的随机性和创造性

### 2. 提示词工程核心概念

#### 基础设计原则
1. **清晰具体**：明确表达任务要求
2. **角色设定**：为AI分配专业角色
3. **格式化输出**：指定输出格式和结构
4. **上下文丰富**：提供充足的背景信息

#### 学习范式
- **Zero-shot学习**：无示例的任务执行
- **Few-shot学习**：基于少量示例的学习
- **In-context学习**：通过上下文学习新任务

## 🚀 实战技巧

### 1. OpenAI官方最佳实践

#### 基础技巧
1. **使用最新模型**：选择性能最佳的模型
2. **指令前置**：将指令放在提示词开头
3. **分隔符使用**：用`###`或`"""`分隔指令和内容
4. **具体描述**：详细说明所需的输出格式和风格

#### 高级技巧
1. **示例驱动**：通过具体示例展示期望格式
2. **渐进式优化**：从零样本到少样本再到微调
3. **明确指导**：说明要做什么而非不要做什么
4. **引导词使用**：用特定词汇引导模型生成

### 2. 高阶提示词技巧

#### 思维链(Chain of Thought, CoT)
```python
# 基础CoT示例
prompt = """
请分析以下数学问题，并逐步展示解题过程：

问题：小明有15个苹果，吃了3个，又买了8个，最后有多少个苹果？

步骤1：计算吃了苹果后的数量
步骤2：计算买了苹果后的总数量
步骤3：给出最终答案

请按步骤分析：
"""
```

#### 自我反思(Self-Reflection)
```python
# 自我反思流程
def self_reflection_process(initial_answer, question):
    reflection_prompt = f"""
    原问题：{question}
    我的初始回答：{initial_answer}
    
    现在请审视这个回答：
    1. 回答是否准确完整？
    2. 有没有遗漏的要点？
    3. 逻辑是否清晰？
    4. 是否需要补充或修正？
    
    请给出改进后的最终答案。
    """
    return reflection_prompt
```

### 3. 中文提示词构成框架

#### 完整框架结构
```python
prompt_template = """
【能力与角色】
你是一名{role}，具有{years}年的{field}经验。

【相关性】
你可以参考以下信息：
```
{reference_info}
```

【指令】
请根据参考信息和用户输入，{task_description}

【上下文】
当前对话背景：{context}

【范例】
以下是一个示例：
用户输入：{example_input}
期望输出：{example_output}

【约束】
1. {constraint_1}
2. {constraint_2}
3. {constraint_3}

【正式开始】
用户输入：{user_input}
请输出：
"""
```

## 🛠️ 项目结构

```
chapter02-llm-prompt/
├── README.md                      # 课程说明文档
├── prompt_engineering_demo.py     # 基础演示代码
├── advanced_prompting/            # 高级提示词技巧
│   ├── chain_of_thought.py       # 思维链实现
│   ├── self_reflection.py        # 自我反思技巧
│   ├── role_playing.py           # 角色扮演提示词
│   └── structured_output.py      # 结构化输出
├── function_calling/              # 函数调用实战
│   ├── basic_function_calling.py # 基础函数调用
│   ├── weather_assistant.py      # 天气查询助手
│   ├── calculator_agent.py       # 计算器代理
│   └── api_integration.py        # API集成示例
├── prompt_management/             # 提示词管理系统
│   ├── prompt_manager.py         # 提示词管理器
│   ├── template_engine.py        # 模板引擎
│   ├── version_control.py        # 版本控制
│   └── optimization_tools.py     # 优化工具
├── content_generation/            # 内容生成应用
│   ├── document_generator.py     # 文档生成器
│   ├── code_generator.py         # 代码生成器
│   ├── image_prompt_generator.py # 图像提示词生成
│   └── video_script_generator.py # 视频脚本生成
├── templates/                     # 提示词模板库
│   ├── business/                 # 商业场景模板
│   ├── education/                # 教育场景模板
│   ├── creative/                 # 创意场景模板
│   └── technical/                # 技术场景模板
├── examples/                      # 实战案例
│   ├── customer_service.py      # 客服场景
│   ├── content_creation.py      # 内容创作
│   ├── data_analysis.py         # 数据分析
│   └── translation_agent.py     # 翻译代理
└── tests/                        # 测试用例
    ├── test_basic_prompts.py     # 基础测试
    ├── test_advanced_prompts.py  # 高级测试
    └── test_function_calling.py  # 函数调用测试
```

## 🚀 快速开始

### 1. 环境准备

#### 方式一：使用Conda环境管理（推荐）

**快速创建（推荐）**
```bash
# 进入模块目录
cd chapter02-llm-prompt

# 使用environment.yml创建环境
conda env create -f environment.yml

# 激活环境
conda activate llm101-prompt

# 配置API密钥
export OPENAI_API_KEY="your-api-key"
# 或
export DEEPSEEK_API_KEY="your-deepseek-key"
```

**手动创建**
```bash
# 创建Conda环境
conda create -n llm101-prompt python=3.10.18

# 激活环境
conda activate llm101-prompt

# 进入模块目录
cd chapter02-llm-prompt

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
export OPENAI_API_KEY="your-api-key"
# 或
export DEEPSEEK_API_KEY="your-deepseek-key"
```

#### 方式二：使用虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Linux/Mac）
source venv/bin/activate
# 或 Windows
# venv\Scripts\activate

# 进入模块目录
cd chapter02-llm-prompt

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
export OPENAI_API_KEY="your-api-key"
# 或
export DEEPSEEK_API_KEY="your-deepseek-key"
```

#### Conda环境管理命令
```bash
# 查看所有环境
conda env list

# 激活环境
conda activate llm101-prompt

# 停用环境
conda deactivate

# 删除环境（如需要）
conda env remove -n llm101-prompt

# 导出环境配置
conda env export > environment.yml

# 从配置文件创建环境
conda env create -f environment.yml
```

### 2. 运行基础演示
```bash
# 运行提示词工程演示
python prompt_engineering_demo.py

# 运行函数调用演示
python function_calling/basic_function_calling.py

# 运行提示词管理演示
python prompt_management/prompt_manager.py
```

### 3. 实战练习
1. **情感分析优化**：比较不同提示词技巧的效果
2. **内容生成实战**：生成文档、代码、图像提示词
3. **函数调用应用**：构建天气查询、计算器等工具
4. **提示词管理**：建立自己的提示词库

## 📈 学习路径

### 初级阶段
1. 理解基础概念和原理
2. 掌握基本提示词设计技巧
3. 练习零样本和少样本学习

### 中级阶段
1. 学习高级技巧（CoT、自我反思）
2. 实践函数调用功能
3. 构建结构化输出系统

### 高级阶段
1. 建立提示词管理系统
2. 优化和版本控制
3. 跨模态内容生成

## 💡 最佳实践

### 提示词设计原则
1. **从简单开始**：先用基础提示词测试
2. **迭代优化**：根据结果不断改进
3. **A/B测试**：比较不同版本的效果
4. **版本管理**：记录和管理提示词变更

### 性能优化技巧
1. **温度调节**：事实性任务用低温度，创意性任务用高温度
2. **长度控制**：合理设置max_tokens
3. **停止序列**：使用stop tokens优化输出
4. **批量处理**：提高处理效率

## 🎯 实战项目

完成本模块后，你将能够：
- 设计高效的提示词系统
- 实现函数调用功能
- 构建内容生成应用
- 管理和优化提示词库
- 应用于实际业务场景

## 📚 延伸阅读

- [OpenAI官方提示词工程指南](https://platform.openai.com/docs/guides/prompt-engineering)
- [OpenAI 提示词工程的最佳实践](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [LangChain提示词模板](https://python.langchain.com/api_reference/core/prompts.html#langchain-core-prompts)
- [思维链论文](https://arxiv.org/abs/2201.11903)
- [自我反思技术](https://arxiv.org/abs/2303.11366) 