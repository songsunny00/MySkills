from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
from typing import Dict, Any, Optional
from .models import NovelGenre

class PromptTemplateManager:
    """提示词模板管理器"""

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(str(templates_dir)))

    def render(self, template_name: str, **kwargs) -> str:
        """渲染模板"""
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

    def render_string(self, template_str: str, **kwargs) -> str:
        """渲染字符串模板"""
        template = Template(template_str)
        return template.render(**kwargs)


# 内置模板（如果文件不存在则使用）
BUILTIN_TEMPLATES = {
    "worldbuilding": """你是一位资深的小说世界观设计师。请为以下小说创建详细的世界观设定。

**小说类型**: {{ genre }}
**生成模式**: {{ mode }}
{% if user_input %}
**用户输入**: {{ user_input }}
{% endif %}

请创建包含以下内容的世界观设定：
1. 时代背景（时间、地点、历史背景）
2. 地理设定（主要地点、地理特征）
3. 力量体系（如果适用于该类型）
4. 社会结构（政治、经济、文化）
5. 独特元素（该世界的特色设定）

要求：
- 设定要符合{{ genre }}类型的特点
- 内容详细但不冗长（800-1200字）
- 为后续情节发展留出空间
- 设定要有内在逻辑性

请以Markdown格式输出。
""",

    "character_creation": """你是一位资深的小说角色设计师。请为以下小说创建角色设定。

**小说类型**: {{ genre }}
**角色类型**: {{ role }}  {# protagonist, supporting, antagonist #}
**世界观**:
{{ world_building }}

{% if user_input %}
**用户要求**: {{ user_input }}
{% endif %}

请创建包含以下内容的角色档案：
1. 基本信息（姓名、年龄、外貌）
2. 性格特征（3-5个关键特质）
3. 背景故事（成长经历、重要事件）
4. 能力/特长（符合世界观设定）
5. 成长弧线（角色在故事中的变化方向）
6. 与其他角色的关系（如果已有其他角色）

要求：
- 角色要立体、有深度
- 性格要有优点也有缺点
- 背景故事要能引发情节
- 符合{{ genre }}类型的角色特点

请以Markdown格式输出。
""",

    "plot_design": """你是一位资深的小说情节设计师。请为以下小说设计情节框架。

**小说类型**: {{ genre }}
**目标字数**: {{ target_word_count }}
**世界观**:
{{ world_building }}

**主要角色**:
{% for char in characters %}
- {{ char.name }} ({{ char.role }}): {{ char.personality[:100] }}
{% endfor %}

{% if user_input %}
**用户要求**: {{ user_input }}
{% endif %}

请设计包含以下内容的情节框架：
1. 核心冲突（故事的主要矛盾）
2. 主线情节（3-5个关键情节点）
3. 副线情节（2-3条，丰富故事层次）
4. 情感线（角色关系发展）
5. 成长线（主角的成长路径）
6. 高潮设计（故事的最高点）
7. 结局方向（开放式/封闭式）

要求：
- 情节要有起承转合
- 冲突要层层递进
- 符合{{ genre }}类型的情节特点
- 为{{ target_word_count }}字的篇幅设计合理节奏

请以Markdown格式输出。
""",

    "outline_generation": """你是一位资深的小说大纲设计师。请为以下小说创建详细的章节大纲。

**小说类型**: {{ genre }}
**目标字数**: {{ target_word_count }}
**目标章节数**: {{ chapter_count }}

**世界观**:
{{ world_building }}

**情节框架**:
{{ plot_design }}

请创建详细的章节大纲，每章包含：
1. 章节标题
2. 章节概要（200-300字）
3. 关键情节点
4. 涉及的主要角色
5. 目标字数

要求：
- 总共{{ chapter_count }}章
- 平均每章{{ words_per_chapter }}字
- 标注关键章节（开篇、转折、高潮、结局）
- 情节分布要合理，节奏要有张弛
- 确保情节连贯性

请以Markdown格式输出，每章用二级标题分隔。
""",

    "chapter_generation": """你是一位资深的网络小说作家。请根据大纲创作以下章节。

**小说类型**: {{ genre }}
**章节号**: 第{{ chapter_number }}章
**章节标题**: {{ chapter_title }}
**章节大纲**:
{{ chapter_outline }}

**上下文信息**:
{{ context_summary }}

{% if previous_chapter %}
**上一章结尾**:
{{ previous_chapter[-500:] }}
{% endif %}

**创作要求**:
1. 目标字数: {{ target_word_count }}字（±10%）
2. 符合{{ genre }}类型的写作风格
3. 情节要推进，不要原地踏步
4. 对话要自然，符合角色性格
5. 描写要生动，但不要过度
6. 保持与前文的连贯性
7. 章节结尾要有钩子，吸引读者继续阅读

请直接输出章节内容，以"# 第{{ chapter_number }}章 {{ chapter_title }}"开头。
""",

    "polish": """你是一位经验丰富的网络小说编辑。请对以下章节进行润色，去除AI生成的痕迹。

**小说类型**: {{ genre }}
**章节号**: 第{{ chapter_number }}章

**润色重点**:
1. 去除机械重复的句式
2. 去除过度修饰和形容词堆砌
3. 去除说教感和情绪标签
4. 增加真实细节和五感描写
5. 让对话更自然，有停顿和省略
6. 保持情节不变，字数相近（±15%）

**原始内容**:
{{ original_content }}

{% if user_requirements %}
**特殊要求**: {{ user_requirements }}
{% endif %}

请输出润色后的完整章节，直接以"# 第{{ chapter_number }}章"开头。
"""
}


def get_template_content(template_name: str, templates_dir: Optional[Path] = None) -> str:
    """获取模板内容（优先使用文件，否则使用内置模板）"""
    if templates_dir:
        template_file = templates_dir / f"{template_name}.jinja2"
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')

    return BUILTIN_TEMPLATES.get(template_name, "")