# 🎨 漫画生成配置说明

## 📋 在 .env 中配置漫画参数

在 `.env` 文件中添加以下配置：

```bash
# ========== 漫画生成配置 ==========

# 漫画格数（生成多少格漫画）
COMIC_PANELS=6

# 漫画风格
COMIC_STYLE=manga
```

## 🎯 配置说明

### 1. COMIC_PANELS（漫画格数）

指定生成漫画的格子数量。

**可选值**：任意正整数（建议 4-12）

**示例**：
```bash
COMIC_PANELS=4   # 生成 4 格漫画（短篇）
COMIC_PANELS=6   # 生成 6 格漫画（默认，中等长度）
COMIC_PANELS=8   # 生成 8 格漫画（较长）
COMIC_PANELS=12  # 生成 12 格漫画（长篇）
```

**说明**：
- 格数越多，故事越详细，但生成时间越长，API 费用越高
- 建议根据故事复杂度选择合适的格数
- 简单故事：4-6 格
- 中等故事：6-8 格
- 复杂故事：8-12 格

### 2. COMIC_STYLE（漫画风格）

指定生成漫画的艺术风格。

**可选值**：
- `manga` - 日本漫画风格（默认）
- `comic` - 美式漫画风格
- `webtoon` - 韩国网络漫画风格
- `cartoon` - 卡通风格
- `anime` - 动画风格
- `sketch` - 手绘素描风格
- `watercolor` - 水彩画风格

**示例**：
```bash
COMIC_STYLE=manga      # 日漫风格
COMIC_STYLE=comic      # 美漫风格
COMIC_STYLE=webtoon    # 韩漫风格
COMIC_STYLE=watercolor # 水彩风格
```

## 📝 完整配置示例

### 示例 1：短篇日漫（快速测试）
```bash
USE_MOCK_MODE=true
COMIC_PANELS=4
COMIC_STYLE=manga
```

### 示例 2：中等长度日漫（推荐）
```bash
USE_MOCK_MODE=false
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=your-key
DASHSCOPE_MODEL=qwen-max

COMIC_PANELS=6
COMIC_STYLE=manga

IMAGE_PROVIDER=dashscope
```

### 示例 3：长篇美式漫画
```bash
USE_MOCK_MODE=false
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4

COMIC_PANELS=12
COMIC_STYLE=comic

IMAGE_PROVIDER=dalle
```

### 示例 4：水彩风格短篇
```bash
USE_MOCK_MODE=false
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-opus-4-5-20251101

COMIC_PANELS=4
COMIC_STYLE=watercolor

IMAGE_PROVIDER=stability
STABILITY_API_KEY=your-key
```

## 🚀 使用方法

### 1. 编辑配置文件
```bash
# 编辑 .env 文件
nano .env

# 或者创建新的配置
echo "COMIC_PANELS=8" >> .env
echo "COMIC_STYLE=manga" >> .env
```

### 2. 运行测试
```bash
python3 test_agent.py "你的漫画创意"
```

### 3. 查看结果
生成的漫画格数会严格按照 `COMIC_PANELS` 配置：
```
【第 1 格】
  文本: ...
  url: ...

【第 2 格】
  文本: ...
  url: ...

... 一共 8 格（如果配置了 COMIC_PANELS=8）
```

## 💡 最佳实践

### 根据故事长度选择格数

| 故事类型 | 推荐格数 | 说明 |
|---------|---------|------|
| 单个笑话/梗 | 4 格 | 经典四格漫画 |
| 简短故事 | 6 格 | 起承转合完整 |
| 中等故事 | 8 格 | 详细展开情节 |
| 复杂故事 | 10-12 格 | 多场景、多转折 |

### 根据风格选择提示词

不同风格适合不同类型的故事：

| 风格 | 适合的故事类型 | 特点 |
|------|---------------|------|
| manga | 冒险、热血、日常 | 黑白为主，分镜感强 |
| comic | 超级英雄、动作 | 色彩鲜艳，夸张 |
| webtoon | 爱情、都市 | 竖版长条，细腻 |
| watercolor | 温馨、文艺 | 柔和、梦幻 |
| sketch | 写实、严肃 | 简洁、有力 |

## ⚙️ 高级配置

### 动态调整格数

如果你想要根据故事复杂度动态调整，可以在代码中修改：

```python
# 在 test_agent.py 或其他脚本中
import os

# 短故事：4格
os.environ["COMIC_PANELS"] = "4"

# 中等故事：6格
os.environ["COMIC_PANELS"] = "6"

# 长故事：10格
os.environ["COMIC_PANELS"] = "10"
```

### 批量生成不同格数

```bash
# 生成 4 格版本
COMIC_PANELS=4 python3 test_agent.py "故事创意"

# 生成 8 格版本
COMIC_PANELS=8 python3 test_agent.py "故事创意"

# 生成 12 格版本
COMIC_PANELS=12 python3 test_agent.py "故事创意"
```

## ❓ 常见问题

### Q: 生成的格数和配置不一致？

**A**: 检查以下几点：
1. `.env` 文件是否在项目根目录
2. 配置格式是否正确（`COMIC_PANELS=6` 不要有空格）
3. 重启应用后重新测试

### Q: 可以生成超过 12 格吗？

**A**: 可以，但不推荐：
- API 调用次数多，费用高
- 生成时间长
- LLM 可能难以保持长故事的连贯性
- 建议分多个项目生成

### Q: 不同格数的费用差异？

**A**: 费用与格数成正比：
- 4 格：约 4 次 LLM 调用 + 4 次图片生成
- 6 格：约 6 次 LLM 调用 + 6 次图片生成
- 12 格：约 12 次 LLM 调用 + 12 次图片生成

---

**配置完成后，enjoy创作！** 🎨✨