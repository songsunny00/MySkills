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

    def get_generated_chapters(self) -> list[int]:
        """获取已生成的章节列表"""
        chapters_dir = self.project_dir / "chapters"
        if not chapters_dir.exists():
            return []
        
        chapters = []
        for f in chapters_dir.glob("chapter-*.md"):
            try:
                num = int(f.stem.split('-')[1])
                chapters.append(num)
            except (ValueError, IndexError):
                continue
        return sorted(chapters)

    def get_missing_chapters(self, total_chapters: int) -> list[int]:
        """获取缺失的章节列表"""
        generated = set(self.get_generated_chapters())
        return [i for i in range(1, total_chapters + 1) if i not in generated]

    def get_polished_chapters(self) -> list[int]:
        """获取已润色的章节列表（通过检查metadata中的polish标记）"""
        if not hasattr(self.project, 'polished_chapters'):
            return []
        return self.project.polished_chapters if isinstance(self.project.polished_chapters, list) else []

    def mark_chapter_polished(self, chapter_num: int):
        """标记章节已润色"""
        if not hasattr(self.project, 'polished_chapters'):
            self.project.polished_chapters = []
        if chapter_num not in self.project.polished_chapters:
            self.project.polished_chapters.append(chapter_num)
            self.save_metadata()

    def update_chapter_titles(self, outline: str, on_progress: Optional[Callable] = None) -> dict:
        """批量更新已有章节的标题

        Args:
            outline: 大纲文本
            on_progress: 进度回调函数

        Returns:
            包含更新统计信息的字典
        """
        from .stages import extract_chapter_title

        chapters_dir = self.project_dir / "chapters"
        if not chapters_dir.exists():
            return {"updated": 0, "failed": 0, "message": "章节目录不存在"}

        updated = 0
        failed = 0
        chapter_files = sorted(chapters_dir.glob("chapter-*.md"))

        for idx, chapter_file in enumerate(chapter_files, 1):
            try:
                chapter_number = int(chapter_file.stem.split('-')[1])

                # 提取标题
                title = extract_chapter_title(outline, chapter_number)
                if not title:
                    failed += 1
                    if on_progress:
                        on_progress(f"⚠️  第{chapter_number}章未找到标题")
                    continue

                # 读取章节内容
                content = chapter_file.read_text(encoding='utf-8')

                # 替换第一行标题
                lines = content.split('\n')
                if lines and lines[0].startswith('# 第'):
                    lines[0] = f"# 第{chapter_number}章 {title}"
                    updated_content = '\n'.join(lines)
                    chapter_file.write_text(updated_content, encoding='utf-8')
                    updated += 1

                    if on_progress:
                        on_progress(f"✓ 已更新第{chapter_number}章标题 ({idx}/{len(chapter_files)})")

            except Exception as e:
                failed += 1
                if on_progress:
                    on_progress(f"✗ 第{chapter_number}章更新失败: {str(e)}")
                continue

        return {
            "updated": updated,
            "failed": failed,
            "message": f"已更新 {updated} 章，失败 {failed} 章"
        }

    @classmethod
    def load_from_project_id(cls, project_id: str, output_dir: Path) -> "ContextManager":
        """从项目ID加载上下文管理器"""
        project_dir = output_dir / project_id
        metadata_path = project_dir / "metadata.json"
        
        if not metadata_path.exists():
            raise FileNotFoundError(f"项目不存在: {project_id}")
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project = NovelProject(**data)
        ctx = cls.__new__(cls)
        ctx.project = project
        ctx.output_dir = output_dir
        ctx.project_dir = project_dir
        return ctx