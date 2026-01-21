"""
主入口文件
提供快速启动和示例演示
"""

import sys
from cli import StoryBookCLI


def run_demo():
    """运行演示模式 - 自动创建漫画示例项目"""
    print("\n" + "=" * 60)
    print("🎨 演示模式：自动创建漫画示例项目")
    print("=" * 60)

    from memory import MemorySystem
    from agent_core import StoryCreationAgent

    # 创建示例项目
    project_name = "冒险小猫_漫画"
    comic_idea = "一只勇敢的小猫在城市中寻找失踪的主人，途中遇到各种有趣的动物朋友"

    print(f"\n项目名称: {project_name}")
    print(f"漫画创意: {comic_idea}")

    # 初始化
    memory = MemorySystem(project_name)
    memory.profile.update_settings({
        "project_type": "comic",
        "comic_style": "manga",
        "target_audience": "children",
        "total_panels": 6
    })

    agent = StoryCreationAgent(memory)

    # 运行漫画创作流程
    print("\n开始自动创作漫画...")
    final_state = agent.run(project_name, comic_idea)

    # 显示摘要
    print("\n" + "=" * 60)
    print("📊 演示完成！以下是漫画创作成果摘要：")
    print("=" * 60)

    print(f"\n✓ 漫画标题: {final_state['comic_outline'].get('title')}")
    print(f"✓ 漫画风格: {final_state['comic_outline'].get('style')}")
    print(f"✓ 角色数量: {len(final_state['characters'])}")
    print(f"✓ 漫画格数: {len(final_state['story_segments'])}")
    print(f"✓ 图片数量: {len(final_state['images'])}")

    # 显示生成的图片路径
    if final_state['images']:
        print("\n生成的图片:")
        for img in final_state['images']:
            status_icon = "✓" if img.get("status") in ["generated", "mocked"] else "✗"
            print(f"  {status_icon} Panel {img.get('panel_id')}: {img.get('image_path')}")

    print("\n" + memory.get_summary())

    print("\n提示: 项目已保存到 memory_storage/ 目录，图片已保存到 output/ 目录")


def run_interactive():
    """运行交互式 CLI 模式"""
    cli = StoryBookCLI()
    cli.run()


def print_usage():
    """打印使用说明"""
    usage = """
使用方法:
    python main.py          # 启动交互式 CLI
    python main.py --demo   # 运行演示模式（自动创建示例项目）
    python main.py --help   # 显示此帮助信息

项目结构:
    agent_core.py   - LangGraph Agent 核心（漫画生成流程）
    memory.py       - Memory 系统（Working/Episodic/Semantic/Profile）
    tools.py        - 创作工具（大纲/角色/分段文本/提示词/文生图）
    cli.py          - CLI 交互界面
    main.py         - 主入口

功能特性:
    ✓ LangGraph 状态图管理漫画创作流程
    ✓ 四种 Memory 类型协同工作
    ✓ 自动生成分段故事文本
    ✓ AI 文生图（支持多种API）
    ✓ 角色一致性保证
    ✓ JSON 持久化存储
    """
    print(usage)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--demo":
            run_demo()
        elif arg == "--help" or arg == "-h":
            print_usage()
        else:
            print(f"未知参数: {arg}")
            print_usage()
    else:
        # 默认启动交互式 CLI
        run_interactive()


if __name__ == "__main__":
    main()
