"""
API 配置向导
帮助用户快速配置 API
"""

import os
import sys


def create_env_file():
    """交互式创建 .env 配置文件"""

    print("\n" + "=" * 60)
    print("🔧 API 配置向导")
    print("=" * 60)

    # 选择提供商
    print("\n请选择 LLM 提供商:")
    print("1. Anthropic Claude（推荐）")
    print("2. OpenAI GPT")
    print("3. 阿里云通义千问")
    print("4. 自定义（兼容 OpenAI 的服务）")

    choice = input("\n请选择 [1-4]: ").strip()

    config_lines = []

    # 是否使用模拟模式
    use_mock = input("\n是否使用模拟模式（测试用，无需 API Key）？[y/N]: ").strip().lower()
    if use_mock == 'y':
        config_lines.append("# 使用模拟模式")
        config_lines.append("USE_MOCK_MODE=true")
        config_lines.append("")
    else:
        config_lines.append("# 使用真实 API")
        config_lines.append("USE_MOCK_MODE=false")
        config_lines.append("")

    if choice == '1':
        # Anthropic Claude
        print("\n" + "-" * 60)
        print("配置 Anthropic Claude")
        print("-" * 60)
        print("获取 API Key: https://console.anthropic.com/")

        api_key = input("请输入 API Key: ").strip()
        model = input("请输入模型名称 [claude-opus-4-5-20251101]: ").strip() or "claude-opus-4-5-20251101"
        base_url = input("请输入 Base URL [https://api.anthropic.com]: ").strip() or "https://api.anthropic.com"

        config_lines.extend([
            "# Anthropic Claude 配置",
            "LLM_PROVIDER=anthropic",
            f"ANTHROPIC_API_KEY={api_key}",
            f"ANTHROPIC_BASE_URL={base_url}",
            f"ANTHROPIC_MODEL={model}",
        ])

    elif choice == '2':
        # OpenAI
        print("\n" + "-" * 60)
        print("配置 OpenAI GPT")
        print("-" * 60)
        print("获取 API Key: https://platform.openai.com/")

        api_key = input("请输入 API Key: ").strip()
        model = input("请输入模型名称 [gpt-4]: ").strip() or "gpt-4"
        base_url = input("请输入 Base URL [https://api.openai.com/v1]: ").strip() or "https://api.openai.com/v1"

        config_lines.extend([
            "# OpenAI GPT 配置",
            "LLM_PROVIDER=openai",
            f"OPENAI_API_KEY={api_key}",
            f"OPENAI_BASE_URL={base_url}",
            f"OPENAI_MODEL={model}",
        ])

    elif choice == '3':
        # 阿里云通义千问
        print("\n" + "-" * 60)
        print("配置阿里云通义千问")
        print("-" * 60)
        print("获取 API Key: https://dashscope.aliyun.com/")

        api_key = input("请输入 API Key: ").strip()
        model = input("请输入模型名称 [qwen-max]: ").strip() or "qwen-max"
        base_url = input("请输入 Base URL [https://dashscope.aliyuncs.com/api/v1]: ").strip() or "https://dashscope.aliyuncs.com/api/v1"

        config_lines.extend([
            "# 阿里云通义千问配置",
            "LLM_PROVIDER=dashscope",
            f"DASHSCOPE_API_KEY={api_key}",
            f"DASHSCOPE_BASE_URL={base_url}",
            f"DASHSCOPE_MODEL={model}",
        ])

    elif choice == '4':
        # 自定义服务
        print("\n" + "-" * 60)
        print("配置自定义服务（兼容 OpenAI API）")
        print("-" * 60)
        print("例如：vLLM, Ollama, FastChat 等")

        api_key = input("请输入 API Key（可选）: ").strip() or "not-needed"
        base_url = input("请输入 Base URL: ").strip()
        model = input("请输入模型名称: ").strip()

        config_lines.extend([
            "# 自定义服务配置",
            "LLM_PROVIDER=openai",
            f"OPENAI_API_KEY={api_key}",
            f"OPENAI_BASE_URL={base_url}",
            f"OPENAI_MODEL={model}",
        ])

    else:
        print("无效的选择")
        return False

    # 添加通用配置
    config_lines.extend([
        "",
        "# 生成参数",
        "LLM_TEMPERATURE=0.7",
        "LLM_MAX_TOKENS=2048",
        "",
        "# 其他配置",
        "API_TIMEOUT=60",
        "LOG_LEVEL=INFO",
    ])

    # 预览配置
    print("\n" + "=" * 60)
    print("配置预览:")
    print("=" * 60)
    for line in config_lines:
        if line and not line.startswith('#'):
            # 隐藏 API Key
            if 'API_KEY' in line or 'TOKEN' in line:
                key, value = line.split('=', 1)
                if value and value != 'not-needed':
                    print(f"{key}={value[:10]}...")
                else:
                    print(line)
            else:
                print(line)
        else:
            print(line)

    # 确认保存
    print("\n" + "=" * 60)
    confirm = input("是否保存到 .env 文件？[Y/n]: ").strip().lower()

    if confirm in ['', 'y', 'yes']:
        # 保存文件
        with open('.env', 'w', encoding='utf-8') as f:
            f.write('\n'.join(config_lines))
            f.write('\n')

        print("\n✅ 配置已保存到 .env 文件")
        print("\n下一步:")
        print("  1. 运行 'python3 test_real_api.py check' 检查配置")
        print("  2. 运行 'python3 test_real_api.py quick' 快速测试")
        return True
    else:
        print("\n已取消")
        return False


def show_examples():
    """显示配置示例"""

    print("\n" + "=" * 60)
    print("📝 配置示例")
    print("=" * 60)

    examples = {
        "Anthropic Claude": """
USE_MOCK_MODE=false
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-opus-4-5-20251101
""",
        "OpenAI GPT": """
USE_MOCK_MODE=false
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-xxx...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
""",
        "阿里云通义千问": """
USE_MOCK_MODE=false
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxx...
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1
DASHSCOPE_MODEL=qwen-max
""",
        "本地 vLLM/Ollama": """
USE_MOCK_MODE=false
LLM_PROVIDER=openai
OPENAI_API_KEY=not-needed
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_MODEL=llama-3.1-70b
""",
        "模拟模式（测试）": """
USE_MOCK_MODE=true
"""
    }

    for name, example in examples.items():
        print(f"\n【{name}】")
        print("-" * 60)
        print(example.strip())


def main():
    """主函数"""

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'setup':
            create_env_file()
        elif command == 'examples':
            show_examples()
        else:
            print(f"未知命令: {command}")
    else:
        # 默认：显示帮助
        print("\n" + "=" * 60)
        print("🔧 API 配置工具")
        print("=" * 60)
        print("\n使用方法:")
        print("  python3 setup_api.py setup      # 交互式配置向导")
        print("  python3 setup_api.py examples   # 查看配置示例")
        print("\n快速开始:")
        print("  1. 运行 'python3 setup_api.py setup'")
        print("  2. 根据提示输入配置")
        print("  3. 运行 'python3 test_real_api.py check' 检查")
        print("  4. 运行 'python3 test_real_api.py quick' 测试")
        print("=" * 60)


if __name__ == '__main__':
    main()
