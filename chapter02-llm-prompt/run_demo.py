#!/usr/bin/env python3
"""
🎮 提示词工程演示启动器
统一入口，用户可以选择运行不同的演示模块
"""

import os
import sys
from pathlib import Path

def print_banner():
    """打印欢迎界面"""
    print("🚀" + "=" * 78 + "🚀")
    print("🎯               LLM-101 提示词工程演示系统                🎯")
    print("🚀" + "=" * 78 + "🚀")
    print("📚 模块二：大模型基础推理与提示词工程")
    print("💡 集成展示：思维链、自我反思、函数调用、内容生成等")
    print("-" * 80)

def print_menu():
    """打印菜单选项"""
    print("\n📋 演示模块菜单：")
    print("-" * 40)
    print("1.  基础提示词工程演示")
    print("2.  思维链(CoT)技术演示") 
    print("3.  自我反思技术演示")
    print("4.  函数调用(Function Calling)演示")
    print("5.  文档生成器演示")
    print("6.  提示词管理系统演示")
    print("7.  提示词模板演示")
    print("8.  综合技术整合演示")
    print("9.  性能对比分析")
    print("10. 全部演示(按序执行)")
    print("-" * 40)
    print("0.  退出系统")
    print("-" * 40)

def run_basic_demo():
    """运行基础演示"""
    print("🔄 启动基础提示词工程演示...")
    try:
        from prompt_engineering_demo import main
        main()
    except Exception as e:
        print(f"❌ 基础演示启动失败: {e}")

def run_cot_demo():
    """运行思维链演示"""
    print("🔄 启动思维链技术演示...")
    try:
        from advanced_prompting.chain_of_thought import main
        main()
    except Exception as e:
        print(f"❌ 思维链演示启动失败: {e}")

def run_reflection_demo():
    """运行自我反思演示"""
    print("🔄 启动自我反思技术演示...")
    try:
        from advanced_prompting.self_reflection import main
        main()
    except Exception as e:
        print(f"❌ 自我反思演示启动失败: {e}")

def run_function_calling_demo():
    """运行函数调用演示"""
    print("🔄 启动函数调用演示...")
    try:
        from function_calling.basic_function_calling import main
        main()
    except Exception as e:
        print(f"❌ 函数调用演示启动失败: {e}")

def run_document_generator_demo():
    """运行文档生成器演示"""
    print("🔄 启动文档生成器演示...")
    try:
        from content_generation.document_generator import main
        main()
    except Exception as e:
        print(f"❌ 文档生成器演示启动失败: {e}")

def run_prompt_manager_demo():
    """运行提示词管理演示"""
    print("🔄 启动提示词管理系统演示...")
    try:
        from prompt_management.prompt_manager import main
        main()
    except Exception as e:
        print(f"❌ 提示词管理演示启动失败: {e}")

def run_template_demo():
    """运行模板应用演示"""
    print("🔄 启动提示词模板演示...")
    try:
        import yaml
        from jinja2 import Template
        from prompt_engineering_demo import PromptEngineeringDemo
        
        # 加载营销模板
        template_file = Path("templates/business/marketing_templates.yaml")
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                templates = yaml.safe_load(f)
            
            print("📋 可用的营销模板：")
            for key, template in templates.items():
                print(f"  • {template['name']}: {template['description']}")
            
            # 演示产品描述生成
            product_template = templates['product_description']
            # 使用Jinja2模板引擎创建模板对象，用于渲染包含变量的提示词模板
            jinja_template = Template(product_template['template'])
            
            variables = {
                'product_name': '智能运动手表',
                'product_features': '心率监测、GPS定位、运动记录、健康分析',
                'target_audience': '运动爱好者和健康关注者',
                'unique_selling_point': '7天续航、50米防水、专业运动算法',
                'price_range': '1999-2999元'
            }
            
            rendered_prompt = jinja_template.render(**variables)
            print(f"\n📝 生成的提示词：\n{rendered_prompt}")
            
            # 使用提示词生成内容
            demo = PromptEngineeringDemo()
            result = demo.call_llm([
                {"role": "system", "content": "你是专业的电商文案专家。"},
                {"role": "user", "content": rendered_prompt}
            ])
            print(f"\n✨ 生成的产品文案：\n{result}")
            
        else:
            print("❌ 模板文件不存在")
            
    except Exception as e:
        print(f"❌ 模板演示启动失败: {e}")

