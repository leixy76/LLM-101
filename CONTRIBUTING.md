# 🤝 贡献指南

感谢您对 LLM-101 项目的关注！我们欢迎所有形式的贡献，包括但不限于代码改进、文档完善、问题报告、功能建议等。

## 📋 贡献方式

### 🐛 报告问题
如果您发现了 bug 或有改进建议，请：
1. 在 [GitHub Issues](https://github.com/FlyAIBox/LLM-101/issues) 中搜索是否已有相关问题
2. 如果没有，请创建新的 Issue，包含以下信息：
   - 问题描述
   - 复现步骤
   - 预期结果
   - 实际结果
   - 环境信息（操作系统、Python版本、依赖版本等）

### 💡 功能建议
我们欢迎新功能的建议：
1. 创建 Feature Request Issue
2. 详细描述功能需求和使用场景
3. 如果可能，提供设计思路或参考资料

### 🔧 代码贡献
1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature-name`
5. 创建 Pull Request

### 📚 文档贡献
- 改进 README.md 或其他文档
- 添加代码注释
- 创建教程或示例
- 翻译文档

## 🛠️ 开发环境搭建

### 1. 克隆项目
```bash
git clone https://github.com/FlyAIBox/LLM-101.git
cd LLM-101
```

### 2. 设置开发环境
```bash
# 运行自动化配置脚本
./setup_env.sh

# 或手动配置
conda create -n llm101-dev python=3.10.18
conda activate llm101-dev
pip install -r requirements.txt
```

### 3. 安装开发工具
```bash
# 代码格式化
pip install black isort flake8

# 类型检查
pip install mypy

# 测试工具
pip install pytest pytest-cov
```

## 📝 代码规范

### Python 代码风格
- 使用 [Black](https://github.com/psf/black) 进行代码格式化
- 使用 [isort](https://github.com/PyCQA/isort) 进行导入排序
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用 [flake8](https://flake8.pycqa.org/) 进行代码检查

### 代码检查
```bash
# 格式化代码
black .
isort .

# 检查代码质量
flake8 .

# 类型检查
mypy .
```

### 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型说明：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建工具或辅助工具的变动

示例：
```
feat(agent): add new travel planning agent
fix(prompt): resolve temperature parameter issue
docs(readme): update installation instructions
```

## 🧪 测试规范

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_specific.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 编写测试
- 为新功能编写单元测试
- 测试文件命名：`test_*.py`
- 测试函数命名：`test_*`
- 使用 pytest fixtures 管理测试数据

### 测试结构
```
tests/
├── conftest.py          # pytest配置和fixtures
├── unit/                # 单元测试
│   ├── test_agents.py
│   ├── test_prompts.py
│   └── test_utils.py
├── integration/         # 集成测试
│   ├── test_api.py
│   └── test_workflows.py
└── fixtures/            # 测试数据
    ├── sample_data.json
    └── mock_responses.py
```

## 📖 文档规范

### 代码文档
- 使用 docstring 为函数、类和模块添加文档
- 遵循 [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) 或 [NumPy Style](https://numpydoc.readthedocs.io/en/latest/format.html)

```python
def analyze_sentiment(text: str, model: str = "gpt-3.5-turbo") -> dict:
    """分析文本情感倾向。
    
    Args:
        text: 要分析的文本
        model: 使用的模型名称
        
    Returns:
        包含情感分析结果的字典
        
    Raises:
        ValueError: 当文本为空时抛出
    """
    pass
```

### README 更新
- 添加新功能时更新 README.md
- 保持示例代码的准确性
- 更新依赖列表和环境要求

## 🎯 贡献重点领域

我们特别欢迎以下方面的贡献：

### 🔥 高优先级
- 新的 Agent 示例和用例
- RAG 系统的优化和改进
- 模型微调的最佳实践
- 性能优化和内存管理

### 🌟 中等优先级
- 更多的提示词工程技巧
- 新的数据处理工具
- 监控和日志系统
- 安全性改进

### 💡 创新功能
- 多模态支持
- 新的工作流自动化
- 企业级功能扩展
- 可视化工具

## 🏆 贡献者认可

我们会在以下地方认可贡献者：
- README.md 中的贡献者列表
- 发布说明中的感谢名单
- 项目官网的贡献者页面

## 📞 联系我们

如果您有任何问题或建议，欢迎通过以下方式联系我们：

- 📧 邮件：fly910905@sina.com
- 💬 GitHub Discussions：[项目讨论区](https://github.com/FlyAIBox/LLM-101/discussions)
- 🐛 GitHub Issues：[问题报告](https://github.com/FlyAIBox/LLM-101/issues)
- 🔗 微信公众号：萤火AI百宝箱

## 📜 许可证

通过贡献代码，您同意您的贡献将按照项目的 [MIT 许可证](LICENSE) 进行许可。

---

<div align="center">

**🙏 感谢您的贡献！**

每一个贡献都让 LLM-101 变得更好，帮助更多人学习和掌握大模型技术。

</div> 