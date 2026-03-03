#!/usr/bin/env python
"""
一键生成小说 CLI工具
"""
import asyncio
import sys
from pathlib import Path
from src.novel_generator.models import NovelGenre, GenerationMode
from src.novel_generator.config import LLMConfig, ProjectConfig
from src.novel_generator.generator import NovelGenerator

def print_progress(message: str):
    """打印进度信息"""
    print(f"[进度] {message}")

async def on_stage_complete(stage_name: str, result):
    """阶段完成回调"""
    print(f"\n{'='*50}")
    print(f"[完成] {stage_name} 阶段完成")
    print(f"{'='*50}\n")

    if isinstance(result, str) and len(result) < 500:
        print(result[:500])
    elif isinstance(result, list):
        print(f"生成了 {len(result)} 个项目")

    # 等待用户确认
    input("\n按回车键继续...")

async def main():
    """主函数"""
    print("="*60)
    print(" "*15 + "一键生成小说系统")
    print("="*60)

    # 1. 选择类型
    print("\n请选择小说类型:")
    genres = list(NovelGenre)
    for i, genre in enumerate(genres, 1):
        print(f"{i}. {genre.value}")

    genre_choice = int(input("\n请输入编号: ")) - 1
    genre = genres[genre_choice]

    # 2. 选择模式
    print("\n请选择生成模式:")
    print("1. 快速模式（系统自动决策）")
    print("2. 详细模式（提供详细信息）")

    mode_choice = int(input("\n请输入编号: "))
    mode = GenerationMode.QUICK if mode_choice == 1 else GenerationMode.DETAILED

    # 3. 设置字数
    print("\n请输入目标字数（默认60000）:")
    word_count_input = input("字数: ").strip()
    target_word_count = int(word_count_input) if word_count_input else 60000

    # 4. 配置
    project_root = Path.cwd()
    project_config = ProjectConfig.create(str(project_root))
    llm_config = LLMConfig()

    # 5. 开始生成
    print("\n" + "="*60)
    print("开始生成小说...")
    print("="*60 + "\n")

    generator = NovelGenerator(project_config, llm_config)

    try:
        project = await generator.generate_novel(
            genre=genre,
            mode=mode,
            target_word_count=target_word_count,
            on_progress=print_progress,
            on_stage_complete=on_stage_complete
        )

        print("\n" + "="*60)
        print("小说生成完成！")
        print("="*60)
        print(f"\n项目ID: {project.project_id}")
        print(f"输出目录: {project_config.output_dir / project.project_id}")

    except KeyboardInterrupt:
        print("\n\n用户中断生成")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())