def run_comprehensive_demo():
    """运行综合演示"""
    print("🔄 启动综合技术整合演示...")
    try:
        from examples.comprehensive_demo import main
        main()
    except Exception as e:
        print(f"❌ 综合演示启动失败: {e}")

def run_performance_comparison():
    """运行性能对比"""
    print("🔄 启动性能对比分析...")
    try:
        from examples.comprehensive_demo import ComprehensiveDemo
        demo = ComprehensiveDemo()
        results = demo.demo_performance_comparison()
        
        print("\n📊 详细性能报告：")
        print("=" * 60)
        for technique, data in results.items():
            if "error" not in data:
                efficiency = data['word_count'] / data['execution_time']
                print(f"🔍 {technique}:")
                print(f"  ⏱️  执行时间: {data['execution_time']:.3f} 秒")
                print(f"  📝 输出字数: {data['word_count']} 字")
                print(f"  ⚡ 生成效率: {efficiency:.1f} 字/秒")
                print(f"  📄 内容预览: {data['result_preview']}")
                print("-" * 40)
        
    except Exception as e:
        print(f"❌ 性能对比启动失败: {e}")

def run_all_demos():
    """按序运行所有演示"""
    print("🔄 启动全部演示模块...")
    
    demos = [
        ("基础提示词工程", run_basic_demo),
        ("思维链技术", run_cot_demo),
        ("自我反思技术", run_reflection_demo),
        ("函数调用", run_function_calling_demo),
        ("文档生成器", run_document_generator_demo),
        ("提示词管理", run_prompt_manager_demo),
        ("提示词模板", run_template_demo),
        ("综合技术整合", run_comprehensive_demo),
        ("性能对比分析", run_performance_comparison)
    ]
    
    for name, demo_func in demos:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            demo_func()
            print(f"✅ {name}演示完成")
        except Exception as e:
            print(f"❌ {name}演示失败: {e}")
        
        input("\n⏸️  按Enter继续下一个演示...")

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查API密钥
    openai_key = os.getenv("OPENAI_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not openai_key and not deepseek_key:
        print("⚠️  警告：未检测到API密钥")
        print("💡 请设置以下环境变量之一：")
        print("   export OPENAI_API_KEY='your-openai-key'")
        print("   export DEEPSEEK_API_KEY='your-deepseek-key'")
        print("📝 或在 .env 文件中配置")
        return False
    
    if openai_key:
        print("✅ 检测到 OpenAI API 密钥")
    if deepseek_key:
        print("✅ 检测到 DeepSeek API 密钥")
    
    # 检查依赖包
    try:
        import openai
        import jinja2
        import yaml
        print("✅ 所有依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("💡 请运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return
    
    print("✅ 环境检查通过，系统准备就绪！")
    
    while True:
        print_menu()
        
        try:
            choice = input("\n🎯 请选择演示模块 (0-10): ").strip()
            
            if choice == "0":
                print("👋 感谢使用提示词工程演示系统！")
                break
            elif choice == "1":
                run_basic_demo()
            elif choice == "2":
                run_cot_demo()
            elif choice == "3":
                run_reflection_demo()
            elif choice == "4":
                run_function_calling_demo()
            elif choice == "5":
                run_document_generator_demo()
            elif choice == "6":
                run_prompt_manager_demo()
            elif choice == "7":
                run_template_demo()
            elif choice == "8":
                run_comprehensive_demo()
            elif choice == "9":
                run_performance_comparison()
            elif choice == "10":
                run_all_demos()
            else:
                print("❌ 无效选择，请输入 0-10 之间的数字")
            
            input("\n⏸️  按Enter返回主菜单...")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出系统")
            break
        except Exception as e:
            print(f"❌ 程序执行出错: {e}")
            input("⏸️  按Enter继续...")

if __name__ == "__main__":
    main() 