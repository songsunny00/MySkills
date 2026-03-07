from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NovelGenre(str, Enum):
    """小说类型"""
    XUANHUAN = "xuanhuan"  # 玄幻
    DUSHI = "dushi"  # 都市
    YANQING = "yanqing"  # 言情
    TIANYUAN_YANQING = "tianyuan_yanqing"  # 田园现代言情
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
    words_per_chapter: int = 2000

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
    polished_chapters: List[int] = Field(default_factory=list)  # 已润色的章节列表

    class Config:
        use_enum_values = True