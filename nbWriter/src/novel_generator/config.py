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