import pytest
import tempfile
import shutil
from pathlib import Path
from src.novel_generator.context_manager import ContextManager
from src.novel_generator.models import NovelProject, NovelGenre, GenerationMode, StageStatus

@pytest.fixture
def temp_output_dir():
    """创建临时输出目录"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_project():
    """创建示例项目"""
    return NovelProject(
        project_id="test_project_001",
        title="测试小说",
        genre=NovelGenre.XUANHUAN,
        mode=GenerationMode.QUICK,
        target_word_count=60000
    )

def test_context_manager_initialization(temp_output_dir, sample_project):
    """测试上下文管理器初始化"""
    ctx = ContextManager(sample_project, temp_output_dir)

    assert ctx.project_dir.exists()
    assert (ctx.project_dir / "worldbuilding").exists()
    assert (ctx.project_dir / "characters").exists()
    assert (ctx.project_dir / "chapters").exists()

def test_save_and_load_metadata(temp_output_dir, sample_project):
    """测试保存和加载元数据"""
    ctx = ContextManager(sample_project, temp_output_dir)
    ctx.save_metadata()

    loaded_project = ctx.load_metadata()
    assert loaded_project.project_id == sample_project.project_id
    assert loaded_project.title == sample_project.title

def test_update_stage_status(temp_output_dir, sample_project):
    """测试更新阶段状态"""
    ctx = ContextManager(sample_project, temp_output_dir)
    ctx.update_stage_status("worldbuilding", StageStatus.COMPLETED)

    assert ctx.project.current_stage == "worldbuilding"
    assert ctx.project.stage_status["worldbuilding"] == StageStatus.COMPLETED

def test_save_world_building(temp_output_dir, sample_project):
    """测试保存世界观"""
    ctx = ContextManager(sample_project, temp_output_dir)
    world_content = "这是一个修仙世界..."
    ctx.save_world_building(world_content)

    world_file = ctx.project_dir / "worldbuilding" / "world.md"
    assert world_file.exists()
    assert world_file.read_text(encoding='utf-8') == world_content

def test_save_and_get_chapter(temp_output_dir, sample_project):
    """测试保存和获取章节"""
    ctx = ContextManager(sample_project, temp_output_dir)
    chapter_content = "# 第一章\n\n这是第一章的内容..."
    ctx.save_chapter(1, chapter_content)

    retrieved_content = ctx.get_chapter(1)
    assert retrieved_content == chapter_content

    # 测试获取不存在的章节
    assert ctx.get_chapter(999) is None