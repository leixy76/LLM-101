# 🎯 模块二：大模型基础推理与提示词工程

## 📚 课程概览

本模块深入探讨大模型的推理机制和提示词工程的艺术。你将从零开始理解大模型如何生成文本，掌握各种解码策略，并通过**交互式 Jupyter Notebook 教程**逐步学习如何设计高效、精准的提示词，以最大化模型的性能。

### 🎯 学习目标

- 通过交互式实践理解大模型文本生成的基本原理和解码策略
- 掌握OpenAI官方推荐的提示词设计原则和最佳实践
- 熟练运用思维链(CoT)、自我反思等高级提示词技巧
- 理解并实践大模型函数调用（Function Calling）机制
- 学会提示词的管理、优化和版本控制
- 能够构建完整的AI应用系统

## 🗂️ 项目结构

```
chapter02-llm-prompt/
├── README.md                          # 📖 课程主文档
├── environment.yml                    # 🐍 Conda环境配置
├── requirements.txt                   # 📦 Python依赖包
│
├── openai_prompt_jupyter/             # 🎓 交互式教程（**从这里开始**）
│   ├── INSTALL_GUIDE.md              # 📋 安装使用指南
│   ├── setup_env.sh                  # 🔧 环境配置脚本
│   ├── config.py                     # ⚙️ 配置管理
│   ├── hints.py                      # 💡 教学辅助功能
│   │
│   ├── 00_Tutorial_How-To.ipynb      # 🚀 教程使用指南
│   ├── 01_Basic_Prompt_Structure.ipynb        # 📝 基础提示词结构
│   ├── 02_Being_Clear_and_Direct.ipynb       # 🎯 清晰直接的表达
│   ├── 03_Assigning_Roles_Role_Prompting.ipynb   # 🎭 角色扮演技巧
│   ├── 04_Separating_Data_and_Instructions.ipynb # 📊 数据与指令分离
│   ├── 05_Formatting_Output_and_Speaking_for_Claude.ipynb # 📋 格式化输出
│   ├── 06_Thinking_Step_by_Step.ipynb        # 🧠 逐步思考技术
│   ├── 07_Using_Examples_Few-Shot_Prompting.ipynb    # 📚 少样本学习
│   ├── 08_Avoiding_Hallucinations.ipynb      # ⚠️ 避免模型幻觉
│   ├── 09_Complex_Prompts_from_Scratch.ipynb # 🏗️ 复杂提示词构建
│   └── 10_Tool_Use.ipynb             # 🔧 工具使用和函数调用
│
├── run_demo.py                        # 🎮 统一演示启动器
├── prompt_engineering_demo.py         # 🧪 基础演示代码
│
├── advanced_prompting/                # 🚀 高级提示词技巧
│   ├── chain_of_thought.py           # 🔗 思维链实现
│   └── self_reflection.py            # 🪞 自我反思技巧
│
├── function_calling/                  # 🛠️ 函数调用实战
│   ├── basic_function_calling.py     # 🔧 基础函数调用
│   ├── weather_assistant.py          # 🌤️ 天气查询助手
│   ├── calculator_agent.py           # 🧮 计算器代理
│   └── api_integration.py            # 🔗 API集成示例
│
├── prompt_management/                 # 📚 提示词管理系统
│   └──  prompt_manager.py             # 📝 提示词管理器
│
├── content_generation/                # ✍️ 内容生成应用
│   └── document_generator.py         # 📄 文档生成器
│
├── templates/                         # 📚 提示词模板库
│   └── business/                     # 💼 商业场景模板
│       └── marketing_templates.yaml  # 📢 营销模板
│
├── examples/                          # 🎯 实战案例
│   └── comprehensive_demo.py         # 🌟 综合技术演示
│
├── prompts_best_practice/             # 💎 最佳实践案例
│   ├── 提示词-文本案例/              # 📝 文本处理案例
│   ├── 提示词-视频案例/              # 🎬 视频生成案例
│   ├── 提示词-图表案例/              # 📊 图表分析案例
│   ├── 提示词-技巧/                  # 💡 高级技巧
│   ├── 提示词评判/                   # ⚖️ 质量评估
│   ├── 提示词优化/                   # 🔧 优化方法
│   └── 提示词生成/                   # 🎨 自动生成
│
└── prompts_storage/                   # 💾 提示词存储
    ├── templates.json                # 🗂️ 模板存储
    └── executions.json               # 📊 执行记录
```

## 🚀 学习路径（零基础推荐）

### 📚 第一阶段：交互式入门（必修）

> **⚠️ 重要提示：强烈建议从 Jupyter Notebook 教程开始学习！**

