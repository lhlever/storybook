"""
LangGraph Agent 核心模块
实现基于状态图的创作流程
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
import operator
from memory import MemorySystem
from tools import (
    generate_comic_outline,
    design_characters,
    generate_story_segments,
    generate_image_prompts,
    generate_images_from_prompts
)


class AgentState(TypedDict):
    """
    Agent 的状态定义 - 漫画生成流程
    使用 TypedDict 确保类型安全
    """
    # 基础信息
    project_name: str
    user_input: str

    # 流程状态
    current_step: str
    completed_steps: Annotated[list, operator.add]

    # 创作内容（漫画）
    comic_outline: dict        # 漫画大纲
    characters: list           # 角色设计列表
    story_segments: list       # 分段故事文本
    image_prompts: list        # 图片提示词列表
    images: list               # 生成的图片列表

    # 控制流
    next_action: str
    error_message: str


class StoryCreationAgent:
    """创作型 Agent - 使用 LangGraph 管理工作流"""

    def __init__(self, memory_system: MemorySystem):
        self.memory = memory_system
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """构建 LangGraph 状态图 - 漫画生成流程"""

        # 创建状态图
        workflow = StateGraph(AgentState)

        # 添加节点（漫画生成流程）
        workflow.add_node("init", self.initialize_node)
        workflow.add_node("generate_comic_outline", self.generate_comic_outline_node)
        workflow.add_node("design_characters", self.design_characters_node)
        workflow.add_node("generate_story_segments", self.generate_story_segments_node)
        workflow.add_node("generate_image_prompts", self.generate_image_prompts_node)
        workflow.add_node("generate_images", self.generate_images_node)
        workflow.add_node("finalize", self.finalize_node)

        # 设置入口点
        workflow.set_entry_point("init")

        # 添加边（定义流程）
        workflow.add_edge("init", "generate_comic_outline")
        workflow.add_edge("generate_comic_outline", "design_characters")
        workflow.add_edge("design_characters", "generate_story_segments")
        workflow.add_edge("generate_story_segments", "generate_image_prompts")
        workflow.add_edge("generate_image_prompts", "generate_images")
        workflow.add_edge("generate_images", "finalize")
        workflow.add_edge("finalize", END)

        # 编译图
        return workflow.compile()

    def initialize_node(self, state: AgentState) -> AgentState:
        """初始化节点 - 准备工作环境"""
        print("\n" + "=" * 50)
        print("🚀 初始化漫画创作流程")
        print("=" * 50)

        # 记录到 Episodic Memory
        self.memory.episodic.add_episode(
            "workflow_start",
            f"开始创作漫画项目: {state['project_name']}",
            {"user_input": state["user_input"]}
        )

        # 设置 Working Memory
        self.memory.working.set("current_project", state["project_name"])
        self.memory.working.set("workflow_status", "initialized")

        # 设置 Profile Memory（项目偏好）
        self.memory.profile.update_settings({
            "project_type": "comic",
            "comic_style": "manga"
        })

        state["current_step"] = "初始化完成"
        state["completed_steps"] = ["init"]
        return state

    def generate_comic_outline_node(self, state: AgentState) -> AgentState:
        """生成漫画大纲节点"""
        print("\n📝 Step 1: 生成漫画大纲")
        print("-" * 50)

        try:
            # 从 Profile Memory 获取设置
            settings = self.memory.profile.get_profile("settings")
            memory_context = {
                "settings": settings,
                "project_name": state["project_name"]
            }

            # 调用工具生成漫画大纲
            outline = generate_comic_outline(state["user_input"], memory_context)

            # 更新状态
            state["comic_outline"] = outline
            state["current_step"] = "漫画大纲已生成"
            state["completed_steps"] = state.get("completed_steps", []) + ["generate_comic_outline"]

            # 保存到 Semantic Memory
            self.memory.semantic.update_knowledge("comic_outline", outline)

            # 记录到 Episodic Memory
            self.memory.episodic.add_episode(
                "outline_created",
                outline,
                {"title": outline.get("title"), "total_panels": outline.get("total_panels")}
            )

            print(f"✓ 漫画标题: {outline.get('title')}")
            print(f"✓ 漫画风格: {outline.get('style')}")
            print(f"✓ 预计格数: {outline.get('total_panels')}")

        except Exception as e:
            state["error_message"] = f"生成大纲失败: {str(e)}"
            print(f"✗ 错误: {state['error_message']}")

        return state

    def design_characters_node(self, state: AgentState) -> AgentState:
        """设计角色形象节点"""
        print("\n🎭 Step 2: 设计角色形象")
        print("-" * 50)

        try:
            outline = state.get("comic_outline")
            if not outline:
                raise ValueError("缺少漫画大纲")

            memory_context = {
                "project_name": state["project_name"]
            }

            # 调用工具设计角色
            characters = design_characters(outline, memory_context)

            # 更新状态
            state["characters"] = characters
            state["current_step"] = "角色形象已设计"
            state["completed_steps"] = state.get("completed_steps", []) + ["design_characters"]

            # 保存到 Semantic Memory
            self.memory.semantic.update_knowledge("characters", characters)

            # 记录到 Episodic Memory
            self.memory.episodic.add_episode(
                "characters_designed",
                characters,
                {"character_count": len(characters)}
            )

            print(f"✓ 角色数量: {len(characters)}")
            for char in characters:
                print(f"  - {char.get('name')}: {char.get('role')}")

        except Exception as e:
            state["error_message"] = f"设计角色失败: {str(e)}"
            print(f"✗ 错误: {state['error_message']}")

        return state

    def generate_story_segments_node(self, state: AgentState) -> AgentState:
        """生成分段故事文本节点"""
        print("\n📖 Step 3: 生成分段故事文本")
        print("-" * 50)

        try:
            outline = state.get("comic_outline")
            characters = state.get("characters")

            if not outline or not characters:
                raise ValueError("缺少必要的前置内容")

            memory_context = {
                "project_name": state["project_name"]
            }

            # 调用工具生成分段文本
            segments = generate_story_segments(outline, characters, memory_context)

            # 更新状态
            state["story_segments"] = segments
            state["current_step"] = "分段故事文本已生成"
            state["completed_steps"] = state.get("completed_steps", []) + ["generate_story_segments"]

            # 保存到 Semantic Memory
            self.memory.semantic.update_knowledge("story_segments", segments)

            # 记录到 Episodic Memory
            self.memory.episodic.add_episode(
                "segments_generated",
                segments,
                {"segment_count": len(segments)}
            )

            print(f"✓ 生成文本段数: {len(segments)}")
            for i, seg in enumerate(segments, 1):
                print(f"  [{i}] {seg.get('text', '')[:50]}...")

        except Exception as e:
            state["error_message"] = f"生成文本失败: {str(e)}"
            print(f"✗ 错误: {state['error_message']}")

        return state

    def generate_image_prompts_node(self, state: AgentState) -> AgentState:
        """生成图片提示词节点"""
        print("\n🎨 Step 4: 生成图片提示词")
        print("-" * 50)

        try:
            segments = state.get("story_segments", [])
            characters = state.get("characters", [])
            outline = state.get("comic_outline", {})

            if not segments:
                raise ValueError("缺少故事文本段")

            memory_context = {
                "project_name": state["project_name"],
                "comic_style": outline.get("style", "manga")
            }

            # 调用工具生成图片提示词
            prompts = generate_image_prompts(segments, characters, outline, memory_context)

            # 更新状态
            state["image_prompts"] = prompts
            state["current_step"] = "图片提示词已生成"
            state["completed_steps"] = state.get("completed_steps", []) + ["generate_image_prompts"]

            # 保存到 Semantic Memory
            self.memory.semantic.update_knowledge("image_prompts", prompts)

            # 记录到 Episodic Memory
            self.memory.episodic.add_episode(
                "prompts_generated",
                prompts,
                {"prompt_count": len(prompts)}
            )

            print(f"✓ 生成提示词数量: {len(prompts)}")
            for i, prompt_data in enumerate(prompts, 1):
                print(f"  [{i}] Panel {prompt_data.get('panel_id')}: {prompt_data.get('positive_prompt', '')[:60]}...")

        except Exception as e:
            state["error_message"] = f"生成提示词失败: {str(e)}"
            print(f"✗ 错误: {state['error_message']}")

        return state

    def generate_images_node(self, state: AgentState) -> AgentState:
        """生成漫画图片节点"""
        print("\n🖼️  Step 5: 生成漫画图片")
        print("-" * 50)

        try:
            prompts = state.get("image_prompts", [])
            if not prompts:
                raise ValueError("缺少图片提示词")

            memory_context = {
                "project_name": state["project_name"]
            }

            # 调用工具生成图片
            images = generate_images_from_prompts(prompts, memory_context)

            # 更新状态
            state["images"] = images
            state["current_step"] = "漫画图片已生成"
            state["completed_steps"] = state.get("completed_steps", []) + ["generate_images"]

            # 保存到 Semantic Memory
            self.memory.semantic.update_knowledge("images", images)

            # 记录到 Episodic Memory
            for img in images:
                self.memory.episodic.add_episode(
                    "image_generated",
                    img,
                    {"panel_id": img.get("panel_id")}
                )

            print(f"✓ 生成图片数量: {len(images)}")
            for img in images:
                print(f"  - Panel {img.get('panel_id')}: {img.get('image_path')}")

        except Exception as e:
            state["error_message"] = f"生成图片失败: {str(e)}"
            print(f"✗ 错误: {state['error_message']}")

        return state

    def finalize_node(self, state: AgentState) -> AgentState:
        """完成节点 - 整理和保存结果"""
        print("\n✅ Step 6: 完成漫画创作流程")
        print("-" * 50)

        # 更新 Working Memory
        self.memory.working.set("workflow_status", "completed")
        self.memory.working.set("total_steps", len(state.get("completed_steps", [])))

        # 记录到 Episodic Memory
        self.memory.episodic.add_episode(
            "workflow_completed",
            {
                "completed_steps": state.get("completed_steps", []),
                "comic_title": state.get("comic_outline", {}).get("title"),
                "total_panels": len(state.get("story_segments", [])),
                "total_images": len(state.get("images", []))
            }
        )

        # 保存 Memory 到磁盘
        self.memory.save_to_disk()

        state["current_step"] = "全部完成"
        state["completed_steps"] = state.get("completed_steps", []) + ["finalize"]

        print(f"✓ 项目已保存到: memory_storage/{state['project_name']}.json")
        print(f"✓ 完成步骤: {len(state.get('completed_steps', []))}")
        print(f"✓ 生成格数: {len(state.get('story_segments', []))}")
        print(f"✓ 生成图片: {len(state.get('images', []))}")

        return state

    def run(self, project_name: str, user_input: str):
        """
        运行漫画生成 Agent 工作流

        Args:
            project_name: 项目名称
            user_input: 用户输入的漫画创意

        Returns:
            格式化的结果列表：[{"word": "文本", "url": "图片URL"}, ...]
        """
        # 初始化状态
        initial_state: AgentState = {
            "project_name": project_name,
            "user_input": user_input,
            "current_step": "starting",
            "completed_steps": [],
            "comic_outline": {},
            "characters": [],
            "story_segments": [],
            "image_prompts": [],
            "images": [],
            "next_action": "continue",
            "error_message": ""
        }

        # 执行工作流
        final_state = self.graph.invoke(initial_state)

        # 格式化返回结果
        result = self._format_result(final_state)

        return result

    def _format_result(self, state: AgentState) -> list:
        """
        格式化最终结果为简洁的列表格式

        Args:
            state: Agent 最终状态

        Returns:
            [{"word": "文本", "url": "图片URL"}, ...]
        """
        segments = state.get("story_segments", [])
        images = state.get("images", [])

        # 创建 panel_id 到图片的映射
        image_map = {img.get("panel_id"): img for img in images}

        # 构建结果列表
        result = []
        for segment in segments:
            panel_id = segment.get("panel_id")
            text = segment.get("text", "")

            # 获取对应的图片
            img = image_map.get(panel_id, {})
            image_url = img.get("image_url", "")

            result.append({
                "word": text,
                "url": image_url
            })

        return result

    def get_workflow_summary(self) -> str:
        """获取工作流摘要"""
        return """
漫画创作流程节点：
1. init - 初始化
2. generate_comic_outline - 生成漫画大纲
3. design_characters - 设计角色形象
4. generate_story_segments - 生成分段故事文本
5. generate_image_prompts - 生成图片提示词
6. generate_images - 生成漫画图片
7. finalize - 完成并保存
        """.strip()
