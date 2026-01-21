"""
语言模型客户端
使用 HTTP 请求，无需安装厂商 SDK
只需配置 URL + API Key + Model
"""

import time
import requests
from typing import Optional, Dict, Any
from config import get_config


class LLMClient:
    """统一的语言模型客户端 - 基于 HTTP 请求"""

    def __init__(self):
        self.config = get_config()
        self.llm_config = self.config.get_llm_config()
        self.provider = self.llm_config["provider"]

        if not self.config.use_mock_mode:
            self._initialize()

    def _initialize(self):
        """初始化客户端"""
        print(f"✓ {self.provider.upper()} 客户端初始化成功")
        print(f"  - URL: {self.llm_config.get('base_url')}")
        print(f"  - Model: {self.llm_config['model']}")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        生成文本

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）

        Returns:
            生成的文本
        """
        if self.config.use_mock_mode:
            return self._mock_generate(prompt)

        try:
            if self.provider == "anthropic":
                return self._generate_anthropic_http(prompt, system_prompt)
            elif self.provider == "openai":
                return self._generate_openai_http(prompt, system_prompt)
            elif self.provider == "dashscope":
                return self._generate_dashscope_http(prompt, system_prompt)
            else:
                # 默认尝试 OpenAI 兼容格式
                return self._generate_openai_http(prompt, system_prompt)
        except Exception as e:
            print(f"✗ LLM 调用失败: {e}")
            print(f"  切换到模拟模式")
            return self._mock_generate(prompt)

    def _generate_anthropic_http(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """使用 HTTP 调用 Anthropic API"""
        url = f"{self.llm_config['base_url']}/v1/messages"

        headers = {
            "x-api-key": self.llm_config["api_key"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        messages = [{"role": "user", "content": prompt}]

        data = {
            "model": self.llm_config["model"],
            "max_tokens": self.llm_config["max_tokens"],
            "temperature": self.llm_config["temperature"],
            "messages": messages
        }

        if system_prompt:
            data["system"] = system_prompt

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.llm_config["timeout"]
        )
        response.raise_for_status()

        result = response.json()
        return result["content"][0]["text"]

    def _generate_openai_http(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """使用 HTTP 调用 OpenAI API（也兼容其他 OpenAI 格式的服务）"""
        url = f"{self.llm_config['base_url']}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.llm_config['api_key']}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.llm_config["model"],
            "messages": messages,
            "max_tokens": self.llm_config["max_tokens"],
            "temperature": self.llm_config["temperature"],
            "top_p": self.llm_config["top_p"]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.llm_config["timeout"]
        )
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    def _generate_dashscope_http(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """使用 HTTP 调用阿里云通义千问 API"""
        url = f"{self.llm_config['base_url']}/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.llm_config['api_key']}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.llm_config["model"],
            "messages": messages,
            "parameters": {
                "max_tokens": self.llm_config["max_tokens"],
                "temperature": self.llm_config["temperature"],
                "top_p": self.llm_config["top_p"]
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=self.llm_config["timeout"]
        )
        response.raise_for_status()

        result = response.json()
        # 你的 API 返回的是 OpenAI 兼容格式
        return result["choices"][0]["message"]["content"]

    def _mock_generate(self, prompt: str) -> str:
        """模拟生成（用于测试）"""
        print(f"[模拟 LLM 调用] Provider: {self.provider}")
        time.sleep(0.5)  # 模拟网络延迟

        # 根据提示词关键字返回不同的模拟内容
        if "大纲" in prompt or "outline" in prompt.lower():
            return self._get_mock_outline()
        elif "角色" in prompt or "character" in prompt.lower() or "IP" in prompt:
            return self._get_mock_character()
        elif "分镜" in prompt or "storyboard" in prompt.lower():
            return self._get_mock_storyboard()
        elif "镜头" in prompt or "shot" in prompt.lower():
            return self._get_mock_shot()
        else:
            return f"[模拟内容]\n基于输入生成的响应: {prompt[:100]}..."

    def _get_mock_outline(self) -> str:
        """返回模拟的故事大纲"""
        return """故事大纲：《时光旅行者》

