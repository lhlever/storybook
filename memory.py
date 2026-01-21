"""
Memory 系统实现
包含四种类型的 Memory：
- Working Memory: 当前工作上下文
- Episodic Memory: 事件记忆
- Semantic Memory: 语义知识库
- Profile Memory: 项目配置信息
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class WorkingMemory:
    """工作记忆 - 存储当前正在处理的临时信息"""

    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        """设置工作记忆中的键值对"""
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取工作记忆中的值"""
        return self.data.get(key, default)

    def clear(self):
        """清空工作记忆"""
        self.data.clear()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.data.copy()


class EpisodicMemory:
    """情节记忆 - 存储发生的事件序列"""

    def __init__(self):
        self.episodes: List[Dict[str, Any]] = []

    def add_episode(self, event_type: str, content: Any, metadata: Optional[Dict] = None):
        """添加一个事件记录"""
        episode = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "content": content,
            "metadata": metadata or {}
        }
        self.episodes.append(episode)

    def get_recent_episodes(self, n: int = 10) -> List[Dict[str, Any]]:
        """获取最近的 n 个事件"""
        return self.episodes[-n:]

    def get_episodes_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """根据事件类型获取所有相关事件"""
        return [ep for ep in self.episodes if ep["event_type"] == event_type]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {"episodes": self.episodes}


class SemanticMemory:
    """语义记忆 - 存储知识和概念"""

    def __init__(self):
        self.knowledge: Dict[str, Any] = {
            "story_outline": None,
            "characters": [],
            "world_setting": {},
            "storyboards": [],
            "shots": []
        }

    def update_knowledge(self, key: str, value: Any):
        """更新知识库"""
        self.knowledge[key] = value

    def get_knowledge(self, key: str, default: Any = None) -> Any:
        """获取知识"""
        return self.knowledge.get(key, default)

    def add_to_list(self, key: str, item: Any):
        """向列表类型的知识中添加项"""
        if key not in self.knowledge:
            self.knowledge[key] = []
        if isinstance(self.knowledge[key], list):
            self.knowledge[key].append(item)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.knowledge.copy()


class ProfileMemory:
    """配置记忆 - 存储项目配置和用户偏好"""

    def __init__(self, project_name: str = "未命名项目"):
        self.profile: Dict[str, Any] = {
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "preferences": {},
            "settings": {
                "story_style": "现代",
                "target_audience": "全年龄",
                "story_length": "中篇"
            }
        }

    def set_profile(self, key: str, value: Any):
        """设置配置项"""
        self.profile[key] = value

    def get_profile(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.profile.get(key, default)

    def update_settings(self, settings: Dict[str, Any]):
        """批量更新设置"""
        self.profile["settings"].update(settings)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.profile.copy()


class MemorySystem:
    """统一的记忆系统管理器"""

    def __init__(self, project_name: str = "未命名项目"):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.profile = ProfileMemory(project_name)
        self.storage_path = Path("memory_storage")
        self.storage_path.mkdir(exist_ok=True)

    def save_to_disk(self, filename: Optional[str] = None):
        """将所有记忆保存到磁盘"""
        if filename is None:
            filename = f"{self.profile.get_profile('project_name')}.json"

        filepath = self.storage_path / filename
        memory_data = {
            "working": self.working.to_dict(),
            "episodic": self.episodic.to_dict(),
            "semantic": self.semantic.to_dict(),
            "profile": self.profile.to_dict()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)

        print(f"✓ Memory 已保存到: {filepath}")

    def load_from_disk(self, filename: str):
        """从磁盘加载记忆"""
        filepath = self.storage_path / filename

        if not filepath.exists():
            print(f"✗ 文件不存在: {filepath}")
            return False

        with open(filepath, 'r', encoding='utf-8') as f:
            memory_data = json.load(f)

        # 恢复各个记忆模块
        self.working.data = memory_data.get("working", {})
        self.episodic.episodes = memory_data.get("episodic", {}).get("episodes", [])
        self.semantic.knowledge = memory_data.get("semantic", {})
        self.profile.profile = memory_data.get("profile", {})

        print(f"✓ Memory 已从 {filepath} 加载")
        return True

    def get_summary(self) -> str:
        """获取记忆系统摘要"""
        summary = f"""
=== Memory 系统摘要 ===
项目名称: {self.profile.get_profile('project_name')}
创建时间: {self.profile.get_profile('created_at')}

Working Memory: {len(self.working.data)} 项
Episodic Memory: {len(self.episodic.episodes)} 个事件
Semantic Memory:
  - 故事大纲: {'已创建' if self.semantic.get_knowledge('story_outline') else '未创建'}
  - 角色数量: {len(self.semantic.get_knowledge('characters', []))}
  - 分镜数量: {len(self.semantic.get_knowledge('storyboards', []))}
  - 镜头数量: {len(self.semantic.get_knowledge('shots', []))}
        """
        return summary.strip()