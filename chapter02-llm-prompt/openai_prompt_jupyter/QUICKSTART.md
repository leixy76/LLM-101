# 🚀 快速开始指南

## 一键安装

```bash
# 安装依赖
pip install openai==1.61.0 jupyter

# 进入教程目录
cd chapter02-llm-prompt/openai_prompt_jupyter/

# 启动Jupyter
jupyter notebook
```

## 设置API密钥

在第一个notebook cell中运行：

```python
# OpenAI API
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MODEL_NAME = "gpt-4o"

# 或使用DeepSeek API
# API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
# MODEL_NAME = "deepseek-r1"

%store API_KEY
%store MODEL_NAME
```

## 学习路径

1. **01_Basic_Prompt_Structure.ipynb** ← 从这里开始
2. **02_Being_Clear_and_Direct.ipynb**
3. **03_Assigning_Roles_Role_Prompting.ipynb**

## 支持的模型

- `gpt-4o` - OpenAI最新模型（推荐）
- `deepseek-r1` - DeepSeek推理模型
- `gpt-4o-mini` - 轻量级版本

## 遇到问题？

1. 检查API密钥是否正确
2. 确认网络连接正常  
3. 查看 [故障排除指南](INSTALL_GUIDE.md#故障排除)

🎉 开始您的提示工程学习之旅！
