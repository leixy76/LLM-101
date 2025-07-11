#!/usr/bin/env python3
"""
自动化脚本：将Anthropic Jupyter notebook教程转换为OpenAI版本
- 将Anthropic API调用替换为OpenAI API调用
- 将Claude模型引用替换为GPT模型引用
- 更新相关文档链接和说明
"""

import json
import os
import re
from pathlib import Path

def convert_anthropic_to_openai(text):
    """将文本中的Anthropic相关内容转换为OpenAI"""
    
    # 基本替换映射
    replacements = {
        # 库和客户端
        'anthropic': 'openai',
        'import anthropic': 'import openai',
        '!pip install anthropic': '%pip install openai==1.61.0',
        '%pip install anthropic': '%pip install openai==1.61.0',
        'anthropic.Anthropic': 'openai.OpenAI',
        'client = anthropic.Anthropic(api_key=API_KEY)': 'client = openai.OpenAI(api_key=API_KEY)',
        
        # 模型名称
        'Claude': 'GPT',
        'claude': 'gpt',
        'Claude 3': 'GPT-4o',
        'claude-3': 'gpt-4o',
        'Claude-3': 'GPT-4o',
        'claude-3-haiku-20240307': 'gpt-4o-mini',
        'claude-3-sonnet-20240229': 'gpt-4o',
        'claude-3-opus-20240229': 'gpt-4o',
        'claude-3-5-sonnet-20241022': 'gpt-4o',
        'claude-3-5-haiku-20241022': 'gpt-4o-mini',
        
        # API调用
        'client.messages.create': 'client.chat.completions.create',
        'message.content[0].text': 'response.choices[0].message.content',
        'messages.create': 'chat.completions.create',
        
        # 文档链接
        'docs.anthropic.com': 'platform.openai.com/docs',
        'Anthropic': 'OpenAI',
        'API文档](https://docs.anthropic.com/claude/reference/messages_post)': 'API文档](https://platform.openai.com/docs/api-reference/chat)',
        '[如何使用系统提示](https://docs.anthropic.com/claude/docs/how-to-use-system-prompts)': '[系统消息最佳实践](https://platform.openai.com/docs/guides/prompt-engineering)',
        
        # API术语
        '消息API': 'Chat Completions API',
        'messages API': 'Chat Completions API',
        'Message API': 'Chat Completions API',
        '文本完成API': 'Legacy Completions API',
        
        # 错误处理相关
        'message = client.messages.create': 'response = client.chat.completions.create',
        'return message.content[0].text': 'return response.choices[0].message.content',
        
        # 响应相关
        'Claude的响应': 'GPT的响应',
        'Claude响应': 'GPT响应',
        '获取Claude的完成响应': '获取GPT的完成响应',
        '打印Claude的响应': '打印GPT的响应',
        '获取Claude的响应': '获取GPT的响应',
        
        # 系统提示相关
        'system=system_prompt': '# system消息通过messages处理',
        'system=': '# system参数在OpenAI中通过messages处理: ',
    }
    
    # 执行替换
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    return result

def convert_api_call_structure(text):
    """转换API调用结构"""
    
    # 查找并替换client.messages.create调用
    pattern = r'client\.messages\.create\s*\(\s*model=([^,]+),\s*max_tokens=([^,]+),\s*temperature=([^,]+),\s*system=([^,]+),\s*messages=\[\s*\{"role": "user", "content": ([^}]+)\}\s*\]\s*\)'
    
    def replace_api_call(match):
        model = match.group(1)
        max_tokens = match.group(2)
        temperature = match.group(3)
        system = match.group(4)
        prompt = match.group(5)
        
        return f'''# 构建消息列表
    messages = []
    
    # 如果有系统提示，添加系统消息
    if {system}:
        messages.append({{"role": "system", "content": {system}}})
    
    # 添加用户消息
    messages.append({{"role": "user", "content": {prompt}}})
    
    # 调用OpenAI API
    response = client.chat.completions.create(
        model={model},              # 模型名称 (gpt-4o 或 deepseek-r1)
        messages=messages,             # 消息列表
        max_tokens={max_tokens},              # 最大token数
        temperature={temperature}               # 温度参数，0表示更确定性
    )'''
    
    result = re.sub(pattern, replace_api_call, text, flags=re.MULTILINE | re.DOTALL)
    return result

