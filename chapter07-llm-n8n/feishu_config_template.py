# 飞书 Turkish TTS 配置文件模板
# 请根据您的实际情况填写以下配置项

class FeishuTTSConfig:
    """
    飞书 Turkish TTS 系统配置类
    
    使用说明：
    1. 复制此文件为 feishu_config.py
    2. 填写所有必要的配置项
    3. 在主程序中导入使用
    """
    
    # ================================
    # ngrok 配置
    # ================================
    # 从 https://ngrok.com 获取您的认证token
    NGROK_TOKEN = "YOUR_NGROK_TOKEN_HERE"
    
    # ngrok端口配置
    NGROK_PORT = 7860
    
    # ================================
    # 飞书应用配置
    # ================================
    # 从飞书开放平台获取应用凭证
    FEISHU_APP_ID = "YOUR_FEISHU_APP_ID"                    # 应用标识
    FEISHU_APP_SECRET = "YOUR_FEISHU_APP_SECRET"            # 应用密钥
    FEISHU_VERIFICATION_TOKEN = "YOUR_VERIFICATION_TOKEN"   # 事件验证Token
    FEISHU_ENCRYPT_KEY = ""                                 # 事件加密密钥（可选）
    
    # 飞书API基础配置
    FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
    FEISHU_TOKEN_EXPIRE_BUFFER = 300  # Token提前过期时间（秒）
    
    # ================================
    # TTS 模型配置
    # ================================
    # XTTS v2 模型名称
    TTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # 默认语言
    DEFAULT_LANGUAGE = "tr"  # 土耳其语
    
    # 支持的语言列表
    SUPPORTED_LANGUAGES = [
        "tr",  # 土耳其语
        "en",  # 英语
        "zh",  # 中文
        "es",  # 西班牙语
        "fr",  # 法语
        "de",  # 德语
        "it",  # 意大利语
        "pt",  # 葡萄牙语
        "ru",  # 俄语
        "ja",  # 日语
        "ko",  # 韩语
    ]
    
    # 音频样本文件路径（可选）
    SPEAKER_SAMPLE_PATH = None  # 如："turkish_speaker.wav"
    
    # ================================
    # API 服务配置
    # ================================
    # FastAPI 服务器配置
    API_HOST = "0.0.0.0"
    API_PORT = 7860
    API_LOG_LEVEL = "info"
    
    # API 限制配置
    MAX_TEXT_LENGTH = 1000  # 最大文本长度
    API_TIMEOUT = 60        # API超时时间（秒）
    
    # 文件配置
    OUTPUT_FORMAT = "mp3"   # 输出音频格式
    TEMP_FILE_PREFIX = "feishu_tts_output"
    
    # ================================
    # 飞书机器人配置
    # ================================
    # 机器人基本信息
    BOT_NAME = "Turkish TTS Bot"
    BOT_DESCRIPTION = "土耳其语文本转语音助手"
    BOT_VERSION = "1.0.0"
    
    # 支持的命令列表
    SUPPORTED_COMMANDS = {
        "/help": "显示帮助信息",
        "/帮助": "显示帮助信息",
        "/status": "查看系统状态",
        "/状态": "查看系统状态",
        "/test": "测试TTS功能",
        "/测试": "测试TTS功能"
    }
    
    # 回复消息模板
    REPLY_TEMPLATES = {
        "processing": "🎵 正在生成语音，请稍候...",
        "test_processing": "🧪 正在进行TTS测试，请稍候...",
        "error_tts_failed": "❌ 语音生成失败，请稍后重试",
        "error_upload_failed": "❌ 语音文件上传失败，请稍后重试",
        "error_send_failed": "❌ 语音发送失败，请稍后重试",
        "error_text_empty": "❌ 文本不能为空",
        "error_text_too_long": "⚠️ 文本太长，请控制在{max_length}字符以内",
        "error_unknown_command": "❓ 未知命令: {command}\\n发送 /help 查看可用命令"
    }
    
    # ================================
    # 企业功能配置
    # ================================
    # 用户权限管理
    ENABLE_USER_PERMISSION = False   # 是否启用用户权限控制
    ALLOWED_DEPARTMENTS = []          # 允许使用的部门ID列表
    ALLOWED_USERS = []               # 允许使用的用户ID列表
    
    # 使用统计
    ENABLE_USAGE_STATS = True       # 是否启用使用统计
    STATS_COLLECTION_INTERVAL = 3600 # 统计收集间隔（秒）
    
    # 审计日志
    ENABLE_AUDIT_LOG = True         # 是否启用审计日志
    AUDIT_LOG_LEVEL = "INFO"        # 审计日志级别
    
    # ================================
    # 系统性能配置
    # ================================
    # GPU 配置
    USE_GPU = True          # 是否使用GPU加速
    GPU_MEMORY_FRACTION = 0.8  # GPU内存使用比例
    
    # 并发配置
    MAX_CONCURRENT_REQUESTS = 2  # 最大并发请求数
    REQUEST_QUEUE_SIZE = 10      # 请求队列大小
    
    # 缓存配置
    ENABLE_CACHE = False    # 是否启用缓存
    CACHE_TTL = 3600       # 缓存过期时间（秒）
    
    # 飞书API限制
    FEISHU_API_RATE_LIMIT = 100    # 每分钟API调用限制
    FEISHU_FILE_SIZE_LIMIT = 20 * 1024 * 1024  # 文件大小限制（20MB）
    
    # ================================
    # 文件管理配置
    # ================================
    # 临时文件清理
    AUTO_CLEANUP = True     # 是否自动清理临时文件
    CLEANUP_INTERVAL = 300  # 清理间隔（秒）
    MAX_FILE_AGE = 3600    # 文件最大保存时间（秒）
    
    # 文件大小限制
    MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_OUTPUT_SIZE = 10 * 1024 * 1024  # 10MB
    
    # ================================
    # 日志配置
    # ================================
    # 日志级别
    LOG_LEVEL = "INFO"
    
    # 日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 日志文件配置
    LOG_TO_FILE = False
    LOG_FILE_PATH = "feishu_tts.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # 飞书专用日志
    FEISHU_LOG_EVENTS = True        # 是否记录飞书事件
    FEISHU_LOG_API_CALLS = True     # 是否记录API调用
    
    # ================================
    # 错误处理配置
    # ================================
    # 重试配置
    MAX_RETRIES = 3         # 最大重试次数
    RETRY_DELAY = 5         # 重试延迟（秒）
    
    # 飞书特定错误处理
    FEISHU_ERROR_RETRY_CODES = [429, 500, 502, 503, 504]  # 需要重试的错误码
    FEISHU_TOKEN_REFRESH_ON_401 = True  # 401错误时是否自动刷新token
    
    # ================================
    # 开发和调试配置
    # ================================
    # 调试模式
    DEBUG_MODE = False
    
    # 测试配置
    TEST_MODE = False
    TEST_TEXT = "Merhaba! Bu bir test mesajıdır. Feishu entegrasyonu çalışıyor."
    
    # 性能监控
    ENABLE_METRICS = False
    METRICS_PORT = 8080
    
    # 飞书调试
    FEISHU_DEBUG_WEBHOOK = False    # 是否调试webhook事件
    FEISHU_MOCK_MODE = False        # 是否使用模拟模式
    
    # ================================
    # 高级功能配置
    # ================================
    # 语音质量配置
    AUDIO_QUALITY = "standard"  # standard, high, low
    SAMPLE_RATE = 22050        # 音频采样率
    
    # 语音风格配置（实验性功能）
    ENABLE_STYLE_CONTROL = False
    DEFAULT_STYLE = "neutral"
    AVAILABLE_STYLES = ["neutral", "happy", "sad", "excited"]
    
    # 多租户支持
    ENABLE_MULTI_TENANT = False    # 是否支持多租户
    TENANT_ISOLATION = "app_id"    # 租户隔离方式
    
    # 企业集成
    ENABLE_SSO = False             # 是否启用单点登录
    ENABLE_LDAP = False            # 是否集成LDAP
    
    # ================================
    # 飞书事件配置
    # ================================
    # 事件订阅配置
    SUBSCRIBE_EVENTS = [
        "im.message.receive_v1",     # 接收消息
        "im.message.message_read_v1", # 消息已读（可选）
    ]
    
    # 事件处理配置
    EVENT_TIMEOUT = 30             # 事件处理超时时间
    EVENT_RETRY_COUNT = 3          # 事件处理重试次数
    
    # Webhook配置
    WEBHOOK_PATH = "/feishu/events"
    WEBHOOK_VERIFY_SIGNATURE = True  # 是否验证签名
    
    @classmethod
    def validate_config(cls):
        """
        验证配置的有效性
        
        Returns:
            tuple: (is_valid, error_message)
        """
        errors = []
        
        # 验证必要的token
        if cls.NGROK_TOKEN == "YOUR_NGROK_TOKEN_HERE" or not cls.NGROK_TOKEN:
            errors.append("请设置有效的 NGROK_TOKEN")
            
        if cls.FEISHU_APP_ID == "YOUR_FEISHU_APP_ID" or not cls.FEISHU_APP_ID:
            errors.append("请设置有效的 FEISHU_APP_ID")
            
        if cls.FEISHU_APP_SECRET == "YOUR_FEISHU_APP_SECRET" or not cls.FEISHU_APP_SECRET:
            errors.append("请设置有效的 FEISHU_APP_SECRET")
            
        if cls.FEISHU_VERIFICATION_TOKEN == "YOUR_VERIFICATION_TOKEN" or not cls.FEISHU_VERIFICATION_TOKEN:
            errors.append("请设置有效的 FEISHU_VERIFICATION_TOKEN")
        
        # 验证端口配置
        if not (1024 <= cls.API_PORT <= 65535):
            errors.append("API_PORT 必须在 1024-65535 范围内")
            
        if not (1024 <= cls.NGROK_PORT <= 65535):
            errors.append("NGROK_PORT 必须在 1024-65535 范围内")
        
        # 验证文本长度限制
        if cls.MAX_TEXT_LENGTH <= 0:
            errors.append("MAX_TEXT_LENGTH 必须大于 0")
            
        # 验证超时设置
        if cls.API_TIMEOUT <= 0:
            errors.append("API_TIMEOUT 必须大于 0")
        
        # 验证语言配置
        if cls.DEFAULT_LANGUAGE not in cls.SUPPORTED_LANGUAGES:
            errors.append(f"DEFAULT_LANGUAGE '{cls.DEFAULT_LANGUAGE}' 不在支持的语言列表中")
        
        # 验证飞书特定配置
        if cls.FEISHU_API_RATE_LIMIT <= 0:
            errors.append("FEISHU_API_RATE_LIMIT 必须大于 0")
            
        if cls.FEISHU_FILE_SIZE_LIMIT <= 0:
            errors.append("FEISHU_FILE_SIZE_LIMIT 必须大于 0")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, "配置验证通过"
    
    @classmethod
    def get_config_summary(cls):
        """
        获取配置摘要信息
        
        Returns:
            dict: 配置摘要
        """
        return {
            "ngrok_configured": cls.NGROK_TOKEN != "YOUR_NGROK_TOKEN_HERE",
            "feishu_app_configured": cls.FEISHU_APP_ID != "YOUR_FEISHU_APP_ID",
            "feishu_secret_configured": cls.FEISHU_APP_SECRET != "YOUR_FEISHU_APP_SECRET",
            "verification_token_configured": cls.FEISHU_VERIFICATION_TOKEN != "YOUR_VERIFICATION_TOKEN",
            "api_port": cls.API_PORT,
            "default_language": cls.DEFAULT_LANGUAGE,
            "supported_languages": cls.SUPPORTED_LANGUAGES,
            "max_text_length": cls.MAX_TEXT_LENGTH,
            "gpu_enabled": cls.USE_GPU,
            "debug_mode": cls.DEBUG_MODE,
            "enterprise_features": {
                "user_permission": cls.ENABLE_USER_PERMISSION,
                "usage_stats": cls.ENABLE_USAGE_STATS,
                "audit_log": cls.ENABLE_AUDIT_LOG,
                "multi_tenant": cls.ENABLE_MULTI_TENANT
            }
        }
    
    @classmethod
    def get_feishu_help_text(cls):
        """
        获取飞书机器人帮助文本
        
        Returns:
            str: 帮助文本
        """
        commands_text = "\\n".join([f"• {cmd} - {desc}" for cmd, desc in cls.SUPPORTED_COMMANDS.items()])
        languages_text = ", ".join(cls.SUPPORTED_LANGUAGES)
        
        return f"""🤖 {cls.BOT_NAME} 使用说明：

📝 **基本用法**：
• 直接发送文本，我会转换为语音回复
• 主要优化{cls.DEFAULT_LANGUAGE}语言，同时支持多语言

🎯 **命令列表**：
{commands_text}

💡 **使用提示**：
• 文本长度建议控制在{cls.MAX_TEXT_LENGTH}字符以内
• 为获得最佳效果，请使用标准语法
• 语音生成可能需要15-30秒时间

🌍 **支持语言**：
{languages_text}

🔧 **技术支持**：
• 基于开源XTTS v2模型
• 运行在Google Colab免费GPU上
• 支持声音克隆和多语言TTS
• 版本：{cls.BOT_VERSION}"""

