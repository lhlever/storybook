"""
工具函数模块 - 漫画生成
提供漫画创作过程中的各种工具调用
- generate_comic_outline: 生成漫画大纲
- design_characters: 设计角色形象
- generate_story_segments: 生成分段故事文本
- generate_image_prompts: 生成图片提示词
- generate_images_from_prompts: 文生图
"""

from typing import Dict, Any, List, Optional
import time
import json
import os
import requests
from llm_client import get_llm_client
from image_client import get_image_client
from config import get_config


def call_llm(prompt: str, task_type: str, system_prompt: Optional[str] = None) -> str:
    """
    调用语言模型生成内容
    根据配置自动选择使用真实 API 还是模拟模式

    Args:
        prompt: 用户提示词
        task_type: 任务类型（用于日志显示）
        system_prompt: 系统提示词

    Returns:
        生成的文本内容
    """
    config = get_config()

    print(f"\n[{'模拟' if config.use_mock_mode else 'LLM'} 调用] {task_type}...")

    llm_client = get_llm_client()
    return llm_client.generate(prompt, system_prompt)


def generate_comic_outline(user_input: str, memory_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成漫画大纲

    Args:
        user_input: 用户输入的漫画创意
        memory_context: 来自 Memory 的上下文信息

    Returns:
        包含漫画大纲的字典
    """
    # 获取配置中的格数和风格
    config = get_config()
    comic_panels = config.comic_panels
    comic_style = config.comic_style

    prompt = f"""你是一个专业的漫画编剧。请根据以下创意生成漫画故事大纲：

【创意】
{user_input}

【要求】
- 生成适合漫画表现的故事情节
- 包含明确的起承转合
- **必须生成恰好 {comic_panels} 格漫画**（严格按照此数量）
- 标注每格的关键情节点
- 漫画风格：{comic_style}

【输出格式 - 请严格按照此JSON格式输出】
{{
  "title": "漫画标题",
  "theme": "主题",
  "style": "{comic_style}",
  "total_panels": {comic_panels},
  "plot_outline": "完整故事概要（2-3句话）",
  "panel_breakdown": [
    {{"panel_id": 1, "plot_point": "开场场景描述"}},
    {{"panel_id": 2, "plot_point": "发展..."}},
    ... 一共 {comic_panels} 个格子
  ]
}}

**重要：panel_breakdown 数组必须包含恰好 {comic_panels} 个元素，panel_id 从 1 到 {comic_panels}**

请直接返回JSON，不要包含其他文字说明。"""

    outline_text = call_llm(prompt, "生成漫画大纲")

    # 尝试解析 JSON
    try:
        # 清理可能的markdown代码块标记
        cleaned_text = outline_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        outline_data = json.loads(cleaned_text)
        outline_data["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return outline_data
    except json.JSONDecodeError:
        # 如果解析失败，返回默认结构（使用配置的格数）
        print("⚠️ LLM 返回格式不是有效 JSON，使用默认结构")
        return {
            "title": "未命名漫画",
            "theme": "冒险",
            "style": comic_style,
            "total_panels": comic_panels,
            "plot_outline": outline_text[:200],
            "panel_breakdown": [
                {"panel_id": i, "plot_point": f"第{i}格情节"}
                for i in range(1, comic_panels + 1)
            ],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }


def design_characters(comic_outline: Dict[str, Any], memory_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    设计角色形象

    Args:
        comic_outline: 漫画大纲
        memory_context: Memory 上下文

    Returns:
        角色列表
    """
    prompt = f"""你是一个专业的漫画角色设计师。请根据漫画大纲设计角色形象。

【漫画大纲】
标题: {comic_outline.get('title')}
主题: {comic_outline.get('theme')}
故事概要: {comic_outline.get('plot_outline')}

【要求】
- 为每个主要角色设计详细的外观描述
- 描述要具体，包含：发型、服装、体型、面部特征、配色
- 描述需适合用于 AI 图片生成（Stable Diffusion, DALL-E 等）
- 保持风格统一

【输出格式 - 请严格按照此JSON格式输出】
[
  {{
    "name": "角色名",
    "role": "主角",
    "appearance": "详细外观描述（用于文生图 prompt）",
    "personality": "性格特点",
    "visual_tags": ["标签1", "标签2"]
  }}
]

请直接返回JSON数组，不要包含其他文字说明。"""

    characters_text = call_llm(prompt, "设计角色形象")

    # 尝试解析 JSON
    try:
        cleaned_text = characters_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        characters = json.loads(cleaned_text)
        return characters
    except json.JSONDecodeError:
        print("⚠️ LLM 返回格式不是有效 JSON，使用默认角色")
        return [
            {
                "name": "主角",
                "role": "主角",
                "appearance": "年轻人，简单服装，友善表情",
                "personality": "勇敢、善良",
                "visual_tags": ["young", "casual_clothes", "friendly"]
            }
        ]


def generate_story_segments(
    comic_outline: Dict[str, Any],
    characters: List[Dict[str, Any]],
    memory_context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    生成分段故事文本

    Args:
        comic_outline: 漫画大纲
        characters: 角色列表
        memory_context: Memory 上下文

    Returns:
        分段文本列表
    """
    segments = []
    panel_breakdown = comic_outline.get("panel_breakdown", [])

    # 构建角色信息字符串
    char_info = "\n".join([
        f"- {c['name']} ({c['role']}): {c.get('appearance', '')}"
        for c in characters
    ])

    # 为每个格子生成详细文本
    for panel_data in panel_breakdown:
        panel_id = panel_data.get("panel_id")
        plot_point = panel_data.get("plot_point")

        prompt = f"""你是一个专业的漫画分镜师。请为这一格漫画生成详细文本。

【漫画信息】
标题: {comic_outline.get('title')}
总体情节: {comic_outline.get('plot_outline')}

【角色信息】
{char_info}

【当前格子】
格子ID: {panel_id}
情节点: {plot_point}

【要求】
- 生成这一格的详细场景描述
- 包含角色动作、对话、表情
- 描述要适合漫画表现（视觉化）
- 字数控制在 50-100 字

【输出格式 - 请严格按照此JSON格式输出】
{{
  "panel_id": {panel_id},
  "scene_description": "场景描述",
  "characters_in_scene": ["角色1", "角色2"],
  "dialogue": "对话内容（如果有）",
  "action": "动作描述",
  "emotion": "情绪氛围",
  "text": "完整文本描述（50-100字）"
}}

请直接返回JSON，不要包含其他文字说明。"""

        segment_text = call_llm(prompt, f"生成第{panel_id}格文本")

        # 尝试解析 JSON
        try:
            cleaned_text = segment_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()

            segment = json.loads(cleaned_text)
            segments.append(segment)
        except json.JSONDecodeError:
            print(f"⚠️ 第{panel_id}格文本解析失败，使用默认结构")
            segments.append({
                "panel_id": panel_id,
                "scene_description": plot_point,
                "characters_in_scene": [],
                "dialogue": "",
                "action": plot_point,
                "emotion": "中性",
                "text": segment_text[:100] if len(segment_text) > 100 else segment_text
            })

    return segments


def generate_image_prompts(
    segments: List[Dict[str, Any]],
    characters: List[Dict[str, Any]],
    comic_outline: Dict[str, Any],
    memory_context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    生成图片提示词

    Args:
        segments: 分段文本列表
        characters: 角色列表
        comic_outline: 漫画大纲
        memory_context: Memory 上下文

    Returns:
        图片提示词列表
    """
    prompts = []
    comic_style = comic_outline.get("style", "manga")

    # 构建角色外观字典
    char_appearances = {c["name"]: c.get("appearance", "") for c in characters}

    for segment in segments:
        panel_id = segment.get("panel_id")
        scene_desc = segment.get("scene_description", "")
        chars_in_scene = segment.get("characters_in_scene", [])
        action = segment.get("action", "")
        text = segment.get("text", "")

        # 构建角色外观描述（如果有角色在场景中）
        char_desc_parts = []
        for char_name in chars_in_scene:
            if char_name in char_appearances:
                char_desc_parts.append(f"{char_name}: {char_appearances[char_name]}")

        char_descriptions = ", ".join(char_desc_parts) if char_desc_parts else "no characters"

        prompt = f"""你是一个专业的 AI 绘画提示词工程师。请将漫画文本转换为文生图 prompt。

【漫画风格】
{comic_style}

【当前格子信息】
文本: {text}
场景: {scene_desc}
角色: {char_descriptions}
动作: {action}

【要求】
- 生成适合 Stable Diffusion / DALL-E 的英文 prompt
- 包含场景、角色、动作、光线、构图
- 如果有角色，必须包含该角色的详细外观描述（确保一致性）
- 指定漫画风格（manga style, comic style, etc.）
- 添加质量标签（high quality, detailed, etc.）

【输出格式 - 请严格按照此JSON格式输出】
{{
  "panel_id": {panel_id},
  "positive_prompt": "详细的正向提示词",
  "negative_prompt": "负向提示词（要避免的元素）",
  "style_tags": ["manga", "high_quality"]
}}

请直接返回JSON，不要包含其他文字说明。"""

        prompt_text = call_llm(prompt, f"生成第{panel_id}格提示词")

        # 尝试解析 JSON
        try:
            cleaned_text = prompt_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()

            prompt_data = json.loads(cleaned_text)
            prompts.append(prompt_data)
        except json.JSONDecodeError:
            print(f"⚠️ 第{panel_id}格提示词解析失败，使用简化prompt")
            # 构建简化的 prompt
            positive = f"{comic_style} style, {scene_desc}, {action}, {char_descriptions}, high quality, detailed"
            prompts.append({
                "panel_id": panel_id,
                "positive_prompt": positive,
                "negative_prompt": "blurry, low quality, distorted, bad anatomy",
                "style_tags": [comic_style, "high_quality"]
            })

    return prompts


def generate_images_from_prompts(
    prompts: List[Dict[str, Any]],
    memory_context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    从提示词生成图片（直接返回 URL，不下载）

    Args:
        prompts: 图片提示词列表
        memory_context: Memory 上下文

    Returns:
        生成的图片信息列表
    """
    config = get_config()
    images = []

    if config.use_mock_mode:
        # 模拟模式：返回模拟的图片 URL
        print("\n[模拟模式] 生成模拟图片 URL")
        for prompt_data in prompts:
            panel_id = prompt_data.get("panel_id")

            images.append({
                "panel_id": panel_id,
                "image_url": f"https://mock.example.com/comic_panel_{panel_id}.png",
                "prompt": prompt_data.get("positive_prompt", ""),
                "status": "mocked"
            })
            print(f"  ✓ [模拟] Panel {panel_id}: https://mock.example.com/comic_panel_{panel_id}.png")
    else:
        # 真实模式：调用图片生成 API，直接返回 URL
        image_client = get_image_client()

        for prompt_data in prompts:
            panel_id = prompt_data.get("panel_id")
            positive_prompt = prompt_data.get("positive_prompt", "")
            negative_prompt = prompt_data.get("negative_prompt", "")

            try:
                print(f"\n  🎨 生成 Panel {panel_id} 图片...")

                # 调用图片生成 API，获取 URL
                image_url = image_client.generate(
                    prompt=positive_prompt,
                    negative_prompt=negative_prompt
                )

                images.append({
                    "panel_id": panel_id,
                    "image_url": image_url,
                    "prompt": positive_prompt,
                    "status": "generated"
                })

                print(f"  ✓ Panel {panel_id}: {image_url}")

            except Exception as e:
                print(f"  ✗ Panel {panel_id} 生成失败: {e}")
                images.append({
                    "panel_id": panel_id,
                    "image_url": "",
                    "prompt": positive_prompt,
                    "status": "failed",
                    "error": str(e)
                })

    return images


def download_image(url: str, save_path: str) -> None:
    """
    下载图片到本地

    Args:
        url: 图片 URL
        save_path: 保存路径
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"  ⚠️ 下载图片失败: {e}")
        raise


def list_available_tools() -> List[str]:
    """列出所有可用的工具"""
    return [
        "generate_comic_outline - 生成漫画大纲",
        "design_characters - 设计角色形象",
        "generate_story_segments - 生成分段故事文本",
        "generate_image_prompts - 生成图片提示词",
        "generate_images_from_prompts - 文生图"
    ]
