# 🎯 如何启动项目

## 方式一：直接运行（最简单，推荐新手）

无需任何配置，直接运行查看演示：

```bash
# 1. 进入项目目录
cd /Users/liuhailu/pycharmProjects/storybook

# 2. 安装依赖（首次运行需要）
pip install langgraph langchain langchain-core python-dotenv pydantic

# 3. 运行演示
python main.py --demo
```

就这么简单！系统会自动使用模拟模式，展示完整的创作流程。

---

## 方式二：交互式 CLI

```bash
python main.py
```

会看到菜单：
```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              📚 StoryBook 创作型 Agent                      ║
║                                                            ║
║        基于 LangGraph + Memory 的智能创作助手               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

【主菜单】
1. 创建新项目
2. 加载已有项目
3. 查看 Memory 摘要
4. 查看工作流程
5. 退出

请选择操作 (1-5):
```

选择 `1` 创建新项目，按提示输入信息即可。

---

## 方式三：使用真实 API（可选）

如果你有 Claude 或 OpenAI 的 API Key，可以使用真实的 AI 生成：

### Step 1: 复制配置文件
```bash
cp .env.example .env
```

### Step 2: 编辑 .env 文件

用任意文本编辑器打开 `.env`，填入你的配置：

```bash
# 使用 Claude（推荐）
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-你的key

# 或使用 OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-proj-你的key
```

### Step 3: 安装额外依赖
```bash
# 如果用 Claude
pip install anthropic

# 如果用 OpenAI
pip install openai
```

### Step 4: 运行
```bash
python main.py --demo
```

---

## 完整安装（一次性安装所有）

如果你想一次性安装所有依赖：

```bash
pip install -r requirements.txt
```

这会安装：
- LangGraph（必需）
- Anthropic SDK（使用 Claude 时需要）
- OpenAI SDK（使用 GPT/DALL-E 时需要）
- 其他工具库

---

## 常见启动问题

### ❌ 找不到 python 命令

尝试使用 `python3`：
```bash
python3 main.py --demo
```

### ❌ 提示缺少模块

安装对应的模块：
```bash
# 缺少 langgraph
pip install langgraph

# 缺少 dotenv
pip install python-dotenv

# 或安装所有依赖
pip install -r requirements.txt
```

### ❌ 权限错误

使用 `--user` 参数：
```bash
pip install --user -r requirements.txt
```

### ❌ 虚拟环境相关

如果你使用虚拟环境：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py --demo
```

---

## 验证是否启动成功

成功启动后会看到类似输出：

```
⚠ 未找到 .env 文件，使用默认配置（模拟模式）
ℹ️  未检测到有效的 API Key，自动启用模拟模式

====================================================
🚀 演示模式：自动创建示例项目
====================================================

项目名称: 时光旅行者_演示
故事创意: 一个物理学研究生在祖父遗物中发现了时间机器的秘密...

开始自动创作...

==================================================
🚀 初始化创作流程
==================================================

📝 Step 1: 生成故事大纲
--------------------------------------------------
[模拟 LLM 调用] 生成故事大纲...
✓ 故事标题: 时光旅行者
✓ 故事类型: 科幻/剧情
...
```

看到这些输出就说明成功了！

---

## 快速命令速查

| 命令 | 说明 |
|------|------|
| `python main.py --demo` | 运行演示（自动创作示例项目） |
| `python main.py` | 启动交互式 CLI |
| `python main.py --help` | 查看帮助 |
| `python config.py` | 查看当前配置 |
| `python llm_client.py` | 测试语言模型 |
| `python image_client.py` | 测试图像生成 |

---

## 推荐的启动流程

**第一次使用：**
```bash
# 1. 安装基础依赖
pip install langgraph langchain langchain-core python-dotenv pydantic

# 2. 运行演示看看效果
python main.py --demo

# 3. 如果觉得不错，配置真实 API
cp .env.example .env
vim .env  # 填入你的 API Key

# 4. 安装对应的 SDK
pip install anthropic  # 或 openai

# 5. 再次运行，使用真实 AI
python main.py --demo
```

**日常使用：**
```bash
# 直接启动 CLI
python main.py
```

---

**还有问题？** 查看 [README.md](README.md) 或 [QUICK_START.md](QUICK_START.md)
