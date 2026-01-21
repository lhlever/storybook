# 房源漫画生成 Agent

一个基于 AI 的智能 Agent，可以将房源信息自动转换为生动有趣的漫画故事。

## 项目简介

本项目旨在通过 AI 技术，将传统的房源描述转化为漫画形式的视觉内容，让房产信息的展示更加生动、有趣、易于理解。系统能够自动解析房源特征，生成富有创意的故事情节和视觉呈现。

## 核心功能

- **房源信息解析**：自动提取房源的关键信息（面积、户型、位置、价格等）
- **故事生成**：基于房源特点生成有趣的漫画故事脚本
- **漫画风格定制**：支持多种漫画风格（日系、美式、简笔画等）
- **分镜设计**：智能规划漫画分镜和布局
- **角色设定**：根据目标用户群体生成合适的角色形象
- **自动生成**：一键生成完整的房源漫画内容

## 技术架构

```
房源数据输入 → 信息解析 → 故事创作 → 分镜设计 → 图像生成 → 漫画输出
```

### 核心组件

- **信息提取模块**：解析和结构化房源数据
- **创意引擎**：生成漫画故事脚本和情节
- **分镜规划器**：设计漫画的分镜和布局
- **图像生成器**：生成漫画画面
- **后处理模块**：优化和组装最终输出

## 安装说明

```bash
# 克隆项目
git clone <repository-url>
cd storybook

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基础使用

```python
from storybook import HouseComicAgent

# 初始化 Agent
agent = HouseComicAgent()

# 输入房源信息
house_info = {
    "title": "阳光花园三居室",
    "area": 120,
    "bedrooms": 3,
    "price": 580,
    "location": "朝阳区",
    "features": ["南北通透", "精装修", "近地铁"]
}

# 生成漫画
comic = agent.generate_comic(house_info)
comic.save("output/house_comic.png")
```

### 高级配置

```python
# 自定义漫画风格和参数
config = {
    "style": "anime",  # 漫画风格：anime, cartoon, sketch
    "panels": 4,       # 分镜数量
    "characters": ["年轻夫妻", "房产经纪人"],
    "tone": "温馨",    # 故事基调
    "language": "zh-CN"
}

comic = agent.generate_comic(house_info, config=config)
```

## 使用场景

- **房产营销**：为房产中介提供创新的营销素材
- **线上展示**：在房产平台上增加互动性和趣味性
- **社交传播**：易于在社交媒体上分享和传播
- **客户沟通**：用更直观的方式向客户展示房源特点

## 配置说明

在 `config.yaml` 中配置相关参数：

```yaml
# API 配置
api:
  provider: "openai"  # openai, anthropic, local
  api_key: "your-api-key"
  model: "gpt-4"

# 生成配置
generation:
  max_panels: 6
  default_style: "anime"
  image_size: [1024, 1024]

# 语言配置
language:
  default: "zh-CN"
  supported: ["zh-CN", "en-US"]
```

## 项目结构

```
storybook/
├── agents/              # Agent 核心逻辑
├── models/              # 数据模型
├── generators/          # 内容生成器
├── utils/               # 工具函数
├── templates/           # 漫画模板
├── config/              # 配置文件
├── tests/               # 测试文件
└── examples/            # 示例代码
```

## 开发计划

- [ ] 支持更多漫画风格
- [ ] 添加视频动画生成功能
- [ ] 支持批量处理
- [ ] 多语言支持
- [ ] Web 界面
- [ ] API 服务

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- Issue: 在 GitHub 上提交 Issue
- Email: your-email@example.com

## 致谢

感谢所有为这个项目做出贡献的开发者！