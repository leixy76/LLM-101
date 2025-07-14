# Telegram Turkish TTS 配置文件模板
# 请根据您的实际情况填写以下配置项

class TelegramTTSConfig:
    """
    Telegram Turkish TTS 系统配置类
    
    使用说明：
    1. 复制此文件为 config.py
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
    # Telegram Bot 配置
    # ================================
    # 从 @BotFather 获取您的Bot Token
    TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    # Telegram API 基础URL
    TELEGRAM_API_BASE = "https://api.telegram.org/bot"
    
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
        "es",  # 西班牙语
        "fr",  # 法语
        "de",  # 德语
        "it",  # 意大利语
        "pt",  # 葡萄牙语
        "ru",  # 俄语
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
    TEMP_FILE_PREFIX = "tts_output"
    
    # ================================
    # n8n 工作流配置
    # ================================
    # n8n webhook 路径
    N8N_WEBHOOK_PATH = "telegram-webhook"
    
    # n8n 服务器地址（如果使用云端n8n）
    N8N_SERVER_URL = None  # 如："https://your-n8n-instance.com"
    
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
    LOG_FILE_PATH = "telegram_tts.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # ================================
    # 错误处理配置
    # ================================
    # 重试配置
    MAX_RETRIES = 3         # 最大重试次数
    RETRY_DELAY = 5         # 重试延迟（秒）
    
    # 错误消息配置
    ERROR_MESSAGES = {
        "text_too_long": "⚠️ 文本太长，请控制在{max_length}字符以内",
        "text_empty": "❌ 文本不能为空",
        "tts_failed": "❌ 语音生成失败，请稍后重试",
        "api_timeout": "⏰ 处理超时，请尝试较短的文本",
        "server_error": "🔧 服务器错误，请联系管理员",
        "unsupported_language": "🌍 不支持的语言，请使用：{languages}"
    }
    
    # ================================
    # 开发和调试配置
    # ================================
    # 调试模式
    DEBUG_MODE = False
    
    # 测试配置
    TEST_MODE = False
    TEST_TEXT = "Merhaba! Bu bir test mesajıdır."
    
    # 性能监控
    ENABLE_METRICS = False
    METRICS_PORT = 8080
    
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
    
    # 多用户支持
    ENABLE_USER_MANAGEMENT = False
    MAX_USERS = 100
    USER_RATE_LIMIT = 10  # 每分钟请求限制
    
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
            
        if cls.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not cls.TELEGRAM_BOT_TOKEN:
            errors.append("请设置有效的 TELEGRAM_BOT_TOKEN")
        
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
            "telegram_configured": cls.TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE",
            "api_port": cls.API_PORT,
            "default_language": cls.DEFAULT_LANGUAGE,
            "supported_languages": cls.SUPPORTED_LANGUAGES,
            "max_text_length": cls.MAX_TEXT_LENGTH,
            "gpu_enabled": cls.USE_GPU,
            "debug_mode": cls.DEBUG_MODE
        }

# ================================
# 使用示例
# ================================
if __name__ == "__main__":
    # 验证配置
    is_valid, message = TelegramTTSConfig.validate_config()
    
    if is_valid:
        print("✅ 配置验证通过")
        
        # 显示配置摘要
        summary = TelegramTTSConfig.get_config_summary()
        print("\n📋 配置摘要：")
        for key, value in summary.items():
            print(f"   {key}: {value}")
    else:
        print(f"❌ 配置验证失败: {message}")
        print("\n💡 请检查并修正配置文件中的错误")

# ================================
# 配置模板说明
# ================================
"""
使用步骤：

1. 复制配置模板
   cp config_template.py config.py

2. 编辑配置文件
   - 填入您的 ngrok token
   - 填入您的 Telegram Bot token
   - 根据需要调整其他配置项

3. 验证配置
   python config.py

4. 在主程序中导入
   from config import TelegramTTSConfig
   
配置优先级：
1. 环境变量（如果设置）
2. config.py 文件
3. 默认值

环境变量示例：
export NGROK_TOKEN="your_token_here"
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

安全提示：
- 不要将包含真实token的配置文件提交到代码仓库
- 使用 .gitignore 忽略 config.py 文件
- 在生产环境中使用环境变量管理敏感信息
""" 