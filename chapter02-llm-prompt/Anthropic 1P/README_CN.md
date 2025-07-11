# Anthropic Claude 提示工程教程 - 中文版

## 项目简介

这是 Anthropic 官方 Claude 提示工程教程的中文翻译版本。本项目旨在帮助中文用户更好地理解和学习如何有效使用 Claude AI 模型。

## 已完成翻译

### 附录 10.1：提示链式调用 (Chaining Prompts)

**文件**: `10.1_Appendix_Chaining Prompts_CN.ipynb`

**主要内容**:
- 提示链式调用的基本概念和原理
- 如何通过链式调用提高 Claude 响应的准确性
- 响应改进技术和最佳实践
- 预填充技术的使用方法
- 函数调用风格的实现
- 丰富的代码示例和练习

**核心特性**:
- ✅ 完整的中文翻译
- ✅ 详细的中文代码注释
- ✅ 实用的示例和练习
- ✅ 清晰的概念解释
- ✅ 最佳实践指导

## 使用方法

### 环境要求

```bash
pip install anthropic jupyter
```

### 设置 API 密钥

在运行 notebook 之前，您需要设置 Anthropic API 密钥：

```python
# 在 Jupyter notebook 中运行
API_KEY = "your-api-key-here"
MODEL_NAME = "claude-3-sonnet-20240229"  # 或其他可用模型

%store API_KEY
%store MODEL_NAME
```

### 运行教程

1. 打开 Jupyter notebook
2. 加载 `10.1_Appendix_Chaining Prompts_CN.ipynb`
3. 按顺序执行单元格
4. 在练习场部分尝试自己的提示

## 学习目标

通过本教程，您将学会：

1. **理解提示链式调用的原理**
   - 什么是提示链式调用
   - 为什么它能提高响应质量
   - 何时使用这种技术

2. **掌握实用技巧**
   - 如何要求 Claude 改进其响应
   - 如何使用预填充技术
   - 如何避免过度修正问题

3. **应用实际场景**
   - 文本处理和改进
   - 信息提取和整理
   - 多步骤任务处理

## 代码示例亮点

### 基本链式调用
```python
# 第一步：获取初始响应
first_response = get_completion([{"role": "user", "content": "请列出10个单词"}])

# 第二步：要求改进
messages = [
    {"role": "user", "content": "请列出10个单词"},
    {"role": "assistant", "content": first_response},
    {"role": "user", "content": "请检查并改进这个列表"}
]
improved_response = get_completion(messages)
```

### 预填充技术
```python
# 引导 Claude 以特定格式开始响应
messages = [
    {"role": "user", "content": "从文本中提取姓名"},
    {"role": "assistant", "content": "<names>"}
]
response = get_completion(messages)
```

## 技术架构

```
提示链式调用流程:
用户输入 → Claude响应1 → 改进请求 → Claude响应2 → 最终输出
    ↓           ↓           ↓           ↓
  原始提示   → 初始答案   → 修正提示   → 改进答案
```

## 最佳实践

1. **给 Claude 提供"退路"**
   - 在修正提示中包含"如果已经正确，保持原样"
   - 避免强制修改正确的答案

2. **使用清晰的指令**
   - 明确说明期望的改进方向
   - 提供具体的评判标准

3. **合理使用预填充**
   - 用于控制输出格式
   - 引导特定的响应结构

## 贡献指南

欢迎贡献更多的翻译和改进：

1. Fork 本项目
2. 创建功能分支
3. 提交您的改进
4. 发起 Pull Request

## 许可证

本项目遵循原始 Anthropic 教程的许可证条款。

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。

---

**注意**: 使用本教程需要有效的 Anthropic API 密钥。请确保遵守 Anthropic 的使用条款和政策。 