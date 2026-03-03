import asyncio
from typing import Optional, Callable
from pathlib import Path
from .models import NovelProject, NovelGenre, GenerationMode
from .config import LLMConfig, ProjectConfig
from .context_manager import ContextManager
from .llm_client import create_llm_client
from .prompt_templates import PromptTemplateManager
from .stages import (
    WorldBuildingStage,
    CharacterCreationStage,
    PlotDesignStage,
    OutlineGenerationStage,
    ChapterGenerationStage
)

class NovelGenerator:
    """小说生成器主类"""

    def __init__(
        self,
        project_config: ProjectConfig,
        llm_config: LLMConfig
    ):
        self.project_config = project_config
        self.llm_config = llm_config
        self.llm_client = create_llm_client(llm_config)
        self.template_manager = PromptTemplateManager(project_config.templates_dir)

    async def generate_novel(
        self,
        genre: NovelGenre,
        mode: GenerationMode,
        target_word_count: int = 60000,
        project_id: Optional[str] = None,
        on_progress: Optional[Callable] = None,
        on_stage_complete: Optional[Callable] = None
    ) -> NovelProject:
        """一键生成小说"""

        # 创建项目
        if not project_id:
            import uuid
            project_id = f"novel_{uuid.uuid4().hex[:8]}"

        project = NovelProject(
            project_id=project_id,
            genre=genre,
            mode=mode,
            target_word_count=target_word_count
        )

        # 创建上下文管理器
        ctx = ContextManager(project, self.project_config.output_dir)
        ctx.save_metadata()

        if on_progress:
            on_progress("项目初始化完成")

        # 阶段1: 世界观构建
        world_stage = WorldBuildingStage(project, ctx, self.llm_client, self.template_manager)
        world_building = await world_stage.run(on_progress=on_progress)
        project.world_building = world_building

        if on_stage_complete:
            await on_stage_complete("worldbuilding", world_building)

        # 阶段2: 角色创建
        char_stage = CharacterCreationStage(project, ctx, self.llm_client, self.template_manager)
        characters = await char_stage.run(on_progress=on_progress)

        if on_stage_complete:
            await on_stage_complete("characters", characters)

        # 阶段3: 情节设计
        plot_stage = PlotDesignStage(project, ctx, self.llm_client, self.template_manager)
        plot_design = await plot_stage.run(on_progress=on_progress)

        if on_stage_complete:
            await on_stage_complete("plot", plot_design)

        # 阶段4: 大纲生成
        outline_stage = OutlineGenerationStage(project, ctx, self.llm_client, self.template_manager)
        outline = await outline_stage.run(on_progress=on_progress)

        if on_stage_complete:
            await on_stage_complete("outline", outline)

        # 阶段5: 章节生成（智能策略）
        chapter_count = target_word_count // 2000
        await self._generate_chapters_smart(
            project, ctx, chapter_count, on_progress, on_stage_complete
        )

        if on_progress:
            on_progress("小说生成完成！")

        return project

    async def _generate_chapters_smart(
        self,
        project: NovelProject,
        ctx: ContextManager,
        chapter_count: int,
        on_progress: Optional[Callable],
        on_stage_complete: Optional[Callable]
    ):
        """智能章节生成策略：关键章节优先"""

        chapter_stage = ChapterGenerationStage(project, ctx, self.llm_client, self.template_manager)

        # 关键章节列表
        key_chapters = [
            1,  # 开篇
            int(chapter_count * 0.7),  # 高潮
            chapter_count  # 结局
        ]

        # 先生成关键章节
        for chapter_num in key_chapters:
            if on_progress:
                on_progress(f"生成关键章节: 第{chapter_num}章")

            content = await chapter_stage.execute(chapter_num)

            if on_stage_complete:
                await on_stage_complete(f"chapter_{chapter_num}", content)

        # 批量生成其余章节
        remaining_chapters = [i for i in range(1, chapter_count + 1) if i not in key_chapters]

        batch_size = 5
        for i in range(0, len(remaining_chapters), batch_size):
            batch = remaining_chapters[i:i + batch_size]

            if on_progress:
                on_progress(f"批量生成章节: {batch[0]}-{batch[-1]}")

            for chapter_num in batch:
                content = await chapter_stage.execute(chapter_num)

                if on_stage_complete:
                    await on_stage_complete(f"chapter_{chapter_num}", content)

            # 批次完成后暂停，等待用户确认
            if on_stage_complete:
                await on_stage_complete("batch_complete", {"chapters": batch})