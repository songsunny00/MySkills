from pathlib import Path
import json
from typing import Optional
from .models import NovelProject, StageStatus
from datetime import datetime

class ContextManager:
    """全局上下文管理器"""

    def __init__(self, project: NovelProject, output_dir: Path):
        self.project = project
        self.output_dir = output_dir
        self.project_dir = output_dir / project.project_id
        self._ensure_directories()

    def _ensure_directories(self):
        """确保项目目录存在"""
        dirs = [
            self.project_dir,
            self.project_dir / "worldbuilding",
            self.project_dir / "characters",
            self.project_dir / "plot",
            self.project_dir / "chapters",
            self.project_dir / "exports",
            self.project_dir / "config",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def save_metadata(self):
        """保存项目元数据"""
        metadata_path = self.project_dir / "metadata.json"
        self.project.updated_at = datetime.now()
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.project.model_dump(), f, ensure_ascii=False, indent=2, default=str)

    def load_metadata(self) -> NovelProject:
        """加载项目元数据"""
        metadata_path = self.project_dir / "metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Project metadata not found: {metadata_path}")

        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return NovelProject(**data)

    def update_stage_status(self, stage: str, status: StageStatus):
        """更新阶段状态"""
        self.project.stage_status[stage] = status
        self.project.current_stage = stage
        self.save_metadata()

    def save_world_building(self, content: str):
        """保存世界观"""
        path = self.project_dir / "worldbuilding" / "world.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.project.world_building = content
        self.save_metadata()

    def save_character(self, character_name: str, content: str):
        """保存角色档案"""
        safe_name = character_name.replace(" ", "_").lower()
        path = self.project_dir / "characters" / f"{safe_name}.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def save_outline(self, content: str):
        """保存大纲"""
        path = self.project_dir / "plot" / "outline.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def save_chapter(self, chapter_num: int, content: str):
        """保存章节"""
        path = self.project_dir / "chapters" / f"chapter-{chapter_num:03d}.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.project.chapters[chapter_num] = content
        self.save_metadata()

    def get_chapter(self, chapter_num: int) -> Optional[str]:
        """获取章节内容"""
        path = self.project_dir / "chapters" / f"chapter-{chapter_num:03d}.md"
        if not path.exists():
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_context_summary(self) -> str:
        """获取上下文摘要（用于生成时保持一致性）"""
        summary_parts = []

        if self.project.world_building:
            summary_parts.append(f"## 世界观\n{self.project.world_building[:500]}...")

        if self.project.characters:
            summary_parts.append("## 主要角色")
            for char in self.project.characters[:3]:
                summary_parts.append(f"- {char.name}: {char.personality[:100]}")

        return "\n\n".join(summary_parts)