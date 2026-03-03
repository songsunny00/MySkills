# 一键生成小说系统 - 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标**: 实现一个完整的中长篇小说（50,000-80,000字）自动化生成系统，支持分阶段确认和全面的用户控制。

**架构**: 采用模块化设计，每个生成阶段独立封装，通过统一的上下文管理器维护全局状态。使用提示词模板系统支持不同类型的小说生成，文件系统作为持久化存储。

**技术栈**:
- Python 3.10+
- LLM API (Claude/OpenAI)
- Jinja2 (提示词模板)
- Markdown (文档格式)
- JSON (配置和元数据)

---

## Task 1: 项目基础结构搭建

**Files:**
- Create: `src/novel_generator/__init__.py`
- Create: `src/novel_generator/config.py`
- Create: `src/novel_generator/models.py`
- Create: `tests/test_config.py`
- Create: `requirements.txt`
- Create: `README.md`

**Step 1: 创建项目目录结构**

```bash
mkdir -p src/novel_generator
mkdir -p src/novel_generator/stages
mkdir -p src/novel_generator/templates
mkdir -p src/novel_generator/utils
mkdir -p tests
mkdir -p examples
```

**Step 2: 编写 requirements.txt**

```txt
anthropic>=0.18.0
openai>=1.12.0
jinja2>=3.1.3
pydantic>=2.6.0
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

**Step 3: 创建配置模块**

在 `src/novel_generator/config.py`:

```python
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class GenerationConfig(BaseModel):
    """生成配置"""
    target_word_count_min: int = 50000
    target_word_count_max: int = 80000
    chapter_count_min: int = 30
    chapter_count_max: int = 40
    words_per_chapter_avg: int = 2000

class LLMConfig(BaseModel):
    """LLM配置"""
    provider: str = "anthropic"  # anthropic or openai
    model: str = "claude-sonnet-4-6"
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000

    def __init__(self, **data):
        super().__init__(**data)
        if not self.api_key:
            if self.provider == "anthropic":
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
            elif self.provider == "openai":
                self.api_key = os.getenv("OPENAI_API_KEY")

class ProjectConfig(BaseModel):
    """项目配置"""
    project_root: Path
    templates_dir: Path
    output_dir: Path

    @classmethod
    def create(cls, project_root: str):
        root = Path(project_root)
        return cls(
            project_root=root,
            templates_dir=root / "templates",
            output_dir=root / "output"
        )
```

**Step 4: 编写数据模型**

在 `src/novel_generator/models.py`:

```python
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NovelGenre(str, Enum):
    """小说类型"""
    XUANHUAN = "xuanhuan"  # 玄幻
    DUSHI = "dushi"  # 都市
    YANQING = "yanqing"  # 言情
    KEHUAN = "kehuan"  # 科幻
    WUXIA = "wuxia"  # 武侠
    XUANYI = "xuanyi"  # 悬疑
    LISHI = "lishi"  # 历史
    YOUXI = "youxi"  # 游戏

class GenerationMode(str, Enum):
    """生成模式"""
    QUICK = "quick"  # 快速模式
    DETAILED = "detailed"  # 详细模式

class StageStatus(str, Enum):
    """阶段状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Character(BaseModel):
    """角色模型"""
    name: str
    role: str  # protagonist, supporting, antagonist
    age: Optional[int] = None
    appearance: str = ""
    personality: str = ""
    background: str = ""
    abilities: List[str] = Field(default_factory=list)
    growth_arc: str = ""
    relationships: Dict[str, str] = Field(default_factory=dict)

class PlotLine(BaseModel):
    """情节线"""
    type: str  # main, sub, emotional, growth
    description: str
    key_events: List[str] = Field(default_factory=list)

class ChapterOutline(BaseModel):
    """章节大纲"""
    chapter_number: int
    title: str
    summary: str
    word_count_target: int
    plot_points: List[str] = Field(default_factory=list)
    characters_involved: List[str] = Field(default_factory=list)
    is_key_chapter: bool = False

class NovelProject(BaseModel):
    """小说项目"""
    project_id: str
    title: str = ""
    genre: NovelGenre
    mode: GenerationMode
    target_word_count: int

    # 生成内容
    world_building: str = ""
    characters: List[Character] = Field(default_factory=list)
    plot_lines: List[PlotLine] = Field(default_factory=list)
    outline: List[ChapterOutline] = Field(default_factory=list)
    chapters: Dict[int, str] = Field(default_factory=dict)

    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    current_stage: str = "init"
    stage_status: Dict[str, StageStatus] = Field(default_factory=dict)

    class Config:
        use_enum_values = True
```

**Step 5: 编写测试**

在 `tests/test_config.py`:

```python
import pytest
from src.novel_generator.config import GenerationConfig, LLMConfig, ProjectConfig
from pathlib import Path

def test_generation_config_defaults():
    config = GenerationConfig()
    assert config.target_word_count_min == 50000
    assert config.target_word_count_max == 80000
    assert config.chapter_count_min == 30

def test_llm_config_creation():
    config = LLMConfig(provider="anthropic", model="claude-sonnet-4-6")
    assert config.provider == "anthropic"
    assert config.temperature == 0.7

def test_project_config_creation():
    config = ProjectConfig.create("/tmp/test_project")
    assert config.project_root == Path("/tmp/test_project")
    assert config.templates_dir == Path("/tmp/test_project/templates")
```

**Step 6: 运行测试**

```bash
pytest tests/test_config.py -v
```

预期: 所有测试通过

**Step 7: 提交**

```bash
git add src/ tests/ requirements.txt
git commit -m "feat: 添加项目基础结构和配置模块"
```

---

## Task 2: 上下文管理器

**Files:**
- Create: `src/novel_generator/context_manager.py`
- Create: `tests/test_context_manager.py`

**Step 1: 编写上下文管理器**

在 `src/novel_generator/context_manager.py`:

```python
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
```

**Step 2: 编写测试**