def add_model_check(text):
    """添加模型名称检查代码"""
    if 'MODEL_NAME' in text and 'try:' not in text:
        model_check = '''# 如果没有设置MODEL_NAME，使用默认值
try:
    MODEL_NAME
except NameError:
    MODEL_NAME = "gpt-4o"  # 默认使用gpt-4o模型

'''
        # 在创建客户端之前插入检查代码
        text = text.replace('# 创建OpenAI客户端', model_check + '# 创建OpenAI客户端')
    return text

def convert_notebook_cell(cell):
    """转换单个notebook cell"""
    if cell['cell_type'] == 'code':
        # 转换代码cell
        if 'source' in cell:
            source_lines = cell['source']
            if isinstance(source_lines, list):
                converted_lines = []
                for line in source_lines:
                    converted_line = convert_anthropic_to_openai(line)
                    converted_line = convert_api_call_structure(converted_line)
                    converted_line = add_model_check(converted_line)
                    converted_lines.append(converted_line)
                cell['source'] = converted_lines
            else:
                converted = convert_anthropic_to_openai(source_lines)
                converted = convert_api_call_structure(converted)
                converted = add_model_check(converted)
                cell['source'] = converted
    
    elif cell['cell_type'] == 'markdown':
        # 转换markdown cell
        if 'source' in cell:
            source_lines = cell['source']
            if isinstance(source_lines, list):
                converted_lines = []
                for line in source_lines:
                    converted_lines.append(convert_anthropic_to_openai(line))
                cell['source'] = converted_lines
            else:
                cell['source'] = convert_anthropic_to_openai(source_lines)
    
    return cell

def convert_notebook_file(file_path):
    """转换整个notebook文件"""
    print(f"转换文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # 转换所有cells
        if 'cells' in notebook:
            for i, cell in enumerate(notebook['cells']):
                notebook['cells'][i] = convert_notebook_cell(cell)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        print(f"✅ 成功转换: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败 {file_path}: {e}")
        return False

def main():
    """主函数：批量转换所有notebook文件"""
    
    # 获取当前目录下的所有.ipynb文件
    current_dir = Path('.')
    notebook_files = list(current_dir.glob('*.ipynb'))
    
    if not notebook_files:
        print("未找到任何.ipynb文件")
        return
    
    print(f"找到 {len(notebook_files)} 个notebook文件")
    print("开始转换...")
    
    success_count = 0
    for notebook_file in notebook_files:
        if convert_notebook_file(notebook_file):
            success_count += 1
    
    print(f"\n转换完成！成功: {success_count}/{len(notebook_files)}")
    
    # 也转换hints.py文件
    hints_file = Path('hints.py')
    if hints_file.exists():
        print("\n转换hints.py文件...")
        try:
            with open(hints_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            converted_content = convert_anthropic_to_openai(content)
            
            # 对hints.py特殊处理，将Claude相关的内容替换
            converted_content = converted_content.replace(
                '本练习中的评分函数正在寻找包含确切阿拉伯数字"1"、"2"和"3"的答案。\n您通常可以通过简单地要求Claude做您想要的事情来实现目标。',
                '本练习中的评分函数正在寻找包含确切阿拉伯数字"1"、"2"和"3"的答案。\n您通常可以通过简单地要求GPT做您想要的事情来实现目标。'
            )
            
            with open(hints_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            
            print("✅ 成功转换hints.py")
        except Exception as e:
            print(f"❌ 转换hints.py失败: {e}")

if __name__ == "__main__":
    main() 