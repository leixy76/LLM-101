#!/usr/bin/env python3
"""
📋 提示词管理系统
提供提示词的创建、管理、版本控制、优化和评估功能
"""

import os
import json
import yaml
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class PromptTemplate:
    """提示词模板"""
    id: str
    name: str
    description: str
    template: str
    variables: List[str]
    category: str
    tags: List[str]
    version: str
    created_at: str
    updated_at: str
    author: str
    usage_count: int = 0
    avg_rating: float = 0.0

@dataclass
class PromptExecution:
    """提示词执行记录"""
    prompt_id: str
    version: str
    input_variables: Dict[str, Any]
    rendered_prompt: str
    model: str
    response: str
    execution_time: float
    tokens_used: int
    cost: float
    timestamp: str
    rating: Optional[int] = None
    feedback: Optional[str] = None

class PromptManager:
    """提示词管理器"""
    
    def __init__(self, storage_path: str = "prompts_storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        self.templates_file = self.storage_path / "templates.json"
        self.executions_file = self.storage_path / "executions.json"
        self.config_file = self.storage_path / "config.yaml"
        
        self.templates: Dict[str, PromptTemplate] = {}
        self.executions: List[PromptExecution] = []
        
        self.client = self.setup_client()
        self.load_data()
    
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
            print("⚠️ 未设置API密钥，某些功能可能无法使用")
            return None
    
    def load_data(self):
        """加载数据"""
        # 加载模板
        if self.templates_file.exists():
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                templates_data = json.load(f)
                self.templates = {
                    tid: PromptTemplate(**template_data)
                    for tid, template_data in templates_data.items()
                }
        
        # 加载执行记录
        if self.executions_file.exists():
            with open(self.executions_file, 'r', encoding='utf-8') as f:
                executions_data = json.load(f)
                self.executions = [
                    PromptExecution(**exec_data)
                    for exec_data in executions_data
                ]
    
    def save_data(self):
        """保存数据"""
        # 保存模板
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            templates_data = {
                tid: asdict(template)
                for tid, template in self.templates.items()
            }
            json.dump(templates_data, f, ensure_ascii=False, indent=2)
        
        # 保存执行记录
        with open(self.executions_file, 'w', encoding='utf-8') as f:
            executions_data = [asdict(execution) for execution in self.executions]
            json.dump(executions_data, f, ensure_ascii=False, indent=2)
    
    def create_template(self, name: str, description: str, template: str,
                       category: str = "general", tags: List[str] = None,
                       author: str = "unknown") -> str:
        """创建提示词模板"""
        # 生成唯一ID
        template_id = hashlib.md5(f"{name}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        # 提取变量
        variables = self.extract_variables(template)
        
        # 创建模板对象
        prompt_template = PromptTemplate(
            id=template_id,
            name=name,
            description=description,
            template=template,
            variables=variables,
            category=category,
            tags=tags or [],
            version="1.0.0",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            author=author
        )
        
        self.templates[template_id] = prompt_template
        self.save_data()
        
        return template_id
    
    def extract_variables(self, template: str) -> List[str]:
        """从模板中提取变量"""
        import re
        # 匹配 Jinja2 变量 {{ variable }}
        variables = re.findall(r'\{\{\s*(\w+)\s*\}\}', template)
        return list(set(variables))
    
    def update_template(self, template_id: str, **kwargs) -> bool:
        """更新模板"""
        if template_id not in self.templates:
            return False
        
        template = self.templates[template_id]
        
        # 如果模板内容改变，增加版本号
        if 'template' in kwargs and kwargs['template'] != template.template:
            version_parts = template.version.split('.')
            version_parts[-1] = str(int(version_parts[-1]) + 1)
            template.version = '.'.join(version_parts)
            template.variables = self.extract_variables(kwargs['template'])
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        template.updated_at = datetime.now().isoformat()
        self.save_data()
        
        return True
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """获取模板"""
        return self.templates.get(template_id)
    
    def list_templates(self, category: str = None, tags: List[str] = None) -> List[PromptTemplate]:
        """列出模板"""
        templates = list(self.templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        if tags:
            templates = [t for t in templates if any(tag in t.tags for tag in tags)]
        
        return sorted(templates, key=lambda x: x.updated_at, reverse=True)
    
    def render_template(self, template_id: str, variables: Dict[str, Any]) -> Optional[str]:
        """渲染模板"""
        template = self.get_template(template_id)
        if not template:
            return None
        
        try:
            jinja_template = Template(template.template)
            return jinja_template.render(**variables)
        except Exception as e:
            print(f"❌ 模板渲染失败: {e}")
            return None
    
    def execute_template(self, template_id: str, variables: Dict[str, Any],
                        model: str = "gpt-3.5-turbo", **llm_params) -> Optional[PromptExecution]:
        """执行模板"""
        if not self.client:
            print("❌ 未配置API客户端")
            return None
        
        template = self.get_template(template_id)
        if not template:
            return None
        
        # 渲染提示词
        rendered_prompt = self.render_template(template_id, variables)
        if not rendered_prompt:
            return None
        
        try:
            start_time = datetime.now()
            
            # 调用API
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": rendered_prompt}],
                **llm_params
            )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # 记录执行
            execution = PromptExecution(
                prompt_id=template_id,
                version=template.version,
                input_variables=variables,
                rendered_prompt=rendered_prompt,
                model=model,
                response=response.choices[0].message.content,
                execution_time=execution_time,
                tokens_used=response.usage.total_tokens,
                cost=self.calculate_cost(model, response.usage),
                timestamp=datetime.now().isoformat()
            )
            
            self.executions.append(execution)
            
            # 更新模板使用次数
            template.usage_count += 1
            self.save_data()
            
            return execution
            
        except Exception as e:
            print(f"❌ 模板执行失败: {e}")
            return None
    
    def calculate_cost(self, model: str, usage) -> float:
        """计算API调用成本"""
        # 简化的成本计算（实际价格可能不同）
        pricing = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},  # per 1K tokens
            "gpt-4": {"input": 0.03, "output": 0.06},
        }
        
        if model not in pricing:
            return 0.0
        
        input_cost = (usage.prompt_tokens / 1000) * pricing[model]["input"]
        output_cost = (usage.completion_tokens / 1000) * pricing[model]["output"]
        
        return input_cost + output_cost
    
    def rate_execution(self, execution_index: int, rating: int, feedback: str = ""):
        """为执行结果评分"""
        if 0 <= execution_index < len(self.executions):
            execution = self.executions[execution_index]
            execution.rating = rating
            execution.feedback = feedback
            
            # 更新模板平均评分
            template = self.get_template(execution.prompt_id)
            if template:
                rated_executions = [
                    e for e in self.executions 
                    if e.prompt_id == template.id and e.rating is not None
                ]
                if rated_executions:
                    template.avg_rating = sum(e.rating for e in rated_executions) / len(rated_executions)
            
            self.save_data()
    
    def analyze_template_performance(self, template_id: str) -> Dict[str, Any]:
        """分析模板性能"""
        template = self.get_template(template_id)
        if not template:
            return {}
        
        template_executions = [e for e in self.executions if e.prompt_id == template_id]
        
        if not template_executions:
            return {"message": "暂无执行记录"}
        
        # 基础统计
        total_executions = len(template_executions)
        total_cost = sum(e.cost for e in template_executions)
        avg_execution_time = sum(e.execution_time for e in template_executions) / total_executions
        total_tokens = sum(e.tokens_used for e in template_executions)
        
        # 评分统计
        rated_executions = [e for e in template_executions if e.rating is not None]
        avg_rating = sum(e.rating for e in rated_executions) / len(rated_executions) if rated_executions else None
        
        # 时间趋势
        executions_by_date = {}
        for execution in template_executions:
            date = execution.timestamp.split('T')[0]
            executions_by_date[date] = executions_by_date.get(date, 0) + 1
        
        return {
            "template_info": {
                "name": template.name,
                "version": template.version,
                "category": template.category
            },
            "usage_statistics": {
                "total_executions": total_executions,
                "total_cost": round(total_cost, 4),
                "avg_execution_time": round(avg_execution_time, 2),
                "total_tokens": total_tokens,
                "avg_tokens_per_execution": round(total_tokens / total_executions, 2)
            },
            "quality_metrics": {
                "avg_rating": round(avg_rating, 2) if avg_rating else None,
                "rated_executions": len(rated_executions),
                "rating_distribution": self.get_rating_distribution(rated_executions)
            },
            "usage_trend": executions_by_date
        }
    
    def get_rating_distribution(self, rated_executions: List[PromptExecution]) -> Dict[int, int]:
        """获取评分分布"""
        distribution = {i: 0 for i in range(1, 6)}
        for execution in rated_executions:
            if execution.rating in distribution:
                distribution[execution.rating] += 1
        return distribution
    
    def export_templates(self, filepath: str, template_ids: List[str] = None):
        """导出模板"""
        templates_to_export = {}
        
        if template_ids:
            for tid in template_ids:
                if tid in self.templates:
                    templates_to_export[tid] = asdict(self.templates[tid])
        else:
            templates_to_export = {tid: asdict(t) for tid, t in self.templates.items()}
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(templates_to_export, f, ensure_ascii=False, indent=2)
    
    def import_templates(self, filepath: str) -> int:
        """导入模板"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            imported_count = 0
            for template_data in imported_data.values():
                # 生成新的ID避免冲突
                original_id = template_data.get('id', '')
                new_id = self.create_template(
                    name=template_data['name'],
                    description=template_data['description'],
                    template=template_data['template'],
                    category=template_data.get('category', 'imported'),
                    tags=template_data.get('tags', []),
                    author=template_data.get('author', 'imported')
                )
                imported_count += 1
            
            return imported_count
            
        except Exception as e:
            print(f"❌ 导入失败: {e}")
            return 0

def demo_template_management():
    """模板管理演示"""
    print("📋 提示词模板管理演示")
    print("=" * 60)
    
    manager = PromptManager()
    
    # 创建示例模板
    template_id1 = manager.create_template(
        name="文本摘要",
        description="对长文本进行摘要",
        template="""请对以下文本进行摘要，要求：
