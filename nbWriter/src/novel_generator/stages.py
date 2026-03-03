from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from .models import NovelProject, StageStatus
from .context_manager import ContextManager
from .llm_client import LLMClient
from .prompt_templates import get_template_content, PromptTemplateManager
from pathlib import Path

class GenerationStage(ABC):
    """生成阶段抽象基类"""

    def __init__(
        self,
        project: NovelProject,
        context_manager: ContextManager,
        llm_client: LLMClient,
        template_manager: Optional[PromptTemplateManager] = None
    ):
        self.project = project
        self.ctx = context_manager
        self.llm = llm_client
        self.template_manager = template_manager

    @abstractmethod
    async def execute(self, user_input: Optional[str] = None) -> Any:
        """执行生成阶段"""
        pass

    @abstractmethod
    def get_stage_name(self) -> str:
        """获取阶段名称"""
        pass

    async def run(self, user_input: Optional[str] = None, on_progress: Optional[Callable] = None) -> Any:
        """运行阶段（带状态管理）"""
        stage_name = self.get_stage_name()

        # 更新状态为进行中
        self.ctx.update_stage_status(stage_name, StageStatus.IN_PROGRESS)

        if on_progress:
            on_progress(f"开始{stage_name}阶段...")

        try:
            result = await self.execute(user_input)

            # 更新状态为完成
            self.ctx.update_stage_status(stage_name, StageStatus.COMPLETED)

            if on_progress:
                on_progress(f"{stage_name}阶段完成！")

            return result

        except Exception as e:
            # 更新状态为失败
            self.ctx.update_stage_status(stage_name, StageStatus.FAILED)
            raise e


class WorldBuildingStage(GenerationStage):
    """世界观构建阶段"""

    def get_stage_name(self) -> str:
        return "世界观构建"

    async def execute(self, user_input: Optional[str] = None) -> str:
        """执行世界观生成"""
        template_content = get_template_content("worldbuilding")

        prompt = self.template_manager.render_string(
            template_content,
            genre=self.project.genre,
            mode=self.project.mode,
            user_input=user_input or ""
        )

        world_building = await self.llm.generate(prompt)

        # 保存世界观
        self.ctx.save_world_building(world_building)

        return world_building


class CharacterCreationStage(GenerationStage):
    """角色创建阶段"""

    def get_stage_name(self) -> str:
        return "角色设定"

    async def execute(self, user_input: Optional[str] = None) -> list:
        """执行角色生成"""
        template_content = get_template_content("character_creation")

        # 生成主角
        protagonist = await self._create_character("protagonist", template_content, user_input)

        # 生成配角（2-3个）
        supporting_chars = []
        for i in range(2):
            char = await self._create_character("supporting", template_content)
            supporting_chars.append(char)

        # 生成反派
        antagonist = await self._create_character("antagonist", template_content)

        all_characters = [protagonist] + supporting_chars + [antagonist]

        return all_characters

    async def _create_character(self, role: str, template_content: str, user_input: Optional[str] = None) -> str:
        """创建单个角色"""
        prompt = self.template_manager.render_string(
            template_content,
            genre=self.project.genre,
            role=role,
            world_building=self.project.world_building,
            user_input=user_input or ""
        )

        character_content = await self.llm.generate(prompt)

        # 保存角色档案
        char_name = self._extract_character_name(character_content, role)
        self.ctx.save_character(char_name, character_content)

        return character_content

    def _extract_character_name(self, content: str, role: str) -> str:
        """从内容中提取角色名称（简单实现）"""
        # 这里可以用更复杂的解析逻辑
        lines = content.split('\n')
        for line in lines:
            if '姓名' in line or '名字' in line:
                parts = line.split('：')
                if len(parts) > 1:
                    return parts[1].strip()
        return f"{role}_character"


class PlotDesignStage(GenerationStage):
    """情节设计阶段"""

    def get_stage_name(self) -> str:
        return "情节设计"

    async def execute(self, user_input: Optional[str] = None) -> str:
        """执行情节设计"""
        template_content = get_template_content("plot_design")

        prompt = self.template_manager.render_string(
            template_content,
            genre=self.project.genre,
            target_word_count=self.project.target_word_count,
            world_building=self.project.world_building,
            characters=self.project.characters,
            user_input=user_input or ""
        )

        plot_design = await self.llm.generate(prompt)

        # 保存情节设计
        plot_file = self.ctx.project_dir / "plot" / "plot_design.md"
        plot_file.write_text(plot_design, encoding='utf-8')

        return plot_design


class OutlineGenerationStage(GenerationStage):
    """大纲生成阶段"""

    def get_stage_name(self) -> str:
        return "大纲生成"

    async def execute(self, user_input: Optional[str] = None) -> str:
        """执行大纲生成"""
        # 计算章节数
        chapter_count = self.project.target_word_count // 2000  # 平均每章2000字
        words_per_chapter = self.project.target_word_count // chapter_count

        template_content = get_template_content("outline_generation")

        # 读取情节设计
        plot_file = self.ctx.project_dir / "plot" / "plot_design.md"
        plot_design = plot_file.read_text(encoding='utf-8') if plot_file.exists() else ""

        prompt = self.template_manager.render_string(
            template_content,
            genre=self.project.genre,
            target_word_count=self.project.target_word_count,
            chapter_count=chapter_count,
            world_building=self.project.world_building,
            plot_design=plot_design,
            words_per_chapter=words_per_chapter
        )

        outline = await self.llm.generate(prompt)

        # 保存大纲
        self.ctx.save_outline(outline)

        return outline


class ChapterGenerationStage(GenerationStage):
    """章节生成阶段"""

    def get_stage_name(self) -> str:
        return "章节生成"

    async def execute(self, chapter_number: int, user_input: Optional[str] = None) -> str:
        """执行单章生成"""
        template_content = get_template_content("chapter_generation")

        # 读取大纲
        outline_file = self.ctx.project_dir / "plot" / "outline.md"
        outline = outline_file.read_text(encoding='utf-8') if outline_file.exists() else ""

        # 提取该章节的大纲
        chapter_outline = self._extract_chapter_outline(outline, chapter_number)

        # 获取上一章内容
        previous_chapter = self.ctx.get_chapter(chapter_number - 1) if chapter_number > 1 else None

        # 获取上下文摘要
        context_summary = self.ctx.get_context_summary()

        prompt = self.template_manager.render_string(
            template_content,
            genre=self.project.genre,
            chapter_number=chapter_number,
            chapter_title=f"第{chapter_number}章",
            chapter_outline=chapter_outline,
            context_summary=context_summary,
            previous_chapter=previous_chapter or "",
            target_word_count=2000
        )

        chapter_content = await self.llm.generate(prompt)

        # 保存章节
        self.ctx.save_chapter(chapter_number, chapter_content)

        return chapter_content

    def _extract_chapter_outline(self, outline: str, chapter_number: int) -> str:
        """从完整大纲中提取指定章节的大纲"""
        # 简单实现：查找对应章节的内容
        lines = outline.split('\n')
        chapter_lines = []
        in_chapter = False

        for line in lines:
            if f"第{chapter_number}章" in line or f"## {chapter_number}" in line:
                in_chapter = True
                chapter_lines.append(line)
            elif in_chapter:
                if line.startswith('##') and chapter_number not in line:
                    break
                chapter_lines.append(line)

        return '\n'.join(chapter_lines) if chapter_lines else f"第{chapter_number}章大纲"