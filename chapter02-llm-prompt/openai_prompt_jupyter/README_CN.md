# OpenAI GPT 提示工程教程 - 中文版

## 项目简介

这是基于 Anthropic 官方 Claude 提示工程教程改造的 OpenAI GPT 版本中文教程。本项目旨在帮助中文用户更好地理解和学习如何有效使用 OpenAI GPT 模型（如 gpt-4o、deepseek-r1 等）。

## 已完成转换

### 基础教程

**已转换的文件**:
- `01_Basic_Prompt_Structure.ipynb` - 基础提示结构
- `02_Being_Clear_and_Direct.ipynb` - 明确和直接的提示
- `03_Assigning_Roles_Role_Prompting.ipynb` - 角色提示工程

**主要内容**:
- OpenAI Chat Completions API 的基本概念和使用方法
- 如何通过清晰直接的提示提高 GPT 响应的准确性
- 角色提示技术和最佳实践
- 系统消息的使用方法
- 函数调用风格的实现
- 丰富的代码示例和练习

**核心特性**:
- ✅ 完整的中文翻译
- ✅ 从 Anthropic API 转换为 OpenAI API
- ✅ 支持 gpt-4o 和 deepseek-r1 模型
- ✅ 详细的中文代码注释
- ✅ 实用的示例和练习
- ✅ 清晰的概念解释
- ✅ 最佳实践指导

## 使用方法

### 环境要求

```bash
pip install openai==1.61.0 jupyter
```

### 设置 API 密钥

在运行 notebook 之前，您需要设置 OpenAI API 密钥：

```python
# 在 Jupyter notebook 中运行
API_KEY = "your-openai-api-key-here"
MODEL_NAME = "gpt-4o"  # 或 "deepseek-r1"

%store API_KEY
%store MODEL_NAME
```

### 支持的模型

- **gpt-4o**: OpenAI 的最新模型，推荐用于大多数任务
- **deepseek-r1**: DeepSeek 的推理模型，适合复杂推理任务
- **gpt-4o-mini**: 轻量级版本，适合简单任务

### 运行教程

1. 打开 Jupyter notebook
2. 加载对应的 `.ipynb` 文件
3. 按顺序执行单元格
4. 在练习部分尝试自己的提示

## 学习目标

通过本教程，您将学会：

1. **理解 OpenAI API 的基本使用**
   - Chat Completions API 的调用方法
   - 消息格式和参数设置
   - 错误处理和最佳实践

2. **掌握提示工程技巧**
   - 如何编写清晰有效的提示
   - 如何使用系统消息设定角色
   - 如何避免常见的提示工程陷阱

3. **应用实际场景**
   - 文本处理和改进
   - 角色扮演和风格控制
   - 逻辑推理和数学问题

## 代码示例亮点

### 基本 API 调用
```python
import openai

client = openai.OpenAI(api_key="your-api-key")

def get_completion(prompt: str, system_prompt=""):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=2000,
        temperature=0.0
    )
    return response.choices[0].message.content
```

### 角色提示示例
```python
# 设置角色提示
system_prompt = "You are a helpful math tutor who explains concepts clearly."
user_prompt = "Explain what algebra is in simple terms."

response = get_completion(user_prompt, system_prompt)
print(response)
```

## 技术架构

```
OpenAI API 调用流程:
用户输入 → 构建消息 → API调用 → GPT响应 → 解析输出
    ↓           ↓           ↓           ↓
  提示工程   → 消息格式   → 模型推理   → 结果处理
```

## API 转换说明

本教程从原始的 Anthropic Claude API 转换为 OpenAI API，主要变化包括：

1. **库导入**: `anthropic` → `openai`
2. **客户端创建**: `anthropic.Anthropic()` → `openai.OpenAI()`
3. **API调用**: `client.messages.create()` → `client.chat.completions.create()`
4. **响应解析**: `message.content[0].text` → `response.choices[0].message.content`
5. **系统提示**: 从 `system` 参数改为消息列表中的 `system` 角色

## 最佳实践

1. **清晰的指令**
   - 使用具体、明确的语言
   - 提供足够的上下文信息
   - 避免模糊或多义的表达

2. **合理使用系统提示**
   - 设定合适的角色和行为准则
   - 控制输出格式和风格
   - 提供专业领域的背景知识

3. **参数调优**
   - 根据任务调整 temperature 参数
   - 设置合理的 max_tokens 限制
   - 选择合适的模型版本

## 模型对比

| 特性 | gpt-4o | deepseek-r1 | gpt-4o-mini |
|------|--------|-------------|-------------|
| 推理能力 | 优秀 | 专业推理 | 良好 |
| 速度 | 快 | 中等 | 最快 |
| 成本 | 中等 | 较低 | 最低 |
| 适用场景 | 通用任务 | 复杂推理 | 简单任务 |

## 贡献指南

欢迎贡献更多的改进和扩展：

1. Fork 本项目
2. 创建功能分支
3. 提交您的改进
4. 发起 Pull Request

## 许可证

本项目遵循原始教程的许可证条款。

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。

---

**注意**: 使用本教程需要有效的 OpenAI API 密钥。请确保遵守 OpenAI 的使用条款和政策。支持的模型包括 gpt-4o 和 deepseek-r1 等。 