1. 保留关键信息
2. 控制在{{ max_words }}字以内
3. 使用{{ style }}风格

文本内容：
{{ text }}

摘要：""",
        category="文本处理",
        tags=["摘要", "NLP"],
        author="示例用户"
    )
    
    template_id2 = manager.create_template(
        name="代码审查",
        description="审查代码质量和提供建议",
        template="""请审查以下{{ language }}代码，重点关注：
1. 代码质量和规范
2. 性能优化建议
3. 安全性问题
4. 可维护性

代码：
```{{ language }}
{{ code }}
```

审查报告：""",
        category="编程",
        tags=["代码审查", "质量"],
        author="示例用户"
    )
    
    print(f"✅ 创建了两个示例模板：{template_id1}, {template_id2}")
    
    # 列出模板
    templates = manager.list_templates()
    print(f"\n📋 当前模板列表 ({len(templates)}个)：")
    for template in templates:
        print(f"  - {template.name} ({template.id}) - {template.category}")
    
    return manager, template_id1, template_id2

def demo_template_execution():
    """模板执行演示"""
    print("\n🚀 模板执行演示")
    print("=" * 60)
    
    manager, template_id1, template_id2 = demo_template_management()
    
    if not manager.client:
        print("⚠️ 跳过执行演示（未配置API密钥）")
        return manager
    
    # 执行文本摘要模板
    text_sample = """
    人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，
    它试图理解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。
    """
    
    print("📝 执行文本摘要模板...")
    execution = manager.execute_template(
        template_id1,
        {
            "text": text_sample.strip(),
            "max_words": "50",
            "style": "专业"
        },
        temperature=0.3
    )
    
    if execution:
        print(f"✅ 执行成功！")
        print(f"⏱️ 执行时间: {execution.execution_time:.2f}秒")
        print(f"🎯 Token数: {execution.tokens_used}")
        print(f"💰 成本: ${execution.cost:.4f}")
        print(f"📤 结果: {execution.response}")
        
        # 为执行结果评分
        manager.rate_execution(len(manager.executions) - 1, 4, "摘要质量不错")
    
    return manager

def demo_performance_analysis():
    """性能分析演示"""
    print("\n📊 性能分析演示")
    print("=" * 60)
    
    manager = demo_template_execution()
    
    if manager.templates:
        template_id = list(manager.templates.keys())[0]
        analysis = manager.analyze_template_performance(template_id)
        
        print(f"📋 模板性能分析: {analysis.get('template_info', {}).get('name', 'Unknown')}")
        
        usage_stats = analysis.get('usage_statistics', {})
        print(f"📈 使用统计:")
        print(f"  - 总执行次数: {usage_stats.get('total_executions', 0)}")
        print(f"  - 总成本: ${usage_stats.get('total_cost', 0):.4f}")
        print(f"  - 平均执行时间: {usage_stats.get('avg_execution_time', 0):.2f}秒")
        
        quality_metrics = analysis.get('quality_metrics', {})
        print(f"⭐ 质量指标:")
        print(f"  - 平均评分: {quality_metrics.get('avg_rating', 'N/A')}")
        print(f"  - 已评分次数: {quality_metrics.get('rated_executions', 0)}")

def demo_import_export():
    """导入导出演示"""
    print("\n📦 导入导出演示")
    print("=" * 60)
    
    manager = PromptManager()
    
    if manager.templates:
        # 导出模板
        export_file = "exported_templates.json"
        manager.export_templates(export_file)
        print(f"✅ 已导出模板到: {export_file}")
        
        # 清空当前模板（仅演示）
        original_templates = manager.templates.copy()
        manager.templates.clear()
        
        # 导入模板
        imported_count = manager.import_templates(export_file)
        print(f"✅ 已导入 {imported_count} 个模板")
        
        # 恢复原始模板
        manager.templates = original_templates
        
        # 清理导出文件
        os.remove(export_file)
    else:
        print("ℹ️ 没有模板可供导出")

def main():
    """主函数"""
    print("📋 提示词管理系统演示")
    print("=" * 80)
    print("🎯 本演示展示如何管理、执行和优化提示词模板")
    print("=" * 80)
    
    try:
        demo_template_management()
        demo_template_execution()
        demo_performance_analysis()
        demo_import_export()
        
        print("\n" + "=" * 80)
        print("🎉 提示词管理系统演示完成！")
        print("💡 通过系统化管理，可以大大提升提示词的复用性和效果。")
        print("🚀 建议在实际项目中建立自己的提示词库。")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main() 