# ================================
# 使用示例
# ================================
if __name__ == "__main__":
    # 验证配置
    is_valid, message = FeishuTTSConfig.validate_config()
    
    if is_valid:
        print("✅ 配置验证通过")
        
        # 显示配置摘要
        summary = FeishuTTSConfig.get_config_summary()
        print("\\n📋 配置摘要：")
        for key, value in summary.items():
            if key == "enterprise_features":
                print(f"   企业功能:")
                for feat_key, feat_value in value.items():
                    print(f"     {feat_key}: {feat_value}")
            else:
                print(f"   {key}: {value}")
                
        # 显示帮助文本预览
        print("\\n📖 机器人帮助文本预览：")
        print("-" * 50)
        print(FeishuTTSConfig.get_feishu_help_text())
        print("-" * 50)
    else:
        print(f"❌ 配置验证失败: {message}")
        print("\\n💡 请检查并修正配置文件中的错误")

# ================================
# 配置模板说明
# ================================
"""
飞书TTS配置使用步骤：

1. 复制配置模板
   cp feishu_config_template.py feishu_config.py

2. 编辑配置文件
   - 填入您的 ngrok token
   - 填入飞书应用 App ID、App Secret、Verification Token
   - 根据企业需求调整其他配置项

3. 验证配置
   python feishu_config.py

4. 在主程序中导入
   from feishu_config import FeishuTTSConfig

飞书特殊配置项：
- FEISHU_APP_ID: 飞书应用标识
- FEISHU_APP_SECRET: 飞书应用密钥
- FEISHU_VERIFICATION_TOKEN: 事件验证token
- FEISHU_ENCRYPT_KEY: 事件加密密钥（可选）

企业功能配置：
- ENABLE_USER_PERMISSION: 用户权限控制
- ENABLE_USAGE_STATS: 使用统计分析
- ENABLE_AUDIT_LOG: 操作审计日志
- ENABLE_MULTI_TENANT: 多租户支持

安全提示：
- 飞书凭证比Telegram更敏感，请妥善保管
- 建议在生产环境使用环境变量
- 定期轮换App Secret
- 启用审计日志监控异常访问

环境变量示例：
export NGROK_TOKEN="your_token_here"
export FEISHU_APP_ID="cli_xxxxxxxxxx"
export FEISHU_APP_SECRET="your_app_secret_here"
export FEISHU_VERIFICATION_TOKEN="your_verification_token"
""" 