#!/usr/bin/env python3
"""
测试中文提示词的脚本
验证修改后的Jupyter notebook文件中的中文提示词是否正确工作
"""

import os
import sys
import json

def test_notebook_chinese_content():
    """测试notebook文件是否包含正确的中文内容"""
    
    test_files = [
        "01_Basic_Prompt_Structure.ipynb",
        "02_Being_Clear_and_Direct.ipynb"
    ]
    
    chinese_keywords = [
        "你好GPT，你好吗？",
        "你能告诉我海洋的颜色吗？",
        "席琳·迪翁出生于哪一年？",
        "天空为什么是蓝色的？",
        "写一首关于机器人的俳句",
        "史上最佳篮球运动员是谁？",
        "[请替换此文本]"
    ]
    
    print("🔍 测试Jupyter notebook文件的中文化...")
    
    for file_name in test_files:
        file_path = file_name
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"\n📁 检查文件: {file_name}")
            
            # 检查是否包含中文关键词
            found_keywords = []
            for keyword in chinese_keywords:
                if keyword in content:
                    found_keywords.append(keyword)
                    print(f"  ✅ 找到中文提示词: {keyword}")
            
            if found_keywords:
                print(f"  📊 该文件包含 {len(found_keywords)} 个中文提示词")
            else:
                print(f"  ⚠️  该文件没有找到预期的中文提示词")
                
        except Exception as e:
            print(f"❌ 读取文件失败 {file_path}: {e}")
    
    print("\n✅ 中文化测试完成!")

def check_replacement_completeness():
    """检查英文到中文的替换是否完整"""
    
    # 常见的英文提示词，应该已经被替换
    english_patterns = [
        "Hi GPT, how are you?",
        "Hello GPT, how are you?",
        "Can you tell me the color of the ocean?",
        "What year was Celine Dion born in?",
        "Why is the sky blue?",
        "Write a haiku about robots",
        "Who is the best basketball player",
        "[Replace this text]"
    ]
    
    test_files = [
        "01_Basic_Prompt_Structure.ipynb",
        "02_Being_Clear_and_Direct.ipynb"
    ]
    
    print("\n🔍 检查英文提示词是否完全替换...")
    
    for file_name in test_files:
        if not os.path.exists(file_name):
            continue
            
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"\n📁 检查文件: {file_name}")
            
            remaining_english = []
            for pattern in english_patterns:
                if pattern in content:
                    remaining_english.append(pattern)
                    print(f"  ⚠️  仍有英文提示词: {pattern}")
            
            if not remaining_english:
                print(f"  ✅ 所有英文提示词都已替换为中文")
            else:
                print(f"  📊 仍有 {len(remaining_english)} 个英文提示词未替换")
                
        except Exception as e:
            print(f"❌ 读取文件失败 {file_name}: {e}")

if __name__ == "__main__":
    print("🚀 开始测试中文提示词...")
    test_notebook_chinese_content()
    check_replacement_completeness()
    print("\n🎉 测试完成!") 