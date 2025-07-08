#!/usr/bin/env python3
"""
🚀 提示词工程综合演示
整合展示所有提示词技术：基础技巧、高级技术、函数调用、内容生成等
"""

import os
import sys
import time
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 导入所有演示模块
from prompt_engineering_demo import PromptEngineeringDemo
from advanced_prompting.chain_of_thought import ChainOfThoughtEngine
from advanced_prompting.self_reflection import SelfReflectionEngine
from function_calling.basic_function_calling import FunctionCallingEngine
from content_generation.document_generator import DocumentGenerator
from prompt_management.prompt_manager import PromptManager

class ComprehensiveDemo:
    """提示词工程综合演示类"""
    
    def __init__(self):
        print("🚀 初始化提示词工程综合演示系统...")
        
        try:
            self.basic_demo = PromptEngineeringDemo()
            self.cot_engine = ChainOfThoughtEngine()
            self.reflection_engine = SelfReflectionEngine()
            self.function_engine = FunctionCallingEngine()
            self.doc_generator = DocumentGenerator()
            self.prompt_manager = PromptManager()
            
            print("✅ 所有模块初始化完成！")
            
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            print("💡 请确保已正确配置API密钥")
            raise
    
    def demo_progressive_optimization(self):
        """渐进式优化演示"""
        print("\n🎯 渐进式提示词优化演示")
        print("=" * 60)
        print("📋 场景：为新产品撰写营销文案")
        
        product_info = "智能语音助手音箱，支持语音控制家电，播放音乐，回答问题"
        
        # 第1步：零样本基础版本
        print("\n📝 第1步：零样本基础版本")
        print("-" * 30)
        basic_result = self.basic_demo.zero_shot_example(
            f"为以下产品写一段营销文案：{product_info}"
        )
        print("结果：", basic_result[:200] + "..." if len(basic_result) > 200 else basic_result)
        
        # 第2步：思维链优化
        print("\n🧠 第2步：思维链分析优化")
        print("-" * 30)
        cot_result = self.cot_engine.multi_step_reasoning(
            f"为智能语音助手音箱创作营销文案：{product_info}",
            [
                "分析目标客户群体和需求痛点",
                "提取产品的核心卖点和差异化优势", 
                "设计情感化的表达方式",
                "加入行动号召和购买理由",
                "检查文案的吸引力和说服力"
            ]
        )
        print("结果：", cot_result[:300] + "..." if len(cot_result) > 300 else cot_result)
        
        # 第3步：自我反思改进
        print("\n🔄 第3步：自我反思改进")
        print("-" * 30)
        reflection_results = self.reflection_engine.multi_round_reflection(
            f"请为智能语音助手音箱撰写具有强烈购买欲望的营销文案，产品特点：{product_info}",
            "营销文案"
        )
        
        if reflection_results:
            final_result = reflection_results[-1].improved_answer
            print(f"最终文案（置信度: {reflection_results[-1].confidence_score:.2f}）：")
            print(final_result[:300] + "..." if len(final_result) > 300 else final_result)
        
        return final_result if reflection_results else cot_result
    
    def demo_function_enhanced_analysis(self):
        """函数增强分析演示"""
        print("\n🔧 函数增强分析演示")
        print("=" * 60)
        print("📋 场景：智能数据分析助手")
        
        # 使用函数调用进行复合分析
        analysis_query = """
        我有一段客户反馈："这个产品功能很棒，但是价格有点贵，界面也不够直观"
        
        请帮我：
        1. 分析这段话的情感倾向
        2. 统计字数
        3. 如果按每分钟200字的阅读速度，需要多长时间读完？
        """
        
        print("🤖 AI助手分析过程：")
        result = self.function_engine.chat_with_functions(analysis_query)
        print(f"\n📊 综合分析结果：\n{result}")
    
    def demo_template_driven_generation(self):
        """模板驱动生成演示"""
        print("\n📋 模板驱动内容生成演示")  
        print("=" * 60)
        print("📋 场景：快速生成技术文档")
        
        # 创建技术文档模板
        template_id = self.prompt_manager.create_template(
            name="API接口文档",
            description="生成标准的API接口文档",
            template="""
请为{{ api_name }}接口生成详细的API文档：

【接口基本信息】
接口名称：{{ api_name }}
请求方法：{{ method }}
接口路径：{{ endpoint }}
功能描述：{{ description }}

【请求参数】
{{ parameters }}

【响应格式】
{{ response_format }}

请生成包含以下部分的完整API文档：
1. 接口概述
2. 请求参数详细说明
3. 响应数据结构
4. 错误码说明
5. 请求示例
6. 响应示例

要求：格式标准、信息完整、示例清晰
""",
            category="技术文档",
            tags=["API", "文档"],
            author="演示用户"
        )
        
        print(f"✅ 创建模板ID: {template_id}")
        
        # 使用模板生成文档
        variables = {
            "api_name": "用户登录",
            "method": "POST", 
            "endpoint": "/api/v1/auth/login",
            "description": "用户登录认证接口",
            "parameters": "username (string): 用户名\npassword (string): 密码",
            "response_format": "JSON格式，包含token和用户信息"
        }
        
        if self.prompt_manager.client:
            print("🔄 正在生成API文档...")
            execution = self.prompt_manager.execute_template(template_id, variables)
            
            if execution:
                print("✅ 文档生成完成！")
                print(f"⏱️ 执行时间: {execution.execution_time:.2f}秒")
                print(f"📄 生成文档：\n{execution.response[:500]}...")
        else:
            print("⚠️ 跳过模板执行（未配置API密钥）")
    
    def demo_multi_modal_content_creation(self):
        """多模态内容创作演示"""
        print("\n🎨 多模态内容创作演示")
        print("=" * 60)
        print("📋 场景：为产品发布会创建全套内容")
        
        product_launch = {
            "product_name": "星际VR头盔",
            "key_features": "4K分辨率、无延迟追踪、轻量化设计",
            "target_audience": "游戏爱好者和科技早期用户",
            "launch_date": "2024年6月"
        }
        
        print(f"🎯 产品：{product_launch['product_name']}")
        
        # 1. 生成新闻稿
        print("\n📰 生成新闻稿...")
        press_release = self.doc_generator.generate_document(
            "technical_doc",
            {
                "project_name": product_launch["product_name"],
                "project_type": "VR设备",
                "target_audience": "媒体和消费者",
                "tech_stack": "VR技术、4K显示、动作追踪",
                "special_requirements": "突出创新性和用户体验"
            },
            "重点说明产品的技术突破和市场意义"
        )
        print("✅ 新闻稿生成完成")
        print("📄 内容预览：", press_release[:200] + "...")
        
        # 2. 生成社交媒体内容
        print("\n📱 生成社交媒体内容...")
        social_content = self.basic_demo.role_playing_example(
            f"为{product_launch['product_name']}发布会创建微博内容，特点：{product_launch['key_features']}"
        )
        print("✅ 社交媒体内容生成完成")
        print("📱 微博文案：", social_content[:150] + "...")
        
        # 3. 生成产品说明书大纲
        print("\n📋 生成产品说明书大纲...")
        manual_outline = self.doc_generator.create_outline(
            "产品说明书",
            f"{product_launch['product_name']}用户手册",
            "包含安装、使用、故障排除等内容"
        )
        print("✅ 说明书大纲生成完成")
        print("📋 大纲预览：", manual_outline[:200] + "...")
    
    def demo_performance_comparison(self):
        """性能对比演示"""
        print("\n📊 提示词技术性能对比演示")
        print("=" * 60)
        
        test_question = "如何提高团队的工作效率？"
        
        techniques = [
            ("零样本", lambda: self.basic_demo.zero_shot_example(test_question)),
            ("少样本", lambda: self.basic_demo.few_shot_example(test_question)),
            ("思维链", lambda: self.cot_engine.zero_shot_cot(test_question)),
            ("自我反思", lambda: self.reflection_engine.initial_answer(test_question))
        ]
        
        results = {}
        
        print(f"📝 测试问题：{test_question}")
        print("\n🔄 开始性能测试...")
        
        for name, method in techniques:
            try:
                start_time = time.time()
                result = method()
                end_time = time.time()
                
                execution_time = end_time - start_time
                word_count = len(result)
                
                results[name] = {
                    "execution_time": execution_time,
                    "word_count": word_count,
                    "result_preview": result[:100] + "..." if len(result) > 100 else result
                }
                
                print(f"  ✅ {name}: {execution_time:.2f}秒, {word_count}字")
                
            except Exception as e:
                print(f"  ❌ {name}: 执行失败 - {e}")
                results[name] = {"error": str(e)}
        
        # 显示对比结果
        print("\n📊 性能对比总结：")
        print("-" * 60)
        for name, data in results.items():
            if "error" not in data:
                print(f"{name:8} | 耗时: {data['execution_time']:6.2f}s | 字数: {data['word_count']:4d} | 效率: {data['word_count']/data['execution_time']:6.1f}字/秒")
        
        return results
    
    def demo_interactive_optimization(self):
        """交互式优化演示"""
        print("\n💬 交互式提示词优化演示")
        print("=" * 60)
        print("🎯 场景：根据用户反馈持续优化提示词")
        
        original_prompt = "请写一个关于人工智能的文章"
        
        print(f"📝 原始提示词：{original_prompt}")
        
        # 模拟优化过程
        optimizations = [
            {
                "feedback": "内容太宽泛，需要更具体的主题",
                "improved_prompt": "请写一篇关于人工智能在医疗诊断中应用的技术文章"
            },
            {
                "feedback": "需要指定目标读者和文章长度",
                "improved_prompt": "请为医疗专业人员写一篇800字的技术文章，介绍人工智能在医疗诊断中的具体应用案例和技术原理"
            },
            {
                "feedback": "希望包含实际案例和数据支撑",
                "improved_prompt": "请为医疗专业人员写一篇800字的技术文章，介绍人工智能在医疗诊断中的应用。要求：1)包含至少2个真实案例 2)引用相关数据和研究 3)分析技术优势和局限性 4)使用专业但易懂的语言"
            }
        ]
        
        current_prompt = original_prompt
        
        for i, opt in enumerate(optimizations, 1):
            print(f"\n🔄 第{i}轮优化：")
            print(f"💬 用户反馈：{opt['feedback']}")
            print(f"✨ 优化后：{opt['improved_prompt']}")
            
            # 使用自我反思评估改进
            analysis = self.reflection_engine.reflect_on_answer(
                "评估这个提示词的质量",
                opt['improved_prompt']
            )
            
            print(f"🔍 质量分析：{analysis[:150]}...")
            current_prompt = opt['improved_prompt']
        
        print(f"\n🎉 最终优化版本：\n{current_prompt}")

