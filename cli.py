"""
CLI 交互模块
提供命令行界面与用户交互
"""

import sys
from typing import Optional
from memory import MemorySystem
from agent_core import StoryCreationAgent


class StoryBookCLI:
    """命令行交互界面"""

    def __init__(self):
        self.memory: Optional[MemorySystem] = None
        self.agent: Optional[StoryCreationAgent] = None
        self.current_project: Optional[str] = None

    def print_banner(self):
        """打印欢迎横幅"""
        banner = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              📚 StoryBook 创作型 Agent                      ║
║                                                            ║
║        基于 LangGraph + Memory 的智能创作助手               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_menu(self):
        """打印主菜单"""
        menu = """
【主菜单】
1. 创建新项目
2. 加载已有项目
3. 查看 Memory 摘要
4. 查看工作流程
5. 退出

请选择操作 (1-5): """
        return input(menu).strip()

    def create_new_project(self):
        """创建新项目"""
        print("\n" + "=" * 60)
        print("📝 创建新项目")
        print("=" * 60)

        # 获取项目信息
        project_name = input("\n请输入项目名称: ").strip()
        if not project_name:
            print("✗ 项目名称不能为空")
            return

        story_idea = input("请输入故事创意（可以是主题、设定或简单描述）: ").strip()
        if not story_idea:
            print("✗ 故事创意不能为空")
            return

        # 可选设置
        print("\n【可选设置】(直接回车使用默认值)")
        story_style = input("故事风格 [默认: 现代]: ").strip() or "现代"
        target_audience = input("目标受众 [默认: 全年龄]: ").strip() or "全年龄"
        story_length = input("故事长度 [默认: 中篇]: ").strip() or "中篇"

        # 初始化 Memory 和 Agent
        self.memory = MemorySystem(project_name)
        self.memory.profile.update_settings({
            "story_style": story_style,
            "target_audience": target_audience,
            "story_length": story_length
        })

        self.agent = StoryCreationAgent(self.memory)
        self.current_project = project_name

        # 确认开始
        print(f"\n✓ 项目 '{project_name}' 已初始化")
        confirm = input("\n是否开始创作流程？(y/n): ").strip().lower()

        if confirm == 'y':
            self.run_creation_workflow(story_idea)
        else:
            print("✓ 项目已保存，您可以稍后继续")
            self.memory.save_to_disk()

    def run_creation_workflow(self, user_input: str):
        """运行创作工作流"""
        if not self.agent or not self.current_project:
            print("✗ 请先创建或加载项目")
            return

        print("\n" + "=" * 60)
        print("🚀 开始创作工作流")
        print("=" * 60)

        try:
            # 运行 Agent
            final_state = self.agent.run(self.current_project, user_input)

            # 显示结果摘要
            self.show_creation_summary(final_state)

        except Exception as e:
            print(f"\n✗ 创作过程出错: {str(e)}")
            import traceback
            traceback.print_exc()

    def show_creation_summary(self, state):
        """显示创作结果摘要"""
        print("\n" + "=" * 60)
        print("📊 创作结果摘要")
        print("=" * 60)

        # 故事大纲
        outline = state.get("story_outline", {})
        if outline:
            print(f"\n【故事大纲】")
            print(f"标题: {outline.get('title')}")
            print(f"类型: {outline.get('genre')}")
            print(f"幕数: {outline.get('acts')}")

        # 角色设计
        ip_design = state.get("ip_design", {})
        if ip_design:
            print(f"\n【角色设计】")
            characters = ip_design.get("characters", [])
            for char in characters:
                print(f"- {char.get('name')} ({char.get('role')}): {char.get('description')}")

        # 分镜
        storyboards = state.get("storyboards", [])
        if storyboards:
            print(f"\n【分镜脚本】")
            for sb in storyboards:
                print(f"- 场景: {sb.get('scene_name')}")
                print(f"  分镜数: {len(sb.get('panels', []))} 个")
                print(f"  总时长: {sb.get('total_duration')} 秒")

        # 镜头
        shots = state.get("shots", [])
        if shots:
            print(f"\n【镜头设计】")
            print(f"总镜头数: {len(shots)} 个")
            for shot in shots[:3]:  # 只显示前3个
                print(f"- {shot.get('shot_id')}: {shot.get('shot_type')}")

        # 完成步骤
        completed_steps = state.get("completed_steps", [])
        print(f"\n【完成步骤】")
        print(f"✓ 共完成 {len(completed_steps)} 个步骤")
        for step in completed_steps:
            print(f"  - {step}")

    def load_existing_project(self):
        """加载已有项目"""
        print("\n" + "=" * 60)
        print("📂 加载已有项目")
        print("=" * 60)

        # 列出可用的项目文件
        import os
        storage_path = "memory_storage"

        if not os.path.exists(storage_path):
            print("\n✗ 没有找到已保存的项目")
            return

        files = [f for f in os.listdir(storage_path) if f.endswith('.json')]

        if not files:
            print("\n✗ 没有找到已保存的项目")
            return

        print("\n可用项目:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")

        try:
            choice = int(input("\n请选择项目编号: ").strip())
            if 1 <= choice <= len(files):
                filename = files[choice - 1]

                # 创建 Memory 系统并加载
                project_name = filename.replace('.json', '')
                self.memory = MemorySystem(project_name)
                self.memory.load_from_disk(filename)

                self.agent = StoryCreationAgent(self.memory)
                self.current_project = project_name

                print(f"\n✓ 项目 '{project_name}' 已加载")
                self.show_memory_summary()
            else:
                print("✗ 无效的选择")
        except ValueError:
            print("✗ 请输入有效的数字")

    def show_memory_summary(self):
        """显示 Memory 摘要"""
        if not self.memory:
            print("\n✗ 没有活动的项目")
            return

        print("\n" + self.memory.get_summary())

    def show_workflow_info(self):
        """显示工作流信息"""
        if not self.agent:
            # 创建临时 agent 只为显示信息
            temp_memory = MemorySystem("temp")
            temp_agent = StoryCreationAgent(temp_memory)
            print("\n" + temp_agent.get_workflow_summary())
        else:
            print("\n" + self.agent.get_workflow_summary())

    def run(self):
        """运行 CLI 主循环"""
        self.print_banner()

        while True:
            try:
                choice = self.print_menu()

                if choice == '1':
                    self.create_new_project()
                elif choice == '2':
                    self.load_existing_project()
                elif choice == '3':
                    self.show_memory_summary()
                elif choice == '4':
                    self.show_workflow_info()
                elif choice == '5':
                    print("\n👋 感谢使用 StoryBook！再见！")
                    sys.exit(0)
                else:
                    print("\n✗ 无效的选择，请输入 1-5")

            except KeyboardInterrupt:
                print("\n\n👋 感谢使用 StoryBook！再见！")
                sys.exit(0)
            except Exception as e:
                print(f"\n✗ 发生错误: {str(e)}")
                import traceback
                traceback.print_exc()


def main():
    """CLI 主入口"""
    cli = StoryBookCLI()
    cli.run()


if __name__ == "__main__":
    main()