#### 🎯 为什么从 Jupyter 开始？
- **交互式学习**：即时看到结果，快速理解概念
- **官方最佳实践**：基于 OpenAI 和 Anthropic 官方教程
- **渐进式设计**：从简单到复杂，适合零基础学习
- **实时调试**：可以修改代码立即验证效果

#### 📖 学习顺序
1. **环境配置和快速入门**
   ```bash
   cd chapter02-llm-prompt/openai_prompt_jupyter/
   jupyter notebook 00_Tutorial_How-To.ipynb
   ```

2. **基础教程系列**（按顺序学习）
   - `01_Basic_Prompt_Structure.ipynb` - 🔧 API调用和基本结构
   - `02_Being_Clear_and_Direct.ipynb` - 🎯 清晰表达的重要性
   - `03_Assigning_Roles_Role_Prompting.ipynb` - 🎭 角色设定技巧

3. **进阶技巧系列**
   - `04_Separating_Data_and_Instructions.ipynb` - 📊 分离数据和指令
   - `05_Formatting_Output_and_Speaking_for_Claude.ipynb` - 📋 输出格式控制
   - `06_Thinking_Step_by_Step.ipynb` - 🧠 思维链技术

4. **高级应用系列**
   - `07_Using_Examples_Few-Shot_Prompting.ipynb` - 📚 少样本学习
   - `08_Avoiding_Hallucinations.ipynb` - ⚠️ 减少错误生成
   - `09_Complex_Prompts_from_Scratch.ipynb` - 🏗️ 复杂系统构建
   - `10_Tool_Use.ipynb` - 🔧 函数调用和工具使用

### 🛠️ 第二阶段：系统实践（选修）

完成 Jupyter 教程后，可以通过统一演示系统巩固学习：

```bash
# 运行统一演示系统
python run_demo.py
```

### 🚀 第三阶段：项目实战（进阶）

根据需求选择具体模块深入学习和实践。

## 📋 环境准备

### 1. 快速开始（推荐）

#### 使用 Conda 环境管理
```bash
# 进入模块目录
cd chapter02-llm-prompt

# 创建并激活环境
conda env create -f environment.yml
conda activate llm101-prompt

# 配置API密钥（选择其一）
export OPENAI_API_KEY="your-openai-api-key"
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# 启动 Jupyter 教程
cd openai_prompt_jupyter/
jupyter notebook
```

#### 使用虚拟环境
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
export OPENAI_API_KEY="your-openai-api-key"

# 启动教程
cd openai_prompt_jupyter/
jupyter notebook
```

### 2. API 密钥获取

#### OpenAI API 密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账户
3. 前往 API Keys 页面创建密钥
4. 设置环境变量或在 notebook 中配置

#### DeepSeek API 密钥（可选）
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册并获取免费 API 密钥

#### 国内用户代理（可选）
```bash
# 使用国内代理服务
export OPENAI_BASE_URL="https://vip.apiyi.com/v1"
```

### 3. 环境验证

运行环境检查：
```bash
python -c "
import openai
print('✅ OpenAI SDK 已安装')
try:
    import os
    if os.getenv('OPENAI_API_KEY') or os.getenv('DEEPSEEK_API_KEY'):
        print('✅ API 密钥已配置')
    else:
        print('⚠️ 需要配置 API 密钥')
except:
    print('❌ 配置检查失败')
"
```

## 📖 理论基础

### 1. 大模型推理基础

#### 文本生成原理
- **自回归生成**：模型逐个预测下一个词（token）
- **条件生成**：基于前文上下文生成后续内容
- **Tokenization**：将文本转换为模型可理解的数字序列
- **Embedding**：词向量表示，在高维语义空间中编码含义

#### 解码策略详解
```python
# 贪婪解码：每次选择概率最高的token
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "你好"}],
    temperature=0.0  # 确定性输出
)

# 随机采样：增加创造性
response = client.chat.completions.create(
    model="gpt-4o", 
    messages=[{"role": "user", "content": "写一首诗"}],
    temperature=0.8,  # 提高随机性
    top_p=0.9        # 核采样
)
```

### 2. 提示词工程核心概念

#### 基础设计原则
1. **清晰具体**：明确表达任务要求，避免歧义
2. **角色设定**：为AI分配专业角色增强专业性
3. **格式化输出**：指定清晰的输出格式和结构
4. **上下文丰富**：提供充足的背景信息和示例

#### 学习范式对比
```python
# Zero-shot：无示例直接执行
prompt = "分析这篇文章的情感倾向：[文章内容]"

