#!/usr/bin/env python3
"""
测试OpenAI API转换是否成功的简单脚本
"""

import os
import sys

def test_conversion():
    """测试转换结果"""
    print("🔍 测试OpenAI教程转换结果...")
    
    # 检查必要文件是否存在
    required_files = [
        "01_Basic_Prompt_Structure.ipynb",
        "02_Being_Clear_and_Direct.ipynb", 
        "03_Assigning_Roles_Role_Prompting.ipynb",
        "README_CN.md",
        "hints.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件都存在")
    
    # 检查文件内容是否已转换
    test_results = []
    
    # 检查notebook文件
    for notebook in ["01_Basic_Prompt_Structure.ipynb", "02_Being_Clear_and_Direct.ipynb"]:
        with open(notebook, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否包含OpenAI相关内容
        if 'openai' in content and 'GPT' in content:
            test_results.append(f"✅ {notebook} - 已转换为OpenAI版本")
        else:
            test_results.append(f"❌ {notebook} - 未完全转换")
    
    # 检查README
    with open("README_CN.md", 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    if 'OpenAI GPT' in readme_content and 'gpt-4o' in readme_content:
        test_results.append("✅ README_CN.md - 已更新为OpenAI版本")
    else:
        test_results.append("❌ README_CN.md - 未完全更新")
    
    # 输出测试结果
    print("\n📊 转换结果:")
    for result in test_results:
        print(f"  {result}")
    
    # 总结
    success_count = sum(1 for r in test_results if r.startswith("✅"))
    total_count = len(test_results)
    
    print(f"\n📈 转换进度: {success_count}/{total_count} 个文件已成功转换")
    
    if success_count == total_count:
        print("🎉 所有文件转换成功！")
        return True
    else:
        print("⚠️  部分文件需要进一步转换")
        return False

def show_usage_example():
    """显示使用示例"""
    print("\n💡 使用示例:")
    print("""
# 1. 安装依赖
pip install openai==1.61.0 jupyter

# 2. 在Jupyter notebook中设置API密钥
API_KEY = "your-openai-api-key"
MODEL_NAME = "gpt-4o"  # 或 "deepseek-r1"
%store API_KEY
%store MODEL_NAME

# 3. 启动Jupyter
jupyter notebook

# 4. 按顺序运行notebook文件
""")

if __name__ == "__main__":
    success = test_conversion()
    show_usage_example()
    
    if success:
        print("\n🚀 您现在可以开始使用OpenAI GPT版本的提示工程教程了！")
        sys.exit(0)
    else:
        print("\n🔧 请检查转换结果并手动修复剩余问题")
        sys.exit(1)
