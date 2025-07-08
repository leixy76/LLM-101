#!/usr/bin/env python3
"""
📄 智能文档生成器
支持多种文档类型的自动生成，包括技术文档、商业计划、报告等
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from jinja2 import Template
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class DocumentTemplate:
    """文档模板"""
    name: str
    description: str
    sections: List[str]
    prompt_template: str
    output_format: str

class DocumentGenerator:
    """文档生成器"""
    
    def __init__(self):
        self.client = self.setup_client()
        self.model = "gpt-3.5-turbo"
        self.templates = self.load_templates()
    
    def setup_client(self):
        """设置API客户端"""
        if os.getenv("OPENAI_API_KEY"):
            return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif os.getenv("DEEPSEEK_API_KEY"):
            return OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
        else:
            raise ValueError("请设置OPENAI_API_KEY或DEEPSEEK_API_KEY环境变量")
    
    def load_templates(self) -> Dict[str, DocumentTemplate]:
        """加载文档模板"""
        templates = {}
        
        # 技术文档模板
        templates["technical_doc"] = DocumentTemplate(
            name="技术文档",
            description="生成技术文档，包括API文档、技术规范等",
            sections=["概述", "技术要求", "架构设计", "API接口", "部署说明", "常见问题"],
            prompt_template="""
你是一位资深的技术文档工程师。请根据以下信息生成专业的技术文档：

项目名称：{{ project_name }}
项目类型：{{ project_type }}
目标受众：{{ target_audience }}
技术栈：{{ tech_stack }}
特殊要求：{{ special_requirements }}

请生成包含以下结构的技术文档：
1. 项目概述
2. 技术要求和依赖
3. 系统架构设计
4. API接口文档
5. 部署和安装说明
6. 常见问题和故障排除

要求：
- 使用Markdown格式
- 内容准确、专业
- 包含代码示例（如适用）
- 结构清晰，易于阅读
""",
            output_format="markdown"
        )
        
        # 商业计划书模板
        templates["business_plan"] = DocumentTemplate(
            name="商业计划书",
            description="生成商业计划书，包括市场分析、财务预测等",
            sections=["执行摘要", "公司介绍", "市场分析", "产品服务", "营销策略", "财务预测"],
            prompt_template="""
你是一位资深的商业顾问。请根据以下信息生成专业的商业计划书：

公司名称：{{ company_name }}
业务类型：{{ business_type }}
目标市场：{{ target_market }}
产品/服务：{{ products_services }}
资金需求：{{ funding_needs }}
预期目标：{{ business_goals }}

请生成包含以下结构的商业计划书：
1. 执行摘要
2. 公司介绍和愿景
3. 市场分析和机会
4. 产品和服务描述
5. 营销和销售策略
6. 财务预测和资金需求
7. 风险分析和应对策略
8. 实施计划和里程碑

要求：
- 内容详实、逻辑清晰
- 数据支撑的分析
- 具体可执行的策略
- 专业的商业语言
""",
            output_format="structured"
        )
        
        # 项目报告模板
        templates["project_report"] = DocumentTemplate(
            name="项目报告",
            description="生成项目进度报告、总结报告等",
            sections=["项目概况", "进度汇报", "成果展示", "问题分析", "下步计划"],
            prompt_template="""
你是一位经验丰富的项目经理。请根据以下信息生成详细的项目报告：

项目名称：{{ project_name }}
报告类型：{{ report_type }}
报告周期：{{ report_period }}
项目状态：{{ project_status }}
关键成果：{{ key_achievements }}
主要问题：{{ main_issues }}
下步计划：{{ next_steps }}

请生成包含以下结构的项目报告：
1. 项目基本信息
2. 执行进度概览
3. 关键成果和里程碑
4. 问题识别和分析
5. 资源使用情况
6. 风险评估和应对
7. 下阶段工作计划
8. 建议和总结

要求：
- 数据准确、客观
- 分析深入、有见地
- 建议可行、具体
- 格式规范、易读
""",
            output_format="structured"
        )
        
        # 研究报告模板
        templates["research_report"] = DocumentTemplate(
            name="研究报告",
            description="生成市场研究、技术调研等报告",
            sections=["研究背景", "方法论", "数据分析", "发现结论", "建议"],
            prompt_template="""
你是一位专业的研究分析师。请根据以下信息生成深入的研究报告：