第一幕：发现
- 主角林晨在祖父遗物中发现一本神秘日记
- 日记中记录了关于时间机器的线索
- 林晨决定寻找时间机器的真相

第二幕：探索
- 林晨跟随线索来到废弃的实验室
- 成功启动了时间机器
- 意外穿越到100年前的同一地点

第三幕：抉择
- 在过去见到了年轻时的祖父
- 发现改变过去可能带来灾难性后果
- 必须在亲情和历史之间做出选择

第四幕：归来
- 林晨放弃改变过去
- 返回现代并封存了时间机器
- 明白了珍惜当下的重要性"""

    def _get_mock_character(self) -> str:
        """返回模拟的角色设计"""
        return """角色设计：

【主角】林晨
- 年龄：28岁
- 职业：物理学研究生
- 性格：好奇心强、理性、有责任感
- 外貌：中等身材、戴眼镜、略显书生气
- 背景：从小与祖父关系亲密，对科学充满热情

【配角】林祖父（年轻版）
- 年龄：25岁（1920年代）
- 职业：实验物理学家
- 性格：激进、理想主义、富有创造力
- 外貌：英俊、眼神坚定
- 背景：致力于时间研究的先驱科学家

【世界观】
- 时间：现代（2024年）与过去（1924年）
- 地点：某大学城及其周边
- 科技水平：时间机器是唯一的超现实科技
- 规则：改变过去会产生蝴蝶效应"""

    def _get_mock_storyboard(self) -> str:
        """返回模拟的分镜脚本"""
        return """分镜脚本：第一场景 - 发现日记

【分镜1】发现时刻
场景：祖父老房子的阁楼
时间：傍晚，阳光从窗户斜射进来
动作：林晨在整理遗物时，从旧木箱中拿出一本皮革日记
情绪：好奇、惊讶
镜头：中景，从侧面拍摄
时长：5秒

【分镜2】翻阅日记
场景：同一阁楼
动作：林晨坐在地板上，打开日记认真阅读
特写：日记上的手写文字和图表
情绪：专注、震惊
镜头：近景切特写
时长：8秒

【分镜3】震惊反应
场景：同一阁楼
动作：林晨猛然抬头，眼神中充满不可置信
情绪：震惊、兴奋
镜头：面部特写
时长：3秒"""

    def _get_mock_shot(self) -> str:
        """返回模拟的镜头设计"""
        return """镜头详细设计：

【镜头1-1】发现时刻 - 中景
- 画面构图：三分法，林晨位于右侧，窗户光源在左
- 运镜方式：固定镜头，slight push in
- 光线设计：暖色调黄昏光，灰尘在光线中飘浮
- 色彩基调：暖黄色为主，木质家具的棕色
- 道具清单：木箱、旧书、皮革日记、老照片
- 服装：林晨穿休闲衬衫和牛仔裤
- 场景氛围：怀旧、神秘

【镜头1-2】日记特写
- 画面构图：居中构图，日记占据画面70%
- 运镜方式：缓慢推进
- 光线设计：从上方45度角的柔光
- 可见内容：手绘时间机器草图、数学公式、日期"1924年3月"
- 细节强调：泛黄的纸张、钢笔墨迹、祖父的签名

【镜头1-3】面部特写
- 画面构图：居中偏上，留有头顶空间
- 表情细节：眼睛睁大、嘴巴微张、眉毛上扬
- 光线设计：Rembrandt lighting（伦勃朗光）
- 背景：虚化的阁楼环境
- 情绪传达：从怀疑到确信的转变"""


# 全局 LLM 客户端实例
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """获取全局 LLM 客户端实例（单例模式）"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


# 测试 LLM 客户端
if __name__ == "__main__":
    print("测试 LLM 客户端...")
    client = get_llm_client()

    # 测试生成
    response = client.generate("请写一个关于时间旅行的故事大纲")
    print("\n生成结果:")
    print(response)
