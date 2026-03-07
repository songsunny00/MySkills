#!/usr/bin/env python
"""测试模板加载诊断"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.novel_generator.config import ProjectConfig
from src.novel_generator.prompt_templates import PromptTemplateManager
from src.novel_generator.models import NovelGenre

print("="*60)
print("模板加载诊断测试")
print("="*60)

# 创建配置
project_config = ProjectConfig.create(str(Path.cwd()))
print(f"\n项目根目录: {project_config.project_root}")
print(f"模板目录: {project_config.templates_dir}")
print(f"模板目录存在: {project_config.templates_dir.exists()}")

# 列出模板目录内容
if project_config.templates_dir.exists():
    print(f"\n模板目录内容:")
    for item in project_config.templates_dir.iterdir():
        print(f"  - {item.name}")

# 创建模板管理器
template_manager = PromptTemplateManager(project_config.templates_dir)

# 测试加载 worldbuilding 模板
print("\n" + "="*60)
print("测试1: 加载 worldbuilding 模板 (genre=tianyuan_yanqing)")
print("="*60)
content = template_manager.get_template_content("worldbuilding", NovelGenre.TIANYUAN_YANQING)

# 检查内容特征
print(f"\n模板内容前200字符:")
print(content[:200])
print(f"\n是否包含'田园现代言情': {'田园现代言情' in content}")
print(f"是否包含'归田青年公寓': {'归田青年公寓' in content}")