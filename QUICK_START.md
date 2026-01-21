# 🚀 快速开始指南

## 1️⃣ 三种运行方式

### 方式 A: 模拟模式（无需配置）

直接运行，无需任何 API Key：
```bash
python main.py --demo
```

### 方式 B: 最简配置（推荐）

只需 3 步：

1. **复制配置模板**
```bash
cp .env.example .env
```

2. **填入你的配置**

编辑 `.env` 文件，填入以下内容：
```bash
# 语言模型配置（三选一）
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-opus-4-5-20251101
```

3. **运行**
```bash
python main.py --demo
```

### 方式 C: 完全自定义

支持自部署模型、第三方服务：
```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=http://your-server:8000/v1
OPENAI_MODEL=your-model-name

IMAGE_PROVIDER=dalle
DALLE_API_KEY=your-key
DALLE_BASE_URL=https://api.openai.com/v1
DALLE_MODEL=dall-e-3
```

---

## 2️⃣ 配置示例

### 使用 Claude（最佳创意）
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-xxx
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-opus-4-5-20251101
```

### 使用 OpenAI GPT
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
```

### 使用阿里云通义千问（国内快）
```bash
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1
DASHSCOPE_MODEL=qwen-max
```

### 使用自部署模型（如 vLLM, Ollama）
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=any-string-or-empty
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_MODEL=llama-3.1-70b
```

### 添加图像生成（可选）
```bash
# 在上面任意配置基础上添加：
IMAGE_PROVIDER=dalle
DALLE_API_KEY=sk-proj-xxx
DALLE_BASE_URL=https://api.openai.com/v1
DALLE_MODEL=dall-e-3
```

---

## 3️⃣ 验证配置

```bash
# 查看配置
python config.py

# 测试 LLM
python llm_client.py

# 测试图像生成
python image_client.py
```

---

## 4️⃣ 必填项说明

每个提供商只需配置 3 个必填项：

| 提供商 | API Key | Base URL | Model |
|--------|---------|----------|-------|
| **Anthropic** | `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL` | `ANTHROPIC_MODEL` |
| **OpenAI** | `OPENAI_API_KEY` | `OPENAI_BASE_URL` | `OPENAI_MODEL` |
| **Dashscope** | `DASHSCOPE_API_KEY` | `DASHSCOPE_BASE_URL` | `DASHSCOPE_MODEL` |

**默认值已配置好**，如果你使用官方服务，只需填 API Key 即可：
```bash
# 最简配置示例
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key
# BASE_URL 和 MODEL 会使用默认值
```

---

## 5️⃣ 获取 API Key

### Anthropic Claude
1. 访问 https://console.anthropic.com/
2. 注册并创建 API Key

### OpenAI
1. 访问 https://platform.openai.com/
2. 注册并创建 API Key

### 阿里云通义千问
1. 访问 https://dashscope.aliyun.com/
2. 开通服务并获取 API Key

---

## 6️⃣ 常见问题

**Q: 没有 API Key 能用吗？**
A: 可以！不配置任何 Key，系统会自动使用模拟模式。

**Q: 可以只配置语言模型吗？**
A: 可以！图像生成是可选的。

**Q: 如何使用自己部署的模型？**
A: 设置 `LLM_PROVIDER=openai`，然后修改 `OPENAI_BASE_URL` 为你的服务地址。

**Q: 配置文件在哪？**
A: 项目根目录的 `.env` 文件（需要从 `.env.example` 复制）。

**Q: 配置错误怎么办？**
A: 运行 `python config.py` 查看详细的配置状态和错误提示。

---

## 7️⃣ 更多信息

- 完整配置说明：查看 [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
- 项目总览：查看 [README.md](README.md)
- 配置模板：查看 [.env.example](.env.example)

---

**开始创作吧！** 🎨✨