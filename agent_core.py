"""
LangGraph Agent 核心模块
实现基于状态图的创作流程
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
import operator
from memory import MemorySystem
from tools import (
    generate_frames_from_llm,
    design_characters,
    generate_images_from_prompts
)


class AgentState(TypedDict):
    """
    Agent 的状态定义 - 漫画生成流程（使用 LLM_conversion）
    使用 TypedDict 确保类型安全
    """
    # 基础信息
    project_name: str
    user_input: str

    # 流程状态
    current_step: str
    completed_steps: Annotated[list, operator.add]

    # 创作内容（漫画）- 新流程
    character_settings: str    # 角色设定（从LLM返回）
    main_story: str            # 故事概要（从LLM返回）
    characters: list           # 角色设计列表（详细设计）
    story_segments: list       # 分段故事文本（9帧）
    image_prompts: list        # 图片提示词列表（9帧）
    images: list               # 生成的图片列表（9帧）

    # 控制流
    next_action: str
    error_message: str


class StoryCreationAgent:
    """创作型 Agent - 使用 LangGraph 管理工作流"""

    def __init__(self, memory_system: MemorySystem):
        self.memory = memory_system
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """构建 LangGraph 状态图 - 新漫画生成流程（使用 LLM_conversion）"""

        # 创建状态图
        workflow = StateGraph(AgentState)

        # 添加节点（新流程：LLM生成 → 角色设计 → 文生图）
        workflow.add_node("init", self.initialize_node)
        workflow.add_node("generate_frames", self.generate_frames_node)
        workflow.add_node("design_characters", self.design_characters_node)
        workflow.add_node("generate_images", self.generate_images_node)
        workflow.add_node("finalize", self.finalize_node)

        # 设置入口点
        workflow.set_entry_point("init")

        # 添加边（定义新流程）
        workflow.add_edge("init", "generate_frames")
        workflow.add_edge("generate_frames", "design_characters")
        workflow.add_edge("design_characters", "generate_images")
        workflow.add_edge("generate_images", "finalize")
        workflow.add_edge("finalize", END)

        # 编译图
        return workflow.compile()

    def initialize_node(self, state: AgentState) -> AgentState:
        """初始化节点 - 准备工作环境"""
        print("\n" + "=" * 50)
        print("🚀 初始化漫画创作流程（新流程：LLM → 角色设计 → 文生图）")
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
            "project_type": "storybook",
            "total_frames": 9
        })

        state["current_step"] = "初始化完成"
        state["completed_steps"] = ["init"]
        return state

    def generate_frames_node(self, state: AgentState) -> AgentState:
        """使用 LLM_conversion 生成 9 帧漫画文本和提示词节点"""
        print("\n📝 Step 1: 使用 LLM 生成 9 帧漫画（文本+提示词）")
        print("-" * 50)

        try:
            memory_context = {
                "project_name": state["project_name"]
            }

            # 调用 LLM_conversion 工具
            result = generate_frames_from_llm(state["user_input"], memory_context)

            # 更新状态
            state["character_settings"] = result.get("character_settings", "")
            state["main_story"] = result.get("main_story", "")
            state["story_segments"] = result.get("segments", [])
            state["image_prompts"] = result.get("prompts", [])
            state["current_step"] = "9帧漫画内容已生成"
            state["completed_steps"] = state.get("completed_steps", []) + ["generate_frames"]

            # 保存到 Semantic Memory
            self.memory.semantic.update_knowledge("character_settings", result.get("character_settings"))
            self.memory.semantic.update_knowledge("main_story", result.get("main_story"))
            self.memory.semantic.update_knowledge("story_segments", result.get("segments"))
            self.memory.semantic.update_knowledge("image_prompts", result.get("prompts"))

            # 记录到 Episodic Memory
            self.memory.episodic.add_episode(
                "frames_generated",
                result,
                {"total_frames": result.get("total_frames", 9)}
            )

            print(f"✓ 角色设定: {result.get('character_settings', '')[:60]}...")
            print(f"✓ 故事概要: {result.get('main_story', '')[:60]}...")
            print(f"✓ 生成帧数: {len(result.get('segments', []))}")

        except Exception as e:
            state["error_message"] = f"生成帧内容失败: {str(e)}"
            print(f"✗ 错误: {state['error_message']}")

        return state

    def design_characters_node(self, state: AgentState) -> AgentState:
        """设计角色详细形象节点（基于 LLM 返回的角色设定）"""
        print("\n🎭 Step 2: 设计角色详细形象")
        print("-" * 50)

        try:
            character_settings = state.get("character_settings", "")
            main_story = state.get("main_story", "")

            if not character_settings:
                print("⚠️ 没有角色设定，跳过角色设计")
                state["characters"] = []
                state["current_step"] = "角色设计已跳过"
                state["completed_steps"] = state.get("completed_steps", []) + ["design_characters"]
                return state

            memory_context = {
                "project_name": state["project_name"]
            }

            # 构建简化的大纲数据（用于 design_characters 函数）
            outline = {
                "title": state["project_name"],
                "theme": "温馨故事",
                "plot_outline": main_story,
                "character_settings": character_settings
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

    def generate_images_node(self, state: AgentState) -> AgentState:
        """生成漫画图片节点"""
        print("\n🖼️  Step 3: 生成漫画图片（9帧）")
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
        print("\n✅ Step 4: 完成漫画创作流程")
        print("-" * 50)

        # 更新 Working Memory
        self.memory.working.set("workflow_status", "completed")
        self.memory.working.set("total_steps", len(state.get("completed_steps", [])))

        # 记录到 Episodic Memory
        self.memory.episodic.add_episode(
            "workflow_completed",
            {
                "completed_steps": state.get("completed_steps", []),
                "main_story": state.get("main_story", ""),
                "total_frames": len(state.get("story_segments", [])),
                "total_images": len(state.get("images", []))
            }
        )

        # 保存 Memory 到磁盘
        self.memory.save_to_disk()

        state["current_step"] = "全部完成"
        state["completed_steps"] = state.get("completed_steps", []) + ["finalize"]

        print(f"✓ 项目已保存到: memory_storage/{state['project_name']}.json")
        print(f"✓ 完成步骤: {len(state.get('completed_steps', []))}")
        print(f"✓ 生成帧数: {len(state.get('story_segments', []))}")
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
            "character_settings": "",
            "main_story": "",
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
漫画创作流程节点（新版本 - 使用 LLM_conversion）：
1. init - 初始化
2. generate_frames - 使用LLM生成9帧文本+提示词（一次性）
3. design_characters - 设计角色详细形象
4. generate_images - 生成漫画图片（9帧）
5. finalize - 完成并保存
        """.strip()