# Few-shot：提供示例
prompt = """
情感分析示例：
文章："今天天气真好！" → 情感：积极
文章："工作压力太大了。" → 情感：消极

请分析：[目标文章] → 情感：
"""

# Chain-of-Thought：逐步推理
prompt = """
请逐步分析这个问题：
1. 首先理解问题的核心
2. 列出相关要素
3. 逐步推理过程
4. 得出最终结论

问题：[具体问题]
"""
```

## 🛠️ 核心工具和代码分析

### 1. run_demo.py 统一演示系统

这是项目的统一入口，提供了完整的菜单系统来演示各种提示词技术：

```python
# 主要功能模块
def main():
    """主函数 - 提供交互式菜单"""
    print_banner()          # 显示欢迎界面
    
    if not check_environment():  # 检查环境配置
        return
    
    while True:
        print_menu()        # 显示功能菜单
        choice = input("请选择演示模块 (0-10): ")
        
        # 根据选择执行对应功能
        if choice == "1":
            run_basic_demo()           # 基础提示词演示
        elif choice == "2": 
            run_cot_demo()             # 思维链技术
        elif choice == "4":
            run_function_calling_demo() # 函数调用
        # ... 其他选项
```

#### 关键设计亮点：
1. **环境检测**：自动检查API密钥和依赖包
2. **模块化设计**：每个功能独立可测试
3. **错误处理**：友好的错误提示和恢复机制
4. **用户体验**：清晰的菜单导航和进度提示

### 2. 模板系统分析

```python
# 模板应用示例（来自 run_demo.py）
def run_template_demo():
    """演示模板引擎的使用"""
    import yaml
    from jinja2 import Template
    
    # 加载YAML模板配置
    template_file = Path("templates/business/marketing_templates.yaml")
    with open(template_file, 'r', encoding='utf-8') as f:
        templates = yaml.safe_load(f)
    
    # 选择产品描述模板
    product_template = templates['product_description']
    jinja_template = Template(product_template['template'])
    
    # 定义变量数据
    variables = {
        'product_name': '智能运动手表',
        'product_features': '心率监测、GPS定位、运动记录',
        'target_audience': '运动爱好者和健康关注者',
        'unique_selling_point': '7天续航、50米防水',
        'price_range': '1999-2999元'
    }
    
    # 渲染最终提示词
    rendered_prompt = jinja_template.render(**variables)
    
    # 调用LLM生成内容
    result = demo.call_llm([
        {"role": "system", "content": "你是专业的电商文案专家。"},
        {"role": "user", "content": rendered_prompt}
    ])
```

### 3. 性能对比系统

```python
def run_performance_comparison():
    """性能对比分析不同提示词技术的效果"""
    results = demo.demo_performance_comparison()
    
    print("\n📊 详细性能报告：")
    for technique, data in results.items():
        if "error" not in data:
            efficiency = data['word_count'] / data['execution_time']
            print(f"🔍 {technique}:")
            print(f"  ⏱️  执行时间: {data['execution_time']:.3f} 秒")
            print(f"  📝 输出字数: {data['word_count']} 字")
            print(f"  ⚡ 生成效率: {efficiency:.1f} 字/秒")
            print(f"  📄 内容预览: {data['result_preview']}")
```

## 💡 高级提示词技巧

### 1. 思维链技术（Chain of Thought）

```python
def chain_of_thought_example():
    """思维链推理示例"""
    prompt = """
    请用思维链方法解决这个问题：
    
    问题：一个班级有30名学生，其中60%是女生。如果又转来5名男生，现在女生占全班的百分比是多少？
    
    思维步骤：
    1. 首先计算原来的女生人数
    2. 确定原来的男生人数
    3. 计算转入男生后的总人数
    4. 计算女生占新总数的百分比
    
    请按步骤解答：
    """
    
    return prompt
```

### 2. 自我反思技术

```python
def self_reflection_prompt(initial_answer, question):
    """自我反思提示词生成器"""
    reflection_prompt = f"""
    原问题：{question}
    我的初始回答：{initial_answer}
    
    现在请从以下角度审视这个回答：
    1. 准确性检查：回答是否符合事实？
    2. 完整性检查：是否遗漏重要信息？
    3. 逻辑性检查：推理过程是否合理？
    4. 清晰度检查：表达是否容易理解？
    
    基于以上检查，请提供改进后的最终答案：
    """
    return reflection_prompt
