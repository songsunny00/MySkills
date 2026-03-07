#!/usr/bin/env python
"""测试模板加载是否正确"""
from pathlib import Path
from src.novel_generator.config import ProjectConfig
from src.novel_generator.prompt_templates import PromptTemplateManager
from src.novel_generator.models import NovelGenre

# 创建配置
project_config = ProjectConfig.create(str(Path.cwd()))

print("="*60)
print("模板加载测试")
print("="*60)
print(f"项目根目录: {project_config.project_root}")
print(f"模板目录: {project_config.templates_dir}")
print(f"模板目录是否存在: {project_config.templates_dir.exists()}")
print()

# 创建模板管理器
template_manager = PromptTemplateManager(project_config.templates_dir)

# 测试加载 tianyuan_yanqing 的 chapter_generation 模板
genre = NovelGenre.TIANYUAN_YANQING
template_content = template_manager.get_template_content("chapter_generation", genre)

print(f"Genre: {genre.value}")
print(f"模板长度: {len(template_content)} 字符")
print()

# 检查是否是自定义模板（包含特定标记）
if "田园现代言情" in template_content:
    print("✓ 成功加载自定义模板（包含'田园现代言情'标记）")
elif "序章（第1-3章）" in template_content:
    print("✓ 成功加载自定义模板（包含'序章'标记）")
else:
    print("✗ 加载的是内置模板（未找到自定义标记）")
    print("\n前500字符:")
    print(template_content[:500])