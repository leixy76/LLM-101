# OpenAI GPT 提示工程教程 - 安装和使用指南

## 快速开始

### 1. 环境准备

确保您的系统已安装 Python 3.8+ 和 pip。

```bash
# 检查Python版本
python --version

# 安装必需的包
pip install openai==1.61.0 jupyter notebook ipywidgets
```

### 2. 获取API密钥

#### OpenAI API密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录或注册账户
3. 前往 API Keys 页面
4. 创建新的API密钥
5. 保存密钥（只显示一次）

#### DeepSeek API密钥（可选）
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册并获取API密钥

### 3. 配置环境

#### 方法一：Jupyter Notebook 内配置（推荐）
```python
# 在第一个notebook cell中运行
API_KEY = "your-openai-api-key-here"
MODEL_NAME = "gpt-4o"  # 或 "deepseek-r1"

# 保存到IPython存储
%store API_KEY
%store MODEL_NAME
```

#### 方法二：环境变量配置
```bash
# Linux/Mac
export OPENAI_API_KEY="your-openai-api-key-here"

# Windows
set OPENAI_API_KEY=your-openai-api-key-here
```

### 4. 启动教程

```bash
# 进入教程目录
cd chapter02-llm-prompt/openai_prompt_jupyter/

# 启动Jupyter Notebook
jupyter notebook
```

### 5. 选择学习路径

建议按以下顺序学习：

1. **01_Basic_Prompt_Structure.ipynb** - 了解基础API调用
2. **02_Being_Clear_and_Direct.ipynb** - 学习清晰的提示写法
3. **03_Assigning_Roles_Role_Prompting.ipynb** - 掌握角色提示技巧
4. **04_Separating_Data_and_Instructions.ipynb** - 数据与指令分离
5. **05_Formatting_Output_and_Speaking_for_Claude.ipynb** - 输出格式化
6. **06_Precognition_Thinking_Step_by_Step.ipynb** - 逐步思考技术
7. **07_Using_Examples_Few-Shot_Prompting.ipynb** - 少样本学习
8. **08_Avoiding_Hallucinations.ipynb** - 避免模型幻觉
9. **09_Complex_Prompts_from_Scratch.ipynb** - 复杂提示构建

## 支持的模型

### OpenAI 模型
- **gpt-4o**: 最新的多模态模型，推荐用于大多数任务
- **gpt-4o-mini**: 轻量级版本，成本更低
- **gpt-4-turbo**: 高性能版本

### DeepSeek 模型
- **deepseek-r1**: 专业推理模型，适合复杂逻辑任务
- **deepseek-chat**: 通用对话模型

## 示例代码

### 基础API调用
```python
import openai

# 创建客户端
client = openai.OpenAI(api_key="your-api-key")

def get_completion(prompt: str, system_prompt="", model="gpt-4o"):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=2000,
        temperature=0.0
    )
    return response.choices[0].message.content

# 使用示例
response = get_completion("Hello, how are you?")
print(response)
```

### 使用DeepSeek模型
```python
# 如果使用DeepSeek API
client = openai.OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com"  # DeepSeek API端点
)

response = get_completion("解释什么是机器学习", model="deepseek-r1")
print(response)
```

## 常见问题

### Q: API调用失败怎么办？
A: 检查以下几点：
1. API密钥是否正确
2. 账户是否有余额
3. 网络连接是否正常
4. 模型名称是否正确

### Q: 如何切换模型？
A: 修改 `MODEL_NAME` 变量：
```python
MODEL_NAME = "gpt-4o-mini"  # 切换到mini版本
%store MODEL_NAME
```

### Q: 如何控制成本？
A: 
1. 使用 `gpt-4o-mini` 等较便宜的模型
2. 降低 `max_tokens` 参数
3. 在开发时使用较小的测试样本

### Q: 响应质量不好怎么办？
A: 
1. 优化提示词，使其更清晰具体
2. 使用系统提示设定角色
3. 提供更多上下文信息
4. 尝试不同的temperature值

## 性能优化建议

### 1. 提示工程最佳实践
- 使用清晰、具体的指令
- 提供充分的上下文
- 使用示例来说明期望的输出格式
- 合理设置系统提示

### 2. API调用优化
- 批量处理请求以提高效率
- 合理设置超时时间
- 实现重试机制
- 缓存常用响应

### 3. 成本控制
- 根据任务复杂度选择合适的模型
- 设置合理的token限制
- 监控API使用量

## 进阶功能

### 1. 流式响应
```python
def get_completion_stream(prompt: str, system_prompt=""):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
```

### 2. 函数调用
```python
def get_completion_with_tools(prompt: str, tools=None):
    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    return response
```

## 故障排除

### 常见错误码
- **401 Unauthorized**: API密钥无效
- **429 Rate Limit**: 请求频率过高
- **500 Internal Server Error**: 服务器错误，稍后重试

### 调试技巧
1. 启用详细日志记录
2. 检查请求和响应格式
3. 使用简单的测试用例验证配置
4. 查看OpenAI官方文档和状态页面

## 资源链接

- [OpenAI API文档](https://platform.openai.com/docs)
- [DeepSeek API文档](https://platform.deepseek.com/api-docs)
- [提示工程指南](https://platform.openai.com/docs/guides/prompt-engineering)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

---

如有问题，请查看项目的GitHub Issues或提交新的问题。 