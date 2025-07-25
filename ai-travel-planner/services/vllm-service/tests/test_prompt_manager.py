"""
提示词管理器测试
Prompt manager tests
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from ..prompt_manager import (
    PromptTemplate, 
    PromptType, 
    PromptManager, 
    get_prompt_manager
)
from ..models import ChatMessage


class TestPromptTemplate:
    """提示词模板测试类"""
    
    def test_template_creation(self):
        """测试模板创建"""
        template = PromptTemplate(
            name="test_template",
            type=PromptType.USER,
            template="Hello {name}, welcome to {place}!",
            description="测试模板",
            variables=["name", "place"]
        )
        
        assert template.name == "test_template"
        assert template.type == PromptType.USER
        assert template.template == "Hello {name}, welcome to {place}!"
        assert template.description == "测试模板"
        assert template.variables == ["name", "place"]
    
    def test_template_format_success(self):
        """测试模板格式化成功"""
        template = PromptTemplate(
            name="test",
            type=PromptType.USER,
            template="Hello {name}!",
            variables=["name"]
        )
        
        result = template.format(name="Alice")
        assert result == "Hello Alice!"
    
    def test_template_format_missing_variable(self):
        """测试模板格式化缺少变量"""
        template = PromptTemplate(
            name="test",
            type=PromptType.USER,
            template="Hello {name}!",
            variables=["name"]
        )
        
        with pytest.raises(ValueError, match="模板变量缺失"):
            template.format()
    
    def test_validate_variables_success(self):
        """测试变量验证成功"""
        template = PromptTemplate(
            name="test",
            type=PromptType.USER,
            template="Hello {name}!",
            variables=["name"]
        )
        
        assert template.validate_variables(name="Alice") is True
    
    def test_validate_variables_missing(self):
        """测试变量验证失败"""
        template = PromptTemplate(
            name="test",
            type=PromptType.USER,
            template="Hello {name}!",
            variables=["name"]
        )
        
        assert template.validate_variables() is False
    
    def test_validate_variables_no_requirements(self):
        """测试无变量要求的验证"""
        template = PromptTemplate(
            name="test",
            type=PromptType.USER,
            template="Hello world!",
            variables=None
        )
        
        assert template.validate_variables() is True


class TestPromptManager:
    """提示词管理器测试类"""
    
    @pytest.fixture
    def manager(self):
        """管理器fixture"""
        return PromptManager()
    
    def test_manager_initialization(self, manager):
        """测试管理器初始化"""
        assert isinstance(manager.templates, dict)
        assert len(manager.templates) > 0  # 应该有默认模板
        
        # 检查默认模板
        assert "qwen_chat" in manager.templates
        assert "travel_system" in manager.templates
        assert "travel_planning" in manager.templates
    
    def test_get_template_exists(self, manager):
        """测试获取存在的模板"""
        template = manager.get_template("travel_system")
        assert template is not None
        assert isinstance(template, PromptTemplate)
        assert template.name == "travel_system"
    
    def test_get_template_not_exists(self, manager):
        """测试获取不存在的模板"""
        template = manager.get_template("nonexistent")
        assert template is None
    
    def test_list_templates(self, manager):
        """测试列出模板"""
        templates = manager.list_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "travel_system" in templates
    
    def test_add_template(self, manager):
        """测试添加模板"""
        new_template = PromptTemplate(
            name="custom_template",
            type=PromptType.USER,
            template="Custom template: {content}",
            variables=["content"]
        )
        
        manager.add_template(new_template)
        
        retrieved = manager.get_template("custom_template")
        assert retrieved is not None
        assert retrieved.name == "custom_template"
    
    def test_remove_template(self, manager):
        """测试删除模板"""
        # 先添加一个模板
        template = PromptTemplate(
            name="temp_template",
            type=PromptType.USER,
            template="Temporary"
        )
        manager.add_template(template)
        
        # 删除模板
        result = manager.remove_template("temp_template")
        assert result is True
        
        # 验证已删除
        assert manager.get_template("temp_template") is None
        
        # 删除不存在的模板
        result = manager.remove_template("nonexistent")
        assert result is False
    
    def test_format_template_success(self, manager):
        """测试格式化模板成功"""
        result = manager.format_template(
            "travel_planning",
            destination="北京",
            duration="3天",
            budget="5000元",
            travelers="2人",
            interests="历史文化",
            special_requirements="无"
        )
        
        assert "北京" in result
        assert "3天" in result
        assert "5000元" in result
    
    def test_format_template_not_exists(self, manager):
        """测试格式化不存在的模板"""
        with pytest.raises(ValueError, match="模板不存在"):
            manager.format_template("nonexistent")
    
    def test_format_template_missing_variables(self, manager):
        """测试格式化模板缺少变量"""
        with pytest.raises(ValueError, match="模板变量验证失败"):
            manager.format_template("travel_planning", destination="北京")
    
    def test_format_chat_prompt(self, manager):
        """测试格式化聊天提示词"""
        messages = [
            ChatMessage(role="system", content="你是一个助手"),
            ChatMessage(role="user", content="你好"),
            ChatMessage(role="assistant", content="你好！有什么可以帮助你的吗？"),
            ChatMessage(role="user", content="介绍一下北京")
        ]
        
        result = manager.format_chat_prompt(messages)
        
        assert "<|im_start|>system" in result
        assert "你是一个助手" in result
        assert "<|im_start|>user" in result
        assert "你好" in result
        assert "<|im_start|>assistant" in result
        assert "介绍一下北京" in result
    
    def test_format_chat_prompt_no_system(self, manager):
        """测试格式化聊天提示词（无系统消息）"""
        messages = [
            ChatMessage(role="user", content="你好")
        ]
        
        result = manager.format_chat_prompt(messages)
        
        # 应该使用默认系统消息
        assert "<|im_start|>system" in result
        assert "旅行规划助手" in result or "AI助手" in result
    
    def test_create_travel_planning_prompt(self, manager):
        """测试创建旅行规划提示词"""
        result = manager.create_travel_planning_prompt(
            destination="上海",
            duration="2天",
            budget="3000元",
            travelers="1人",
            interests="美食、购物",
            special_requirements="素食"
        )
        
        assert "上海" in result
        assert "2天" in result
        assert "3000元" in result
        assert "美食、购物" in result
        assert "素食" in result
    
    def test_create_attraction_prompt(self, manager):
        """测试创建景点推荐提示词"""
        result = manager.create_attraction_prompt(
            destination="杭州",
            attraction_type="自然景观",
            count=3,
            target_audience="家庭游客",
            budget_level="中等"
        )
        
        assert "杭州" in result
        assert "自然景观" in result
        assert "3" in result
        assert "家庭游客" in result
    
    def test_create_food_prompt(self, manager):
        """测试创建美食推荐提示词"""
        result = manager.create_food_prompt(
            destination="成都",
            cuisine_preference="川菜",
            price_range="中等价位",
            dining_scene="晚餐",
            dietary_restrictions="不吃辣"
        )
        
        assert "成都" in result
        assert "川菜" in result
        assert "中等价位" in result
        assert "不吃辣" in result
    
    def test_save_template_to_file(self, manager):
        """测试保存模板到文件"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            manager.save_template_to_file("travel_system", temp_path)
            
            # 验证文件内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert data["name"] == "travel_system"
            assert data["type"] == "system"
            assert "template" in data
            
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_save_nonexistent_template(self, manager):
        """测试保存不存在的模板"""
        with pytest.raises(ValueError, match="模板不存在"):
            manager.save_template_to_file("nonexistent", "/tmp/test.json")
    
    def test_export_all_templates(self, manager):
        """测试导出所有模板"""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager.export_all_templates(temp_dir)
            
            # 检查导出的文件
            export_path = Path(temp_dir)
            json_files = list(export_path.glob("*.json"))
            
            assert len(json_files) > 0
            
            # 验证其中一个文件
            for json_file in json_files:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                assert "name" in data
                assert "type" in data
                assert "template" in data
    
    def test_load_templates_from_dir(self):
        """测试从目录加载模板"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试模板文件
            template_data = {
                "name": "test_loaded_template",
                "type": "user",
                "template": "Test template: {param}",
                "description": "测试加载的模板",
                "variables": ["param"]
            }
            
            template_file = Path(temp_dir) / "test_template.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False)
            
            # 创建管理器并加载模板
            manager = PromptManager(templates_dir=temp_dir)
            
            # 验证模板已加载
            template = manager.get_template("test_loaded_template")
            assert template is not None
            assert template.name == "test_loaded_template"
            assert template.type == PromptType.USER
            assert template.variables == ["param"]


class TestGlobalPromptManager:
    """全局提示词管理器测试"""
    
    def test_get_prompt_manager(self):
        """测试获取全局提示词管理器"""
        manager1 = get_prompt_manager()
        manager2 = get_prompt_manager()
        
        # 应该返回同一个实例
        assert manager1 is manager2
        assert isinstance(manager1, PromptManager)
    
    def test_global_manager_has_defaults(self):
        """测试全局管理器有默认模板"""
        manager = get_prompt_manager()
        
        templates = manager.list_templates()
        assert "travel_system" in templates
        assert "travel_planning" in templates
        assert "qwen_chat" in templates