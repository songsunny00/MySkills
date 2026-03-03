import pytest
from src.novel_generator.config import GenerationConfig, LLMConfig, ProjectConfig
from pathlib import Path

def test_generation_config_defaults():
    config = GenerationConfig()
    assert config.target_word_count_min == 50000
    assert config.target_word_count_max == 80000
    assert config.chapter_count_min == 30
    assert config.chapter_count_max == 40

def test_llm_config_creation():
    config = LLMConfig(provider="anthropic", model="claude-sonnet-4-6")
    assert config.provider == "anthropic"
    assert config.model == "claude-sonnet-4-6"
    assert config.temperature == 0.7

def test_project_config_creation():
    config = ProjectConfig.create("/tmp/test_project")
    assert config.project_root == Path("/tmp/test_project")
    assert config.templates_dir == Path("/tmp/test_project/templates")
    assert config.output_dir == Path("/tmp/test_project/output")