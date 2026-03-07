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
from src.novel_generator.context_manager import ContextManager

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

    input("\n按回车键继续...")

def list_projects(output_dir: Path):
    """列出所有项目"""
    print("\n已有项目:")
    print("-" * 40)
    
    projects = []
    for project_dir in sorted(output_dir.iterdir()):
        if project_dir.is_dir():
            metadata_file = project_dir / "metadata.json"
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                chapters_dir = project_dir / "chapters"
                chapter_count = len(list(chapters_dir.glob("chapter-*.md"))) if chapters_dir.exists() else 0
                
                print(f"  [{len(projects)+1}] {data['project_id']}")
                print(f"      类型: {data.get('genre', '未知')}")
                print(f"      目标字数: {data.get('target_word_count', '未知')}")
                print(f"      每章字数: {data.get('words_per_chapter', 2000)}")
                print(f"      已生成章节: {chapter_count}")
                print(f"      当前阶段: {data.get('current_stage', '未知')}")
                print()
                projects.append(data['project_id'])
    
    return projects

async def resume_project(project_id: str, project_config: ProjectConfig, llm_config: LLMConfig):
    """恢复项目生成"""
    print(f"\n{'='*60}")
    print(f"恢复项目: {project_id}")
    print(f"{'='*60}\n")

    # 加载项目上下文
    from .context_manager import ContextManager
    ctx = ContextManager.load_from_project_id(project_id, project_config.output_dir)

    # 询问是否更新章节标题
    print("是否更新已有章节的标题？")
    print("1. 是（推荐，统一格式）")
    print("2. 否（保持原样）")

    while True:
        update_titles_choice = input("\n请输入编号（默认1）: ").strip() or "1"
        if update_titles_choice in ["1", "2"]:
            break
        print("⚠️  请输入 1 或 2")

    if update_titles_choice == "1":
        outline_file = ctx.project_dir / "plot" / "outline.md"
        if outline_file.exists():
            print("\n正在更新章节标题...")
            outline = outline_file.read_text(encoding='utf-8')
            result = ctx.update_chapter_titles(outline, on_progress=print_progress)
            print(f"\n{result['message']}\n")
        else:
            print("\n⚠️  未找到大纲文件，跳过标题更新\n")

    # 询问是否启用润色
    print("是否启用润色与去AI化？")
    print("1. 是（推荐）")
    print("2. 否")

    while True:
        polish_choice = input("\n请输入编号（默认1）: ").strip() or "1"
        if polish_choice in ["1", "2"]:
            break
        print("⚠️  请输入 1 或 2")

    enable_polish = polish_choice == "1"

    polish_requirements = None
    if enable_polish:
        print("\n是否有特殊润色要求？（直接回车跳过）")
        polish_requirements = input("要求: ").strip() or None

    generator = NovelGenerator(project_config, llm_config)

    try:
        project = await generator.resume_generation(
            project_id=project_id,
            on_progress=print_progress,
            on_stage_complete=on_stage_complete,
            enable_polish=enable_polish,
            polish_requirements=polish_requirements
        )

        print("\n" + "="*60)
        print("小说生成完成！")
        print("="*60)
        print(f"\n项目ID: {project.project_id}")
        print(f"输出目录: {project_config.output_dir / project.project_id}")

    except FileNotFoundError as e:
        print(f"\n错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户中断生成")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

async def main():
    """主函数"""
    print("="*60)
    print(" "*15 + "一键生成小说系统")
    print("="*60)

    project_root = Path.cwd()
    project_config = ProjectConfig.create(str(project_root))
    llm_config = LLMConfig()

    print("\n请选择操作:")
    print("1. 创建新项目")
    print("2. 恢复已有项目")
    print("3. 查看项目列表")

    choice = input("\n请输入编号: ").strip()

    if choice == "2":
        projects = list_projects(project_config.output_dir)
        if not projects:
            print("\n没有找到已有项目，请先创建新项目。")
            return
        
        project_choice = input("\n请输入要恢复的项目编号: ").strip()
        try:
            idx = int(project_choice) - 1
            if 0 <= idx < len(projects):
                await resume_project(projects[idx], project_config, llm_config)
            else:
                print("无效的编号")
        except ValueError:
            print("请输入有效的数字")
        return
    
    if choice == "3":
        list_projects(project_config.output_dir)
        return

    if choice != "1":
        print("无效的选择")
        return

    print("\n请选择小说类型:")
    genres = list(NovelGenre)
    for i, genre in enumerate(genres, 1):
        print(f"{i}. {genre.value}")

    genre_choice = int(input("\n请输入编号: ")) - 1
    genre = genres[genre_choice]

    print("\n请选择生成模式:")
    print("1. 快速模式（系统自动决策）")
    print("2. 详细模式（提供详细信息）")

    mode_choice = int(input("\n请输入编号: "))
    mode = GenerationMode.QUICK if mode_choice == 1 else GenerationMode.DETAILED

    print("\n请输入目标字数（默认60000）:")
    word_count_input = input("字数: ").strip()
    target_word_count = int(word_count_input) if word_count_input else 60000

    print("\n请输入每章字数（默认2000）:")
    wpc_input = input("每章字数: ").strip()
    words_per_chapter = int(wpc_input) if wpc_input else 2000

    print("\n" + "="*60)
    print("开始生成小说...")
    print("="*60 + "\n")

    generator = NovelGenerator(project_config, llm_config)

    try:
        project = await generator.generate_novel(
            genre=genre,
            mode=mode,
            target_word_count=target_word_count,
            words_per_chapter=words_per_chapter,
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