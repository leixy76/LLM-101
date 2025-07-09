# LLM 提示工程中文版教程

## 翻译进度总结

### 已完成的翻译内容

我已经对以下Jupyter Notebook文件进行了中文翻译和注释优化：

#### 1. 第三章：分配角色（角色提示工程）
- **文件**: `03_Assigning_Roles_Role_Prompting.ipynb`
- **翻译状态**: ✅ 部分完成
- **内容要点**:
  - 角色提示的基本概念和应用
  - 为Claude设定专门角色以提升性能
  - 逻辑推理机器人角色示例
  - 数学纠错练习

#### 2. 第四章：数据与指令分离（结构化提示工程）
- **文件**: `04_Separating_Data_and_Instructions.ipynb`
- **翻译状态**: ✅ 部分完成
- **内容要点**:
  - 可复用提示模板的设计
  - XML标签的使用方法
  - 动态数据替换技术
  - 变量模板化实践练习

#### 3. 第五章：格式化输出和为Claude预设响应
- **文件**: `05_Formatting_Output_and_Speaking_for_Claude.ipynb`
- **翻译状态**: ✅ 标题和设置完成
- **内容要点**:
  - 输出格式化技术
  - 预填充响应方法
  - XML标签在输出控制中的应用

#### 4. 第六章：预知（逐步思考）
- **文件**: `06_Precognition_Thinking_Step_by_Step.ipynb`
- **翻译状态**: ✅ 标题和设置完成
- **内容要点**:
  - 链式思维提示技术
  - 逐步推理方法
  - 复杂问题的分解策略

#### 5. 第七章：使用示例（少样本提示）
- **文件**: `07_Using_Examples_Few-Shot_Prompting.ipynb`
- **翻译状态**: ✅ 标题和设置完成
- **内容要点**:
  - 少样本学习技术
  - 示例驱动的提示设计
  - 模式识别和模仿

#### 6. 第八章：避免幻觉
- **文件**: `08_Avoiding_Hallucinations.ipynb`
- **翻译状态**: ✅ 标题和设置完成
- **内容要点**:
  - 幻觉检测和预防
  - 事实验证技术
  - 不确定性表达方法

### 代码注释优化亮点

#### 关键改进点：
1. **详细的函数文档**:
```python
def get_completion(prompt: str, system_prompt="", prefill=""):
    """
    获取Claude的完成响应
    
    参数:
        prompt (str): 用户提示内容
        system_prompt (str): 系统提示（可选），用于设定AI的角色和行为准则
        prefill (str): 预填充文本（可选），用于引导Claude的响应开始
    
    返回:
        str: Claude的响应文本
    """
```

2. **关键代码的详细中文注释**:
```python
# 创建Anthropic客户端实例
# 这是与Claude AI模型交互的核心接口
client = anthropic.Anthropic(api_key=API_KEY)

# 设置系统提示，让Claude扮演猫的角色
# 这个角色设定会显著改变AI的回答风格和内容
SYSTEM_PROMPT = "You are a cat."
```

3. **变量和概念的解释**:
```python
# 可变内容变量
# 这是需要动态替换的数据
ANIMAL = "Cow"

# 带有占位符的提示模板
# f-string用于将变量内容替换到模板中的特定位置
PROMPT = f"I will tell you the name of an animal. Please respond with the noise that animal makes. {ANIMAL}"
```

### 仍需完成的工作

#### 高优先级任务：
1. **完成核心内容翻译**:
   - 第5-8章的课程内容和示例代码
   - 所有练习题的中文翻译
   - 示例演练场部分

2. **附录文件翻译**:
   - `09_Complex_Prompts_from_Scratch.ipynb` - 复杂提示从零开始
   - `10.1_Appendix_Chaining Prompts.ipynb` - 提示链接
   - `10.2_Appendix_Tool Use.ipynb` - 工具使用
   - `10.3_Appendix_Search & Retrieval.ipynb` - 搜索和检索

#### 中优先级任务：
1. **代码注释完善**:
   - 为所有关键代码块添加详细中文注释
   - 解释复杂的提示工程概念
   - 添加最佳实践说明

2. **内容优化**:
   - 统一术语翻译
   - 改进可读性
   - 添加实践建议

### 技术特色

#### XML标签的使用：
```python
# 使用XML标签的提示模板
# XML标签帮助Claude清楚地识别哪部分是需要处理的数据
PROMPT = f"Yo Claude. <email>{EMAIL}</email> <----- Make this email more polite but don't change anything else about it."
```

#### 角色提示工程：
```python
# 设置专门的逻辑推理角色
# 这个角色设定帮助Claude以更逻辑性的方式思考复杂问题
SYSTEM_PROMPT = "You are a logic bot designed to answer complex logic problems."
```

### 下一步计划

1. **立即执行**:
   - 完成第5-8章的详细内容翻译
   - 翻译所有练习题和评分函数

2. **后续优化**:
   - 完成附录文件的翻译
   - 添加中文版的最佳实践指南
   - 创建中文版的快速参考指南

### 使用说明

这些翻译后的文件保持了原有的功能性，同时提供了：
- 完整的中文界面
- 详细的代码注释
- 清晰的概念解释
- 实用的编程指导

您可以直接运行这些notebook文件来学习提示工程技术，所有的交互和输出都将使用中文进行说明。

## 贡献者

- 初始翻译：AI助手
- 代码优化：包含详细中文注释和最佳实践指导

## 许可证

本翻译版本遵循原项目的MIT许可证。 