研究主题：{{ research_topic }}
研究目的：{{ research_purpose }}
研究范围：{{ research_scope }}
数据来源：{{ data_sources }}
关键发现：{{ key_findings }}
目标读者：{{ target_readers }}

请生成包含以下结构的研究报告：
1. 研究背景和目标
2. 研究方法和数据来源
3. 市场/技术现状分析
4. 关键数据和趋势分析
5. 深入发现和洞察
6. 结论和预测
7. 建议和行动方案
8. 附录和参考资料

要求：
- 分析客观、数据支撑
- 逻辑严密、结构清晰
- 洞察深入、有价值
- 建议实用、可操作
""",
            output_format="academic"
        )
        
        return templates
    
    def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """调用大模型"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ 生成失败: {str(e)}"
    
    def generate_document(self, template_name: str, variables: Dict[str, Any],
                         custom_requirements: str = "") -> str:
        """生成文档"""
        if template_name not in self.templates:
            return f"❌ 未知模板: {template_name}"
        
        template = self.templates[template_name]
        
        # 渲染提示词
        jinja_template = Template(template.prompt_template)
        rendered_prompt = jinja_template.render(**variables)
        
        # 添加自定义要求
        if custom_requirements:
            rendered_prompt += f"\n\n额外要求：\n{custom_requirements}"
        
        # 调用LLM生成文档
        messages = [
            {"role": "system", "content": f"你是一位专业的{template.name}撰写专家。"},
            {"role": "user", "content": rendered_prompt}
        ]
        
        return self.call_llm(messages, temperature=0.3)
    
    def generate_section(self, template_name: str, section_name: str,
                        variables: Dict[str, Any], context: str = "") -> str:
        """生成文档的特定章节"""
        if template_name not in self.templates:
            return f"❌ 未知模板: {template_name}"
        
        template = self.templates[template_name]
        
        section_prompt = f"""
请为《{variables.get('project_name', '项目')}》生成「{section_name}」章节的内容。

背景信息：
{json.dumps(variables, ensure_ascii=False, indent=2)}

{f"上下文信息：{context}" if context else ""}

要求：
1. 内容与{section_name}主题高度相关
2. 风格与{template.name}一致
3. 内容详实、专业
4. 结构清晰、逻辑性强

请生成该章节的详细内容：
"""
        
        messages = [
            {"role": "system", "content": f"你是{template.name}的专业撰写者，专注于{section_name}部分的内容创作。"},
            {"role": "user", "content": section_prompt}
        ]
        
        return self.call_llm(messages, temperature=0.4)
    
    def optimize_document(self, original_doc: str, optimization_type: str = "clarity") -> str:
        """优化文档质量"""
        optimization_prompts = {
            "clarity": "请优化以下文档的表达清晰度，使其更易理解：",
            "conciseness": "请精简以下文档，去除冗余内容，保持核心信息：",
            "professionalism": "请提升以下文档的专业性，使用更专业的术语和表达：",
            "structure": "请优化以下文档的结构和组织，使其更有逻辑性：",
            "completeness": "请检查以下文档的完整性，补充可能缺失的重要信息："
        }
        
        if optimization_type not in optimization_prompts:
            return "❌ 未知优化类型"
        
        prompt = f"""
{optimization_prompts[optimization_type]}

原文档：
{original_doc}

优化后的文档：
"""
        
        messages = [
            {"role": "system", "content": "你是一位专业的文档编辑和优化专家。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages, temperature=0.3)
    
    def translate_document(self, document: str, target_language: str = "English") -> str:
        """翻译文档"""
        prompt = f"""
请将以下文档翻译成{target_language}，保持原有的格式和结构：

原文档：
{document}

翻译后的文档：
"""
        
        messages = [
            {"role": "system", "content": f"你是一位专业的{target_language}翻译专家，擅长文档翻译。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages, temperature=0.2)
    
    def create_outline(self, document_type: str, topic: str, requirements: str = "") -> str:
        """创建文档大纲"""
        prompt = f"""
请为以下主题创建详细的{document_type}大纲：

主题：{topic}
{f"特殊要求：{requirements}" if requirements else ""}

请提供：
1. 完整的章节结构
2. 每个章节的主要内容点
3. 预估的篇幅分配
4. 关键信息来源建议

大纲：
"""
        
        messages = [
            {"role": "system", "content": f"你是一位经验丰富的{document_type}大纲设计专家。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages, temperature=0.4)

def demo_technical_documentation():
    """技术文档生成演示"""
    print("📄 技术文档生成演示")
    print("=" * 60)
    
    generator = DocumentGenerator()
    
    # 生成技术文档
    variables = {
        "project_name": "AI智能客服系统",
        "project_type": "Web应用",
        "target_audience": "开发者和系统管理员",
        "tech_stack": "Python, FastAPI, PostgreSQL, Redis, Docker",
        "special_requirements": "需要支持多语言和高并发"
    }
    
    print(f"📝 生成项目: {variables['project_name']}")
    print("🔄 正在生成技术文档...")
    
    doc = generator.generate_document("technical_doc", variables)
    
    print("✅ 技术文档生成完成！")
    print("📄 文档内容预览:")
    print("-" * 40)
    print(doc[:800] + "..." if len(doc) > 800 else doc)
    
    return generator

def demo_business_plan():
    """商业计划书生成演示"""
    print("\n💼 商业计划书生成演示")
    print("=" * 60)
    
    generator = DocumentGenerator()
    
    variables = {
        "company_name": "智慧生活科技有限公司",
        "business_type": "智能家居解决方案",
        "target_market": "中高端家庭用户",
        "products_services": "智能家居控制系统、IoT设备、移动应用",
        "funding_needs": "500万人民币A轮融资",
        "business_goals": "3年内成为地区领先的智能家居品牌"
    }
    
    print(f"🏢 公司: {variables['company_name']}")
    print("🔄 正在生成商业计划书...")
    
    doc = generator.generate_document("business_plan", variables)
    
    print("✅ 商业计划书生成完成！")
    print("📄 文档内容预览:")
    print("-" * 40)
    print(doc[:800] + "..." if len(doc) > 800 else doc)

def demo_section_generation():
    """章节生成演示"""
    print("\n📋 章节生成演示")
    print("=" * 60)
    
    generator = DocumentGenerator()
    
    variables = {
        "project_name": "区块链投票系统",
        "project_type": "分布式应用",
        "target_audience": "政府机构和企业"
    }
    
    print(f"📝 项目: {variables['project_name']}")
    print("🔄 正在生成「系统架构设计」章节...")
    
    section = generator.generate_section(
        "technical_doc", 
        "系统架构设计", 
        variables,
        "这是一个基于以太坊的去中心化投票系统"
    )
    
    print("✅ 章节生成完成！")
    print("📄 章节内容:")
    print("-" * 40)
    print(section)

def demo_document_optimization():
    """文档优化演示"""
    print("\n✨ 文档优化演示")
    print("=" * 60)
    
    generator = DocumentGenerator()
    
    # 模拟一个需要优化的文档片段
    original_doc = """
我们的产品是一个非常好的东西，它可以做很多很多的功能。
用户可以使用它来完成各种各样的任务，非常方便。
它有很多优点，比如快速、稳定、好用等等。
我们觉得这个产品会很受欢迎，因为它真的很棒。
"""
    
    print("📝 原始文档:")
    print(original_doc)
    
    print("\n🔄 正在优化文档专业性...")
    optimized = generator.optimize_document(original_doc, "professionalism")
    
    print("✅ 优化完成！")
    print("📄 优化后文档:")
    print("-" * 40)
    print(optimized)

def demo_outline_creation():
    """大纲创建演示"""
    print("\n📋 文档大纲创建演示")
    print("=" * 60)
    
    generator = DocumentGenerator()
    
    print("🔄 正在创建「人工智能在医疗领域的应用」研究报告大纲...")
    
    outline = generator.create_outline(
        "研究报告",
        "人工智能在医疗领域的应用",
        "重点关注诊断、治疗和药物研发三个方面"
    )
    
    print("✅ 大纲创建完成！")
    print("📋 报告大纲:")
    print("-" * 40)
    print(outline)

def main():
    """主函数"""
    print("📄 智能文档生成器演示")
    print("=" * 80)
    print("🎯 本演示展示如何使用AI自动生成各种类型的专业文档")
    print("=" * 80)
    
    try:
        demo_technical_documentation()
        demo_business_plan()
        demo_section_generation()
        demo_document_optimization()
        demo_outline_creation()
        
        print("\n" + "=" * 80)
        print("🎉 文档生成器演示完成！")
        print("💡 AI可以显著提升文档创作的效率和质量。")
        print("🚀 结合模板化和个性化，能满足各种文档需求。")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main() 