def main():
    """主演示函数"""
    print("🚀 提示词工程综合演示系统")
    print("=" * 80)
    print("🎯 本演示整合展示所有提示词工程技术和最佳实践")
    print("💡 包含：基础技巧、高级技术、函数调用、内容生成、管理优化")
    print("=" * 80)
    
    try:
        demo = ComprehensiveDemo()
        
        print("\n🎭 演示内容清单：")
        print("1. 渐进式提示词优化")
        print("2. 函数增强分析")
        print("3. 模板驱动生成")
        print("4. 多模态内容创作")
        print("5. 性能对比分析")
        print("6. 交互式优化")
        
        demos = [
            ("渐进式优化", demo.demo_progressive_optimization),
            ("函数增强分析", demo.demo_function_enhanced_analysis),
            ("模板驱动生成", demo.demo_template_driven_generation),
            ("多模态内容创作", demo.demo_multi_modal_content_creation),
            ("性能对比", demo.demo_performance_comparison),
            ("交互式优化", demo.demo_interactive_optimization)
        ]
        
        for name, demo_func in demos:
            try:
                demo_func()
                print(f"\n✅ {name}演示完成")
                time.sleep(1)  # 短暂停顿，便于观察
                
            except Exception as e:
                print(f"\n❌ {name}演示失败: {e}")
                continue
        
        print("\n" + "=" * 80)
        print("🎉 提示词工程综合演示完成！")
        print("📈 关键收获：")
        print("  • 渐进式优化能显著提升提示词质量")
        print("  • 函数调用扩展了AI的能力边界") 
        print("  • 模板化管理提高了复用效率")
        print("  • 多轮反思能够持续改进输出")
        print("  • 不同技术适用于不同场景需求")
        print("\n🚀 建议接下来：")
        print("  • 在实际项目中应用这些技术")
        print("  • 建立自己的提示词库")
        print("  • 持续优化和迭代提示词")
        print("  • 结合业务场景设计专用模板")
        
    except Exception as e:
        print(f"❌ 综合演示启动失败: {e}")
        print("💡 请检查环境配置和API密钥设置")

if __name__ == "__main__":
    main() 