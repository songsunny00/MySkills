#!/usr/bin/env python
"""
断点续传示例
演示如何恢复中断的小说生成任务
"""
import asyncio
from pathlib import Path
from src.novel_generator.config import LLMConfig, ProjectConfig
from src.novel_generator.generator import NovelGenerator
from src.novel_generator.context_manager import ContextManager

def print_progress(message: str):
    """打印进度信息"""
    print(f"[进度] {message}")

async def resume_example():
    """恢复项目生成示例"""

    # 配置
    project_root = Path.cwd()
    project_config = ProjectConfig.create(str(project_root))
    llm_config = LLMConfig(provider="anthropic", model="claude-sonnet-4-6")

    # 要恢复的项目ID（替换为你的实际项目ID）
    project_id = "novel_eb2d33af"

    # 检查项目是否存在
    try:
        ctx = ContextManager.load_from_project_id(project_id, project_config.output_dir)
        project = ctx.project

        print("="*60)
        print(f"项目信息: {project_id}")
        print("="*60)
        print(f"类型: {project.genre.value}")
        print(f"目标字数: {project.target_word_count}")
        print(f"当前阶段: {project.current_stage}")
        print(f"阶段状态: {project.stage_status}")
        print(f"已生成章节: {len(ctx.get_generated_chapters())}")
        print(f"已润色章节: {len(ctx.get_polished_chapters())}")

        # 显示缺失的章节
        chapter_count = project.target_word_count // 2000
        missing = ctx.get_missing_chapters(chapter_count)
        if missing:
            print(f"缺失章节: {missing[:10]}{'...' if len(missing) > 10 else ''}")

        print("\n开始恢复生成...")
        print("="*60 + "\n")

    except FileNotFoundError:
        print(f"错误: 项目 {project_id} 不存在")
        print(f"请检查 {project_config.output_dir} 目录")
        return

    # 创建生成器并恢复
    generator = NovelGenerator(project_config, llm_config)

    try:
        project = await generator.resume_generation(
            project_id=project_id,
            enable_polish=True,  # 启用润色
            polish_requirements="保持田园风格，增加五感细节",
            on_progress=print_progress
        )

        print("\n" + "="*60)
        print("✅ 小说生成完成！")
        print("="*60)
        print(f"项目ID: {project.project_id}")
        print(f"输出目录: {project_config.output_dir / project.project_id}")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断生成（进度已保存）")
        print(f"可再次运行此脚本继续生成")
    except Exception as e:
        print(f"\n\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(resume_example())