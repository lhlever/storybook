import json
import os

from openai import OpenAI

# ================= 配置区域 =================
# 1. 这里必须填入阿里云 DashScope 的真实 API KEY (以 sk- 开头)
# 如果你没有，请去阿里云百炼控制台创建一个，或者询问主办方索要 "sk-" 开头的 key
DASHSCOPE_API_KEY = "sk-b2badc27d4b747d6965d782e1638cfde"

# 2. 初始化 OpenAI 客户端 (适配 DashScope)
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)



MODEL_NAME = "qwen3-max"  # 或 "qwen-max"

# ================= Prompt 设计 =================
SYSTEM_PROMPT = """
你是一个专业的漫画分镜师和编剧 Agent。你的任务是将用户的一句话灵感转化为一套**严格包含 9 个画面**的 Storybook 脚本。

请严格遵守以下 JSON 输出规则，**这非常重要**：

1. **角色与场景设定 (Character Sheet)**：
   - 提取并固定角色外貌。
   - 设定统一画风。

2. **故事梗概 (Main Story)**：
   - 创作一段温馨的完整故事。

3. **9连画 (9 Frames)**：
   - **数量强制要求**：输出的 `frames` 数组**必须且只能包含 9 个对象**。
   - **严禁偷懒**：绝对不要只生成 3 个或 6 个，必须从 Frame 1 写到 Frame 9。
   - **连贯性**：
     - Frame 1-3: 开篇与铺垫
     - Frame 4-6: 情节发展或互动
     - Frame 7-9: 高潮与温馨结局
   - **视觉一致性**：在 `visual_prompt` 中，必须每次都**全量重复**角色的外貌描述（例如 "white-haired grandfather with glasses"），不要使用代词 "he/him"。

请仅输出纯 JSON 字符串，格式如下：
{
    "character_settings": "...",
    "main_story": "...",
    "frames": [
        { "frame_index": 1, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 2, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 3, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 4, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 5, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 6, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 7, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 8, "scene_description": "...", "visual_prompt": "..." },
        { "frame_index": 9, "scene_description": "...", "visual_prompt": "..." }
    ]
}
"""


def generate_story_data(user_prompt: str) -> dict:
    """
    核心函数：使用 OpenAI SDK 调用 Qwen
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            # 告诉模型强制返回 JSON (如果模型支持，Qwen-max/plus 效果通常很好)
            response_format={"type": "json_object"}
        )

        content = completion.choices[0].message.content

        # 清洗 Markdown 标记 (以防万一)
        if content.strip().startswith("```"):
            content = content.replace("```json", "").replace("```", "")

        return json.loads(content)

    except Exception as e:
        print(f"[Service Error] LLM Call failed: {e}")
        # 如果是 401，这里会打印具体的鉴权错误信息
        raise Exception(f"模型调用失败: {str(e)}")