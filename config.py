"""
配置管理模块
从环境变量和配置文件中加载配置
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ 已加载配置文件: {env_path}")
else:
    print(f"⚠ 未找到 .env 文件，使用默认配置（模拟模式）")


class Config:
    """统一配置管理类"""

    def __init__(self):
        self._load_config()

    def _load_config(self):
        """加载所有配置"""
        # ===== LLM 配置 =====
        self.llm_provider = os.getenv("LLM_PROVIDER", "anthropic").lower()

        # Anthropic
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.anthropic_base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5-20251101")

        # OpenAI
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")

        # 阿里云通义千问
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.dashscope_base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")
        self.dashscope_model = os.getenv("DASHSCOPE_MODEL", "qwen-max")

        # LLM 参数
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.llm_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2048"))
        self.llm_top_p = float(os.getenv("LLM_TOP_P", "1.0"))

        # ===== 文生图配置 =====
        self.image_provider = os.getenv("IMAGE_PROVIDER", "dalle").lower()

        # DALL-E
        self.dalle_api_key = os.getenv("DALLE_API_KEY", "")
        self.dalle_base_url = os.getenv("DALLE_BASE_URL", "https://api.openai.com/v1")
        self.dalle_model = os.getenv("DALLE_MODEL", "dall-e-3")
        self.dalle_size = os.getenv("DALLE_SIZE", "1024x1024")
        self.dalle_quality = os.getenv("DALLE_QUALITY", "standard")

        # Stability AI
        self.stability_api_key = os.getenv("STABILITY_API_KEY", "")
        self.stability_base_url = os.getenv("STABILITY_BASE_URL", "https://api.stability.ai/v1")
        self.stability_model = os.getenv("STABILITY_MODEL", "stable-diffusion-xl-1024-v1-0")

        # Replicate
        self.replicate_api_token = os.getenv("REPLICATE_API_TOKEN", "")
        self.replicate_base_url = os.getenv("REPLICATE_BASE_URL", "https://api.replicate.com")

        # 阿里云通义万相
        self.dashscope_image_api_key = os.getenv("DASHSCOPE_IMAGE_API_KEY", "")
        self.dashscope_image_base_url = os.getenv("DASHSCOPE_IMAGE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")
        self.dashscope_image_model = os.getenv("DASHSCOPE_IMAGE_MODEL", "wanx-v1")

        # Image 参数
        self.image_num_samples = int(os.getenv("IMAGE_NUM_SAMPLES", "1"))
        self.image_steps = int(os.getenv("IMAGE_STEPS", "50"))

        # ===== 应用配置 =====
        self.use_mock_mode = os.getenv("USE_MOCK_MODE", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.memory_storage_path = os.getenv("MEMORY_STORAGE_PATH", "memory_storage")
        self.api_timeout = int(os.getenv("API_TIMEOUT", "60"))
        self.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS", "3"))

        # ===== 漫画生成配置 =====
        self.comic_panels = int(os.getenv("COMIC_PANELS", "6"))  # 默认生成6格漫画
        self.comic_style = os.getenv("COMIC_STYLE", "manga")  # 默认日漫风格

        # 自动检测模拟模式
        if self._should_use_mock_mode():
            self.use_mock_mode = True
            print("ℹ️  未检测到有效的 API Key，自动启用模拟模式")

    def _should_use_mock_mode(self) -> bool:
        """判断是否应该使用模拟模式"""
        # 如果明确设置了 USE_MOCK_MODE=true，直接返回
        if self.use_mock_mode:
            return True

        # 检查 LLM 配置
        llm_configured = False
        if self.llm_provider == "anthropic" and self.anthropic_api_key:
            llm_configured = True
        elif self.llm_provider == "openai" and self.openai_api_key:
            llm_configured = True
        elif self.llm_provider == "dashscope" and self.dashscope_api_key:
            llm_configured = True

        # 如果没有配置 LLM，则使用模拟模式
        return not llm_configured

    def get_llm_config(self) -> Dict[str, Any]:
        """获取 LLM 配置"""
        config = {
            "provider": self.llm_provider,
            "temperature": self.llm_temperature,
            "max_tokens": self.llm_max_tokens,
            "top_p": self.llm_top_p,
            "timeout": self.api_timeout,
        }

        if self.llm_provider == "anthropic":
            config.update({
                "api_key": self.anthropic_api_key,
                "base_url": self.anthropic_base_url,
                "model": self.anthropic_model,
            })
        elif self.llm_provider == "openai":
            config.update({
                "api_key": self.openai_api_key,
                "base_url": self.openai_base_url,
                "model": self.openai_model,
            })
        elif self.llm_provider == "dashscope":
            config.update({
                "api_key": self.dashscope_api_key,
                "base_url": self.dashscope_base_url,
                "model": self.dashscope_model,
            })

        return config

    def get_image_config(self) -> Dict[str, Any]:
        """获取文生图配置"""
        config = {
            "provider": self.image_provider,
            "num_samples": self.image_num_samples,
            "steps": self.image_steps,
            "timeout": self.api_timeout,
        }

        if self.image_provider == "dalle":
            config.update({
                "api_key": self.dalle_api_key,
                "base_url": self.dalle_base_url,
                "model": self.dalle_model,
                "size": self.dalle_size,
                "quality": self.dalle_quality,
            })
        elif self.image_provider == "stability":
            config.update({
                "api_key": self.stability_api_key,
                "base_url": self.stability_base_url,
                "model": self.stability_model,
            })
        elif self.image_provider == "replicate":
            config.update({
                "api_token": self.replicate_api_token,
                "base_url": self.replicate_base_url,
            })
        elif self.image_provider == "dashscope":
            config.update({
                "api_key": self.dashscope_image_api_key,
                "base_url": self.dashscope_image_base_url,
                "model": self.dashscope_image_model,
            })

        return config

    def validate(self) -> bool:
        """验证配置是否有效"""
        if self.use_mock_mode:
            print("✓ 使用模拟模式，跳过配置验证")
            return True

        errors = []

        # 验证 LLM 配置
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            errors.append("缺少 ANTHROPIC_API_KEY")
        elif self.llm_provider == "openai" and not self.openai_api_key:
            errors.append("缺少 OPENAI_API_KEY")
        elif self.llm_provider == "dashscope" and not self.dashscope_api_key:
            errors.append("缺少 DASHSCOPE_API_KEY")

        # 验证文生图配置（可选）
        if self.image_provider == "dalle" and not self.dalle_api_key:
            print("⚠️  警告: 未配置 DALLE_API_KEY，文生图功能将不可用")
        elif self.image_provider == "stability" and not self.stability_api_key:
            print("⚠️  警告: 未配置 STABILITY_API_KEY，文生图功能将不可用")

        if errors:
            print("✗ 配置验证失败:")
            for error in errors:
                print(f"  - {error}")
            return False

        print("✓ 配置验证成功")
        return True

    def print_summary(self):
        """打印配置摘要"""
        print("\n" + "=" * 60)
        print("📋 当前配置摘要")
        print("=" * 60)
        print(f"模式: {'🔧 模拟模式' if self.use_mock_mode else '🚀 真实 API 模式'}")
        print(f"\nLLM 配置:")
        print(f"  - 提供商: {self.llm_provider}")
        if self.llm_provider == "anthropic":
            print(f"  - 模型: {self.anthropic_model}")
            print(f"  - API Key: {'已配置' if self.anthropic_api_key else '未配置'}")
        elif self.llm_provider == "openai":
            print(f"  - 模型: {self.openai_model}")
            print(f"  - API Key: {'已配置' if self.openai_api_key else '未配置'}")
        elif self.llm_provider == "dashscope":
            print(f"  - 模型: {self.dashscope_model}")
            print(f"  - API Key: {'已配置' if self.dashscope_api_key else '未配置'}")
        print(f"  - Temperature: {self.llm_temperature}")
        print(f"  - Max Tokens: {self.llm_max_tokens}")

        print(f"\n文生图配置:")
        print(f"  - 提供商: {self.image_provider}")
        if self.image_provider == "dalle":
            print(f"  - 模型: {self.dalle_model}")
            print(f"  - API Key: {'已配置' if self.dalle_api_key else '未配置'}")
        elif self.image_provider == "stability":
            print(f"  - 模型: {self.stability_model}")
            print(f"  - API Key: {'已配置' if self.stability_api_key else '未配置'}")

        print(f"\n其他配置:")
        print(f"  - Memory 路径: {self.memory_storage_path}")
        print(f"  - API 超时: {self.api_timeout}秒")
        print(f"  - 日志级别: {self.log_level}")
        print("=" * 60 + "\n")


# 全局配置实例
config = Config()


def get_config() -> Config:
    """获取全局配置实例"""
    return config


if __name__ == "__main__":
    # 测试配置
    cfg = get_config()
    cfg.print_summary()
    cfg.validate()
