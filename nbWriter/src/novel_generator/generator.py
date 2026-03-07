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
    SupplementaryCharacterStage,
    OutlineGenerationStage,
    ChapterGenerationStage,
    PolishStage
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
        words_per_chapter: int = 2000,
        project_id: Optional[str] = None,
        on_progress: Optional[Callable] = None,
        on_stage_complete: Optional[Callable] = None,
        enable_polish: bool = True,
        polish_requirements: Optional[str] = None
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
            target_word_count=target_word_count,
            words_per_chapter=words_per_chapter
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

        # 阶段4: 补充配角
        supplementary_stage = SupplementaryCharacterStage(project, ctx, self.llm_client, self.template_manager)
        supplementary_chars = await supplementary_stage.run(on_progress=on_progress)

        if on_stage_complete:
            await on_stage_complete("supplementary_characters", supplementary_chars)

        # 阶段5: 大纲生成
        outline_stage = OutlineGenerationStage(project, ctx, self.llm_client, self.template_manager)
        outline = await outline_stage.run(on_progress=on_progress)

        if on_stage_complete:
            await on_stage_complete("outline", outline)

        # 阶段6: 章节生成（智能策略）
        chapter_count = target_word_count // words_per_chapter
        await self._generate_chapters_smart(
            project, ctx, chapter_count, on_progress, on_stage_complete
        )

        # 阶段7: 润色与去AI化（可选）
        if enable_polish:
            if on_progress:
                on_progress("开始润色与去AI化处理...")
            polish_stage = PolishStage(project, ctx, self.llm_client, self.template_manager)
            polish_result = await polish_stage.run(
                user_input=polish_requirements,
                on_progress=on_progress
            )
            if on_stage_complete:
                await on_stage_complete("polish", polish_result)

        if on_progress:
            on_progress("小说生成完成！")

        return project

    async def polish_project(
        self,
        project: NovelProject,
        ctx: ContextManager,
        requirements: Optional[str] = None,
        on_progress: Optional[Callable] = None
    ) -> dict:
        """对已有项目单独执行润色"""
        polish_stage = PolishStage(project, ctx, self.llm_client, self.template_manager)
        return await polish_stage.run(user_input=requirements, on_progress=on_progress)

    async def _generate_chapters_smart(
        self,
        project: NovelProject,
        ctx: ContextManager,
        chapter_count: int,
        on_progress: Optional[Callable],
        on_stage_complete: Optional[Callable],
        skip_existing: bool = True
    ):
        """智能章节生成策略：关键章节优先，支持断点续传"""

        chapter_stage = ChapterGenerationStage(project, ctx, self.llm_client, self.template_manager)

        generated_chapters = set(ctx.get_generated_chapters()) if skip_existing else set()
        
        if generated_chapters and on_progress:
            on_progress(f"检测到已生成 {len(generated_chapters)} 章，将跳过...")

        key_chapters = [
            1,
            int(chapter_count * 0.7),
            chapter_count
        ]

        for chapter_num in key_chapters:
            if chapter_num in generated_chapters:
                if on_progress:
                    on_progress(f"跳过已存在的关键章节: 第{chapter_num}章")
                continue
                
            if on_progress:
                on_progress(f"生成关键章节: 第{chapter_num}章")

            content = await chapter_stage.execute(chapter_num)

            if on_stage_complete:
                await on_stage_complete(f"chapter_{chapter_num}", content)

        remaining_chapters = [i for i in range(1, chapter_count + 1) if i not in key_chapters and i not in generated_chapters]

        if not remaining_chapters:
            if on_progress:
                on_progress("所有章节已生成完成！")
            return

        batch_size = 5
        for i in range(0, len(remaining_chapters), batch_size):
            batch = remaining_chapters[i:i + batch_size]

            if on_progress:
                on_progress(f"批量生成章节: {batch[0]}-{batch[-1]}")

            for chapter_num in batch:
                content = await chapter_stage.execute(chapter_num)

                if on_stage_complete:
                    await on_stage_complete(f"chapter_{chapter_num}", content)

            if on_stage_complete:
                await on_stage_complete("batch_complete", {"chapters": batch})

    async def resume_generation(
        self,
        project_id: str,
        on_progress: Optional[Callable] = None,
        on_stage_complete: Optional[Callable] = None,
        enable_polish: bool = True,
        polish_requirements: Optional[str] = None
    ) -> NovelProject:
        """恢复中断的生成任务，智能检测未完成的阶段"""

        ctx = ContextManager.load_from_project_id(project_id, self.project_config.output_dir)
        project = ctx.project

        if on_progress:
            on_progress(f"恢复项目: {project_id}")
            genre_display = project.genre.value if hasattr(project.genre, 'value') else project.genre
            on_progress(f"类型: {genre_display}")
            on_progress(f"目标字数: {project.target_word_count}")
            on_progress(f"当前阶段: {project.current_stage}")

        # 检测各阶段完成情况
        stage_status = project.stage_status

        # 阶段1: 世界观构建
        if stage_status.get("worldbuilding") != "completed" and stage_status.get("世界观构建") != "completed":
            if on_progress:
                on_progress("检测到世界观未完成，开始生成...")
            world_stage = WorldBuildingStage(project, ctx, self.llm_client, self.template_manager)
            world_building = await world_stage.run(on_progress=on_progress)
            project.world_building = world_building
            if on_stage_complete:
                await on_stage_complete("worldbuilding", world_building)
        else:
            if on_progress:
                on_progress("✓ 世界观已完成")

        # 阶段2: 角色创建
        if stage_status.get("characters") != "completed" and stage_status.get("角色设定") != "completed":
            if on_progress:
                on_progress("检测到角色创建未完成，开始生成...")
            char_stage = CharacterCreationStage(project, ctx, self.llm_client, self.template_manager)
            characters = await char_stage.run(on_progress=on_progress)
            if on_stage_complete:
                await on_stage_complete("characters", characters)
        else:
            if on_progress:
                on_progress("✓ 角色创建已完成")

        # 阶段3: 情节设计
        if stage_status.get("plot") != "completed" and stage_status.get("情节设计") != "completed":
            if on_progress:
                on_progress("检测到情节设计未完成，开始生成...")
            plot_stage = PlotDesignStage(project, ctx, self.llm_client, self.template_manager)
            plot_design = await plot_stage.run(on_progress=on_progress)
            if on_stage_complete:
                await on_stage_complete("plot", plot_design)
        else:
            if on_progress:
                on_progress("✓ 情节设计已完成")

        # 阶段4: 补充配角
        if stage_status.get("supplementary_characters") != "completed" and stage_status.get("补充配角") != "completed":
            if on_progress:
                on_progress("检测到补充配角未完成，开始生成...")
            supplementary_stage = SupplementaryCharacterStage(project, ctx, self.llm_client, self.template_manager)
            supplementary_chars = await supplementary_stage.run(on_progress=on_progress)
            if on_stage_complete:
                await on_stage_complete("supplementary_characters", supplementary_chars)
        else:
            if on_progress:
                on_progress("✓ 补充配角已完成")

        # 阶段5: 大纲生成
        if stage_status.get("outline") != "completed" and stage_status.get("大纲生成") != "completed":
            if on_progress:
                on_progress("检测到大纲未完成，开始生成...")
            outline_stage = OutlineGenerationStage(project, ctx, self.llm_client, self.template_manager)
            outline = await outline_stage.run(on_progress=on_progress)
            if on_stage_complete:
                await on_stage_complete("outline", outline)
        else:
            if on_progress:
                on_progress("✓ 大纲已完成")

        # 阶段6: 章节生成（智能续传）
        chapter_count = project.target_word_count // project.words_per_chapter
        generated_chapters = ctx.get_generated_chapters()
        missing_chapters = ctx.get_missing_chapters(chapter_count)

        if on_progress:
            on_progress(f"章节进度: {len(generated_chapters)}/{chapter_count}")
            if missing_chapters:
                on_progress(f"待生成章节: {missing_chapters[:10]}{'...' if len(missing_chapters) > 10 else ''}")

        if missing_chapters:
            await self._generate_chapters_smart(
                project, ctx, chapter_count, on_progress, on_stage_complete
            )
        else:
            if on_progress:
                on_progress("✓ 所有章节已完成")

        # 阶段7: 润色与去AI化（可选）
        if enable_polish:
            polished_chapters = ctx.get_polished_chapters()
            if len(polished_chapters) < len(generated_chapters):
                if on_progress:
                    on_progress(f"润色进度: {len(polished_chapters)}/{len(generated_chapters)}")
                    on_progress("开始润色与去AI化处理...")
                polish_stage = PolishStage(project, ctx, self.llm_client, self.template_manager)
                polish_result = await polish_stage.run(
                    user_input=polish_requirements,
                    on_progress=on_progress
                )
                if on_stage_complete:
                    await on_stage_complete("polish", polish_result)
            else:
                if on_progress:
                    on_progress("✓ 润色已完成")

        if on_progress:
            on_progress("小说生成完成！")

        return project