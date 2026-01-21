# 🔧 配置指南

本文档介绍如何配置 StoryBook 的语言模型和文生图 API。

## 📋 目录

1. [快速开始](#快速开始)
2. [语言模型配置](#语言模型配置)
3. [文生图配置](#文生图配置)
4. [配置文件结构](#配置文件结构)
5. [常见问题](#常见问题)

---

## 🚀 快速开始

### 步骤 1: 复制配置模板

```bash
cd /Users/liuhailu/pycharmProjects/storybook
cp .env.example .env
```

### 步骤 2: 编辑配置文件

用文本编辑器打开 `.env` 文件，填入你的 API Key：

```bash
vim .env
# 或
nano .env
# 或使用其他编辑器
```

### 步骤 3: 最小配置示例

如果你只想先测试，可以使用**模拟模式**（不需要 API Key）：

```bash
# .env 文件
USE_MOCK_MODE=true
```

项目会自动使用模拟数据运行。

---

## 🤖 语言模型配置

### 选项 1: Anthropic Claude（推荐）

```bash
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
ANTHROPIC_MODEL=claude-opus-4-5-20251101

# 模型选择：
# - claude-opus-4-5-20251101    (最强大，创意最佳)
# - claude-sonnet-4-20250514    (平衡性能和成本)
# - claude-3-5-haiku-20241022   (最快速，成本最低)
```

**获取 API Key:**
1. 访问 https://console.anthropic.com/
2. 注册账号
3. 进入 API Keys 页面
4. 创建新的 API Key

### 选项 2: OpenAI GPT

```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-xxx...
OPENAI_MODEL=gpt-4
OPENAI_BASE_URL=https://api.openai.com/v1

# 模型选择：
# - gpt-4              (最强大)
# - gpt-4-turbo        (更快的 GPT-4)
# - gpt-3.5-turbo      (快速且便宜)
```

**获取 API Key:**
1. 访问 https://platform.openai.com/
2. 注册账号
3. 进入 API Keys 页面
4. 创建新的 API Key

### 选项 3: 阿里云通义千问

```bash
# .env
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxx...
DASHSCOPE_MODEL=qwen-max

# 模型选择：
# - qwen-max          (最强大)
# - qwen-plus         (平衡)
# - qwen-turbo        (快速)
```

**获取 API Key:**
1. 访问 https://dashscope.aliyun.com/
2. 注册阿里云账号
3. 开通通义千问服务
4. 获取 API Key

### LLM 参数调整

```bash
# 控制生成的随机性 (0.0 = 确定性, 1.0 = 高随机性)
LLM_TEMPERATURE=0.7

# 生成的最大 token 数
LLM_MAX_TOKENS=2048

# Top-p 采样参数
LLM_TOP_P=1.0
```

---

## 🎨 文生图配置

### 选项 1: DALL-E（OpenAI）

```bash
# .env
IMAGE_PROVIDER=dalle
DALLE_API_KEY=sk-proj-xxx...
DALLE_MODEL=dall-e-3
DALLE_SIZE=1024x1024
DALLE_QUALITY=standard

# 尺寸选项：1024x1024, 1024x1792, 1792x1024
# 质量选项：standard, hd
```

### 选项 2: Stability AI

```bash
# .env
IMAGE_PROVIDER=stability
STABILITY_API_KEY=sk-xxx...
STABILITY_MODEL=stable-diffusion-xl-1024-v1-0
```

**获取 API Key:**
1. 访问 https://platform.stability.ai/
2. 注册账号
3. 获取 API Key

### 选项 3: Replicate

```bash
# .env
IMAGE_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_xxx...
```

**获取 API Key:**
1. 访问 https://replicate.com/
2. 注册账号
3. 进入 Account Settings
4. 获取 API Token

### 选项 4: 阿里云通义万相

```bash
# .env
IMAGE_PROVIDER=dashscope
DASHSCOPE_IMAGE_API_KEY=sk-xxx...
```

---

## 📁 配置文件结构

项目包含以下配置相关文件：

```
storybook/
├── .env.example        # 配置模板（需复制为 .env）
├── .env               # 你的实际配置（不会被 git 跟踪）
├── config.py          # 配置管理模块
├── llm_client.py      # 语言模型客户端
├── image_client.py    # 文生图客户端
└── tools.py           # 使用客户端的工具函数
```

### 配置加载优先级

1. 首先读取 `.env` 文件
2. 如果 `.env` 不存在，使用默认值
3. 如果没有配置 API Key，自动启用**模拟模式**

---

## 🔍 验证配置

### 方法 1: 运行配置测试

```bash
python config.py
```

输出示例：
```
✓ 已加载配置文件: /path/to/.env

====================================================
📋 当前配置摘要
====================================================
模式: 🚀 真实 API 模式

LLM 配置:
  - 提供商: anthropic
  - 模型: claude-opus-4-5-20251101
  - API Key: 已配置
  - Temperature: 0.7
  - Max Tokens: 2048

文生图配置:
  - 提供商: dalle
  - 模型: dall-e-3
  - API Key: 已配置

其他配置:
  - Memory 路径: memory_storage
  - API 超时: 60秒
  - 日志级别: INFO
====================================================

✓ 配置验证成功
```

### 方法 2: 测试 LLM 客户端

```bash
python llm_client.py
```

### 方法 3: 测试图像客户端

```bash
python image_client.py
```

---

## 💡 使用场景配置建议

### 场景 1: 本地开发测试

```bash
# 使用模拟模式，无需 API Key
USE_MOCK_MODE=true
```

### 场景 2: 生产环境（最佳质量）

```bash
# 使用 Claude Opus + DALL-E 3
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-opus-4-5-20251101

IMAGE_PROVIDER=dalle
DALLE_API_KEY=your-key
DALLE_MODEL=dall-e-3
DALLE_QUALITY=hd
```

### 场景 3: 成本优化

```bash
# 使用 Claude Haiku + 标准 DALL-E
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-3-5-haiku-20241022

IMAGE_PROVIDER=dalle
DALLE_API_KEY=your-key
DALLE_QUALITY=standard
```

### 场景 4: 国内环境

```bash
# 使用阿里云服务
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=your-key
DASHSCOPE_MODEL=qwen-max

IMAGE_PROVIDER=dashscope
DASHSCOPE_IMAGE_API_KEY=your-key
```

---

## ❓ 常见问题

### Q1: 如何切换模拟模式和真实 API 模式？

在 `.env` 文件中设置：
```bash
# 模拟模式
USE_MOCK_MODE=true

# 真实 API 模式
USE_MOCK_MODE=false
```

如果没有配置任何 API Key，系统会自动启用模拟模式。

### Q2: 可以只配置语言模型，不配置图像生成吗？

可以！图像生成是可选的。只需配置 LLM：

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key
# 不配置 IMAGE_PROVIDER
```

### Q3: API 调用超时怎么办？

增加超时时间：
```bash
API_TIMEOUT=120  # 增加到 120 秒
```

### Q4: 如何查看详细的调用日志？

设置日志级别：
```bash
LOG_LEVEL=DEBUG
```

### Q5: 配置文件找不到？

确保 `.env` 文件在项目根目录：
```bash
ls -la .env
# 如果不存在，从模板复制
cp .env.example .env
```

### Q6: API Key 安全吗？

`.env` 文件已在 `.gitignore` 中，不会被提交到 git。但仍需注意：
- ✅ 不要分享你的 `.env` 文件
- ✅ 不要将 API Key 硬编码在代码中
- ✅ 定期轮换 API Key
- ✅ 使用环境变量管理敏感信息

### Q7: 可以使用自定义的 OpenAI 兼容 API 吗？

可以！修改 base URL：
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
```

### Q8: 如何估算 API 成本？

不同提供商的定价：
- **Claude Opus 4.5**: ~$15/1M input tokens, ~$75/1M output tokens
- **Claude Sonnet**: ~$3/1M input tokens, ~$15/1M output tokens
- **Claude Haiku**: ~$0.25/1M input tokens, ~$1.25/1M output tokens
- **GPT-4**: ~$30/1M tokens
- **DALL-E 3**: ~$0.04-0.08 per image

一个典型的创作流程（大纲+角色+分镜+镜头）大约消耗：
- 输入: ~3,000 tokens
- 输出: ~5,000 tokens
- 总成本: Claude Opus ~$0.50, Claude Haiku ~$0.01

---

## 🆘 需要帮助？

如果遇到配置问题：

1. 查看配置摘要：`python config.py`
2. 测试客户端：`python llm_client.py`
3. 查看错误日志：设置 `LOG_LEVEL=DEBUG`
4. 在 GitHub 提 Issue

---

## 📚 相关文档

- [README.md](README.md) - 项目总览
- [.env.example](.env.example) - 配置模板
- [Anthropic API 文档](https://docs.anthropic.com/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
- [阿里云通义千问文档](https://help.aliyun.com/zh/dashscope/)
