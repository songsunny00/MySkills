#!/usr/bin/env python
"""端到端测试：验证模板加载在实际生成流程中是否工作"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.novel_generator.config import ProjectConfig, LLMConfig
from src.novel_generator.generator import NovelGenerator
from src.novel_generator.models import NovelGenre, GenerationMode

async def test_worldbuilding_generation():
    """测试世界观生成是否使用自定义模板"""

    print("="*60)
    print("端到端测试：世界观生成")
    print("="*60)

    # 配置
    project_config = ProjectConfig.create(str(Path.cwd()))
    llm_config = LLMConfig(provider="anthropic")

    print(f"\n配置信息:")
    print(f"  templates_dir: {project_config.templates_dir}")
    print(f"  output_dir: {project_config.output_dir}")

    # 创建生成器
    generator = NovelGenerator(project_config, llm_config)

    print(f"\n生成器创建成功")
    print(f"  template_manager.templates_dir: {generator.template_manager.templates_dir}")

    # 测试模板加载（不实际调用LLM）
    print(f"\n测试模板加载:")
    template_content = generator.template_manager.get_template_content(
        "worldbuilding",
        NovelGenre.TIANYUAN_YANQING
    )

    print(f"\n模板内容检查:")
    print(f"  长度: {len(template_content)}")
    print(f"  包含'田园现代言情': {'田园现代言情' in template_content}")
    print(f"  包含'归田青年公寓': {'归田青年公寓' in template_content}")
    print(f"  包含'2020年代': {'2020年代' in template_content}")

    if '田园现代言情' in template_content:
        print(f"\n✓ 成功！使用了自定义模板")
    else:
        print(f"\n✗ 失败！使用了内置模板")
        print(f"\n前500字符:")
        print(template_content[:500])

if __name__ == "__main__":
    asyncio.run(test_worldbuilding_generation())