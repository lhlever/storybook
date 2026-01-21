#!/usr/bin/env python3
"""
简单测试脚本 - 直接运行漫画生成 Agent
用法: python3 test_agent.py "你的漫画创意"
"""

import sys
from memory import MemorySystem
from agent_core import StoryCreationAgent


def test_agent(comic_idea: str):
    """
    测试漫画生成 Agent

    Args:
        comic_idea: 用户输入的漫画创意（一句话）
    """
    print("=" * 70)
    print("🎨 测试漫画生成 Agent")
    print("=" * 70)
    print(f"\n📝 漫画创意: {comic_idea}")
    print("\n" + "-" * 70)

    # 创建项目
    project_name = "测试漫画"

    # 初始化 Memory
    memory = MemorySystem(project_name)
    memory.profile.update_settings({
        "project_type": "comic",
        "comic_style": "manga"
    })

    # 创建 Agent
    agent = StoryCreationAgent(memory)

    # 运行流程
    print("\n🚀 开始运行 Agent...\n")
    result = agent.run(project_name, comic_idea)

    # 输出结果
    print("\n" + "=" * 70)
    print("✅ 运行完成！以下是生成结果：")
    print("=" * 70)

    print(f"\n📊 生成了 {len(result)} 格漫画\n")

    # 显示每一格的内容
    for i, item in enumerate(result, 1):
        word = item.get("word", "无文本")
        url = item.get("url", "无URL")

        print(f"【第 {i} 格】")
        print(f"  文本: {word}")
        print(f"  图片: {url}")
        print()

    # 保存结果到 JSON 文件
    import json
    output_file = f"output/{project_name}_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"💾 结果已保存到: {output_file}")

    print("\n" + "=" * 70)
    print("🎉 测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法:")
        print('  python3 test_agent.py "你的漫画创意"')
        print("\n示例:")
        print('  python3 test_agent.py "一只会魔法的小猫咪在森林里冒险"')
        print('  python3 test_agent.py "机器人学习人类情感"')
        print('  python3 test_agent.py "少年发现了时间旅行的秘密"')
        sys.exit(1)

    # 获取用户输入的创意
    comic_idea = sys.argv[1]

    # 运行测试
    test_agent(comic_idea)