```

### 3. 中文提示词最佳实践框架

```python
def chinese_prompt_template():
    """中文提示词标准模板"""
    template = """
【身份设定】
你是一名{role}，拥有{experience}年的{field}专业经验。

【参考信息】
```
{reference_context}
```

【核心任务】
{main_task}

【输出要求】
1. 格式：{output_format}
2. 长度：{length_requirement}  
3. 风格：{style_requirement}
4. 特殊要求：{special_requirements}

【工作流程】
1. {step_1}
2. {step_2}
3. {step_3}

【质量标准】
- {quality_criterion_1}
- {quality_criterion_2}
- {quality_criterion_3}

【开始执行】
用户输入：{user_input}

请按照以上要求完成任务：
"""
    return template
```


## 📊 性能优化指南

### 1. 提示词长度优化

```python
# ❌ 冗长低效的提示词
long_prompt = """
请你作为一个非常专业的、有着多年经验的、深谙各种写作技巧的、
了解各种文案套路的、能够准确把握用户心理的营销专家，
为我们的产品写一段非常吸引人的、能够打动用户的、
让用户产生购买欲望的产品介绍文案...
"""

# ✅ 简洁高效的提示词  
efficient_prompt = """
角色：资深营销专家
任务：为产品写吸引人的介绍文案
要求：突出卖点，激发购买欲
产品：[产品信息]
"""
```

### 2. 温度参数调优

```python
# 不同任务的温度设置建议
task_temperature_guide = {
    "事实查询": 0.0,      # 需要准确性
    "代码生成": 0.1,      # 需要精确性
    "文档写作": 0.3,      # 平衡准确性和流畅性
    "创意写作": 0.7,      # 需要创造性
    "头脑风暴": 0.9       # 最大化创意
}
```

### 3. 批量处理优化

```python
def batch_process_prompts(prompts, batch_size=5):
    """批量处理提示词以提高效率"""
    results = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        # 并发处理一批提示词
        batch_results = process_concurrent(batch)
        results.extend(batch_results)
    return results
```

## 🚀 进阶学习资源

### 官方文档和教程
- [OpenAI 提示词工程指南](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Claude 提示词教程](https://docs.anthropic.com/zh-CN/docs/build-with-claude/prompt-engineering/overview)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

### 学术论文
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Self-Reflection Techniques](https://arxiv.org/abs/2303.11366)
- [Few-Shot Learning](https://arxiv.org/abs/2005.14165)

### 实用工具
- [精选 AI 提示词库](https://www.waytoagi.com/zh/prompts)
- [LangChain 提示词模板](https://python.langchain.com/api_reference/core/prompts.html)
- [提示词调优指南](https://open.dingtalk.com/document/ai-dev/ho-to-tune-prompt-words)

## 🎓 学习成果检验

完成本模块学习后，你应该能够：

### 基础能力
- ✅ 理解大模型的基本工作原理
- ✅ 熟练使用 OpenAI API 进行模型调用
- ✅ 设计清晰有效的基础提示词
- ✅ 运用角色设定和格式化技巧

### 进阶能力
- ✅ 应用思维链和自我反思技术
- ✅ 实现函数调用和工具使用
- ✅ 构建复杂的对话和推理系统
- ✅ 优化提示词性能和成本效益

### 实战能力
- ✅ 建立个人的提示词管理系统
- ✅ 开发特定领域的AI应用
- ✅ 评估和改进提示词效果
- ✅ 解决实际业务问题

## 🆘 常见问题解答

### Q1: API 调用失败怎么办？
**A:** 检查以下几点：
1. API 密钥是否正确设置
2. 网络连接是否正常
3. 账户余额是否充足
4. 请求格式是否正确

### Q2: 如何控制生成成本？
**A:** 几个有效方法：
1. 使用 `gpt-4o-mini` 等便宜模型
2. 设置合理的 `max_tokens` 限制
3. 优化提示词长度
4. 实现结果缓存机制

### Q3: 提示词效果不理想怎么优化？
**A:** 系统化优化流程：
1. 明确具体问题（太模糊/太冗长/不准确）
2. 应用对应技巧（角色设定/示例引导/思维链）
3. A/B 测试不同版本
4. 根据结果迭代改进

### Q4: 如何避免模型幻觉？
**A:** 有效策略包括：
1. 要求引用具体信息源
2. 设置确认和验证步骤
3. 使用较低的温度参数
4. 实施多轮验证机制

---

🎉 **开始你的大模型提示词工程之旅吧！** 从 `openai_prompt_jupyter/00_Tutorial_How-To.ipynb` 开始，逐步掌握这项改变世界的技术！ 


## 参考
- [Kiro的原始Prompt](https://gist.github.com/CypherpunkSamurai/ad7be9c3ea07cf4fe55053323012ab4d)