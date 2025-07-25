"""
提示词模板管理系统
Prompt template management system
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .models import ChatMessage

logger = logging.getLogger(__name__)


class PromptType(Enum):
    """提示词类型枚举"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    CHAT = "chat"
    COMPLETION = "completion"


@dataclass
class PromptTemplate:
    """提示词模板类"""
    name: str
    type: PromptType
    template: str
    description: Optional[str] = None
    variables: Optional[List[str]] = None
    examples: Optional[List[Dict[str, Any]]] = None
    
    def format(self, **kwargs) -> str:
        """格式化模板"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"模板变量缺失: {e}")
        except Exception as e:
            raise ValueError(f"模板格式化失败: {e}")
    
    def validate_variables(self, **kwargs) -> bool:
        """验证模板变量"""
        if not self.variables:
            return True
        
        missing_vars = set(self.variables) - set(kwargs.keys())
        if missing_vars:
            logger.warning(f"缺失模板变量: {missing_vars}")
            return False
        
        return True


class PromptManager:
    """提示词管理器"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()
        
        if self.templates_dir and self.templates_dir.exists():
            self._load_templates_from_dir()
    
    def _load_default_templates(self):
        """加载默认模板"""
        
        # Qwen模型聊天模板
        qwen_chat_template = PromptTemplate(
            name="qwen_chat",
            type=PromptType.CHAT,
            template="""<|im_start|>system
{system_message}<|im_end|>
{conversation}<|im_start|>assistant
""",
            description="Qwen模型聊天格式模板",
            variables=["system_message", "conversation"]
        )
        
        # 通用系统提示词
        system_template = PromptTemplate(
            name="travel_system",
            type=PromptType.SYSTEM,
            template="""你是一个专业的AI旅行规划助手。你的任务是帮助用户制定详细、实用的旅行计划。

请遵循以下原则：
1. 提供准确、最新的旅行信息
2. 考虑用户的预算、时间和偏好
3. 推荐当地特色景点、美食和文化体验
4. 提供实用的交通、住宿和安全建议
5. 保持友好、专业的服务态度

请用中文回答，并确保信息的准确性和实用性。""",
            description="旅行规划系统提示词"
        )
        
        # 旅行规划模板
        travel_planning_template = PromptTemplate(
            name="travel_planning",
            type=PromptType.USER,
            template="""请为我制定一个{destination}的{duration}旅行计划。

旅行信息：
- 目的地: {destination}
- 旅行时长: {duration}
- 预算范围: {budget}
- 旅行人数: {travelers}
- 兴趣偏好: {interests}
- 特殊要求: {special_requirements}

请提供详细的行程安排，包括：
1. 每日行程规划
2. 推荐景点和活动
3. 住宿建议
4. 交通方案
5. 美食推荐
6. 预算分配
7. 注意事项""",
            description="旅行规划请求模板",
            variables=["destination", "duration", "budget", "travelers", "interests", "special_requirements"]
        )
        
        # 景点推荐模板
        attraction_template = PromptTemplate(
            name="attraction_recommendation",
            type=PromptType.USER,
            template="""请推荐{destination}的{attraction_type}景点。

要求：
- 景点类型: {attraction_type}
- 推荐数量: {count}个
- 适合人群: {target_audience}
- 预算考虑: {budget_level}

请为每个景点提供：
1. 景点名称和简介
2. 开放时间和门票价格
3. 交通方式
4. 游览建议
5. 周边配套设施""",
            description="景点推荐模板",
            variables=["destination", "attraction_type", "count", "target_audience", "budget_level"]
        )
        
        # 美食推荐模板
        food_template = PromptTemplate(
            name="food_recommendation",
            type=PromptType.USER,
            template="""请推荐{destination}的特色美食和餐厅。

偏好信息：
- 菜系偏好: {cuisine_preference}
- 价位要求: {price_range}
- 用餐场景: {dining_scene}
- 特殊需求: {dietary_restrictions}

请推荐：
1. 当地特色菜品
2. 推荐餐厅（包括地址和价位）
3. 街头小食
4. 用餐礼仪和注意事项""",
            description="美食推荐模板",
            variables=["destination", "cuisine_preference", "price_range", "dining_scene", "dietary_restrictions"]
        )
        
        # 注册默认模板
        templates = [
            qwen_chat_template,
            system_template,
            travel_planning_template,
            attraction_template,
            food_template
        ]
        
        for template in templates:
            self.templates[template.name] = template
        
        logger.info(f"加载了 {len(templates)} 个默认模板")
    
    def _load_templates_from_dir(self):
        """从目录加载模板"""
        try:
            for template_file in self.templates_dir.glob("*.json"):
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                template = PromptTemplate(
                    name=template_data["name"],
                    type=PromptType(template_data["type"]),
                    template=template_data["template"],
                    description=template_data.get("description"),
                    variables=template_data.get("variables"),
                    examples=template_data.get("examples")
                )
                
                self.templates[template.name] = template
                logger.info(f"加载模板: {template.name}")
                
        except Exception as e:
            logger.error(f"加载模板文件失败: {e}")
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """获取模板"""
        return self.templates.get(name)
    
    def list_templates(self) -> List[str]:
        """列出所有模板名称"""
        return list(self.templates.keys())
    
    def add_template(self, template: PromptTemplate):
        """添加模板"""
        self.templates[template.name] = template
        logger.info(f"添加模板: {template.name}")
    
    def remove_template(self, name: str) -> bool:
        """删除模板"""
        if name in self.templates:
            del self.templates[name]
            logger.info(f"删除模板: {name}")
            return True
        return False
    
    def format_template(self, name: str, **kwargs) -> str:
        """格式化模板"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"模板不存在: {name}")
        
        if not template.validate_variables(**kwargs):
            raise ValueError(f"模板变量验证失败: {name}")
        
        return template.format(**kwargs)
    
    def format_chat_prompt(self, messages: List[ChatMessage]) -> str:
        """格式化聊天提示词"""
        try:
            # 分离系统消息和对话消息
            system_message = ""
            conversation_parts = []
            
            for message in messages:
                if message.role == "system":
                    system_message = message.content
                elif message.role == "user":
                    conversation_parts.append(f"<|im_start|>user\n{message.content}<|im_end|>")
                elif message.role == "assistant":
                    conversation_parts.append(f"<|im_start|>assistant\n{message.content}<|im_end|>")
            
            # 如果没有系统消息，使用默认的
            if not system_message:
                system_template = self.get_template("travel_system")
                if system_template:
                    system_message = system_template.template
                else:
                    system_message = "你是一个有用的AI助手。"
            
            # 构建完整对话
            conversation = "\n".join(conversation_parts)
            
            # 使用Qwen聊天模板
            qwen_template = self.get_template("qwen_chat")
            if qwen_template:
                return qwen_template.format(
                    system_message=system_message,
                    conversation=conversation
                )
            else:
                # 回退到简单格式
                return f"System: {system_message}\n\n{conversation}\n\nAssistant:"
                
        except Exception as e:
            logger.error(f"格式化聊天提示词失败: {e}")
            # 回退到简单拼接
            return "\n".join([f"{msg.role}: {msg.content}" for msg in messages]) + "\nassistant:"
    
    def create_travel_planning_prompt(
        self,
        destination: str,
        duration: str,
        budget: str = "中等",
        travelers: str = "2人",
        interests: str = "观光、美食",
        special_requirements: str = "无"
    ) -> str:
        """创建旅行规划提示词"""
        return self.format_template(
            "travel_planning",
            destination=destination,
            duration=duration,
            budget=budget,
            travelers=travelers,
            interests=interests,
            special_requirements=special_requirements
        )
    
    def create_attraction_prompt(
        self,
        destination: str,
        attraction_type: str = "热门景点",
        count: int = 5,
        target_audience: str = "一般游客",
        budget_level: str = "中等"
    ) -> str:
        """创建景点推荐提示词"""
        return self.format_template(
            "attraction_recommendation",
            destination=destination,
            attraction_type=attraction_type,
            count=str(count),
            target_audience=target_audience,
            budget_level=budget_level
        )
    
    def create_food_prompt(
        self,
        destination: str,
        cuisine_preference: str = "当地特色",
        price_range: str = "中等价位",
        dining_scene: str = "正餐",
        dietary_restrictions: str = "无"
    ) -> str:
        """创建美食推荐提示词"""
        return self.format_template(
            "food_recommendation",
            destination=destination,
            cuisine_preference=cuisine_preference,
            price_range=price_range,
            dining_scene=dining_scene,
            dietary_restrictions=dietary_restrictions
        )
    
    def save_template_to_file(self, template_name: str, file_path: str):
        """保存模板到文件"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"模板不存在: {template_name}")
        
        template_data = {
            "name": template.name,
            "type": template.type.value,
            "template": template.template,
            "description": template.description,
            "variables": template.variables,
            "examples": template.examples
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"模板已保存到文件: {file_path}")
    
    def export_all_templates(self, export_dir: str):
        """导出所有模板"""
        export_path = Path(export_dir)
        export_path.mkdir(parents=True, exist_ok=True)
        
        for name, template in self.templates.items():
            file_path = export_path / f"{name}.json"
            self.save_template_to_file(name, str(file_path))
        
        logger.info(f"所有模板已导出到: {export_dir}")


# 全局提示词管理器实例
_global_prompt_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    """获取全局提示词管理器"""
    global _global_prompt_manager
    
    if _global_prompt_manager is None:
        _global_prompt_manager = PromptManager()
    
    return _global_prompt_manager