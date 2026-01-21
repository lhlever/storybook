"""
文生图客户端
使用 HTTP 请求，无需安装厂商 SDK
只需配置 URL + API Key + Model
"""

import time
import base64
import requests
from typing import Optional, Dict, Any
from pathlib import Path
from config import get_config


class ImageClient:
    """统一的文生图客户端 - 基于 HTTP 请求"""

    def __init__(self):
        self.config = get_config()
        self.image_config = self.config.get_image_config()
        self.provider = self.image_config["provider"]

        if not self.config.use_mock_mode:
            self._initialize()

    def _initialize(self):
        """初始化客户端"""
        print(f"✓ {self.provider.upper()} 图像客户端初始化成功")
        print(f"  - URL: {self.image_config.get('base_url')}")
        if "model" in self.image_config:
            print(f"  - Model: {self.image_config['model']}")

    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        style: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成图像

        Args:
            prompt: 图像描述提示词
            negative_prompt: 负面提示词（不想要的元素）
            style: 风格（如：anime, realistic, cartoon）
            save_path: 保存路径（可选）

        Returns:
            包含图像信息的字典
        """
        if self.config.use_mock_mode:
            return self._mock_generate(prompt, save_path)

        try:
            if self.provider == "dalle":
                return self._generate_dalle_http(prompt, save_path)
            elif self.provider == "stability":
                return self._generate_stability_http(prompt, negative_prompt, save_path)
            elif self.provider == "dashscope":
                return self._generate_dashscope_http(prompt, negative_prompt, save_path)
            else:
                # 默认尝试类似 DALL-E 的格式
                return self._generate_dalle_http(prompt, save_path)
        except Exception as e:
            print(f"✗ 图像生成失败: {e}")
            print(f"  切换到模拟模式")
            return self._mock_generate(prompt, save_path)

    def _generate_dalle_http(self, prompt: str, save_path: Optional[str] = None) -> Dict[str, Any]:
        """使用 HTTP 调用 DALL-E API"""
        url = f"{self.image_config['base_url']}/v1/images/generations"

        headers = {
            "Authorization": f"Bearer {self.image_config['api_key']}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.image_config["model"],
            "prompt": prompt,
            "n": self.image_config["num_samples"],
            "size": self.image_config["size"],
            "quality": self.image_config["quality"]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.image_config["timeout"]
        )
        response.raise_for_status()

        result = response.json()
        image_url = result["data"][0]["url"]

        output = {
            "url": image_url,
            "provider": "dalle",
            "prompt": prompt,
        }

        if save_path:
            self._download_image(image_url, save_path)
            output["local_path"] = save_path

        return output

    def _generate_stability_http(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """使用 HTTP 调用 Stability AI API"""
        engine_id = self.image_config["model"]
        url = f"{self.image_config['base_url']}/generation/{engine_id}/text-to-image"

        headers = {
            "Authorization": f"Bearer {self.image_config['api_key']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        text_prompts = [{"text": prompt, "weight": 1.0}]
        if negative_prompt:
            text_prompts.append({"text": negative_prompt, "weight": -1.0})

        data = {
            "text_prompts": text_prompts,
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "steps": self.image_config["steps"],
            "samples": self.image_config["num_samples"]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.image_config["timeout"]
        )
        response.raise_for_status()

        result = response.json()
        image_base64 = result["artifacts"][0]["base64"]

        output = {
            "base64": image_base64,
            "provider": "stability",
            "prompt": prompt,
        }

        if save_path:
            image_data = base64.b64decode(image_base64)
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(image_data)
            output["local_path"] = save_path
            print(f"✓ 图像已保存到: {save_path}")

        return output

    def _generate_dashscope_http(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """使用 HTTP 调用阿里云通义万相 API"""
        url = f"{self.image_config['base_url']}/services/aigc/text2image/image-synthesis"

        headers = {
            "Authorization": f"Bearer {self.image_config['api_key']}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.image_config.get("model", "wanx-v1"),
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "size": "1024*1024",
                "n": self.image_config["num_samples"]
            }
        }

        if negative_prompt:
            data["input"]["negative_prompt"] = negative_prompt

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.image_config["timeout"]
        )
        response.raise_for_status()

        result = response.json()
        image_url = result["output"]["results"][0]["url"]

        output = {
            "url": image_url,
            "provider": "dashscope",
            "prompt": prompt,
        }

        if save_path:
            self._download_image(image_url, save_path)
            output["local_path"] = save_path

        return output

    def _download_image(self, url: str, save_path: str):
        """下载图像到本地"""
        response = requests.get(url, timeout=self.config.api_timeout)
        response.raise_for_status()

        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"✓ 图像已保存到: {save_path}")

    def _mock_generate(self, prompt: str, save_path: Optional[str] = None) -> Dict[str, Any]:
        """模拟图像生成"""
        print(f"[模拟图像生成] Provider: {self.provider}")
        print(f"[提示词] {prompt}")
        time.sleep(1.0)  # 模拟生成时间

        result = {
            "provider": "mock",
            "prompt": prompt,
            "mock_url": "https://via.placeholder.com/1024x1024.png?text=Mock+Image",
            "message": "这是模拟生成的图像，实际使用时会调用真实的 API"
        }

        # 创建一个简单的占位图像（可选）
        if save_path:
            self._create_placeholder_image(save_path, prompt)
            result["local_path"] = save_path

        return result

    def _create_placeholder_image(self, save_path: str, text: str):
        """创建占位图像（用于测试）"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            # 创建白色背景
            img = Image.new('RGB', (1024, 1024), color='white')
            draw = ImageDraw.Draw(img)

            # 添加文字
            try:
                font = ImageFont.truetype("Arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            text_lines = [
                "[模拟图像]",
                "",
                f"提示词:",
                text[:50] + "..." if len(text) > 50 else text,
            ]

            y = 400
            for line in text_lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (1024 - text_width) // 2
                draw.text((x, y), line, fill='black', font=font)
                y += 60

            # 保存
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(save_path)
            print(f"✓ 占位图像已创建: {save_path}")

        except ImportError:
            print("⚠️  PIL 未安装，无法创建占位图像")
            print("   可以安装: pip install Pillow")


# 全局图像客户端实例
_image_client: Optional[ImageClient] = None


def get_image_client() -> ImageClient:
    """获取全局图像客户端实例（单例模式）"""
    global _image_client
    if _image_client is None:
        _image_client = ImageClient()
    return _image_client


if __name__ == "__main__":
    # 测试图像客户端
    print("测试图像客户端...")
    client = get_image_client()

    # 测试生成
    result = client.generate(
        "一个年轻人在阁楼里翻看旧日记，温暖的黄昏光线",
        save_path="test_image.png"
    )
    print("\n生成结果:")
    print(result)
