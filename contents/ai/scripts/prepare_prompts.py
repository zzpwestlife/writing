import os

STYLE_LIGHT_PATH = "/Users/joeyzou/Code/OpenSource/writing/.claude/skills/smart-illustrator/styles/style-light.md"
STYLE_COVER_PATH = "/Users/joeyzou/Code/OpenSource/writing/.claude/skills/smart-illustrator/styles/style-cover.md"
OUTPUT_DIR = "/Users/joeyzou/Code/OpenSource/writing/contents/ai/scripts/prompts"

def read_style_prompt(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Extract the content inside the first ``` code block which usually contains the system prompt
        try:
            start = content.index("```") + 3
            end = content.index("```", start)
            return content[start:end].strip()
        except ValueError:
            return content

style_light = read_style_prompt(STYLE_LIGHT_PATH)
style_cover = read_style_prompt(STYLE_COVER_PATH)

prompts = [
    {
        "filename": "cover.txt",
        "system": style_cover,
        "content": """
**内容**：
- 核心概念：人机协作的四个进化阶段
- 视觉隐喻：分屏图，左边是满头大汗驾驶老式汽车的人，右边是充满未来感的自动驾驶座舱，乘客在悠闲喝咖啡
- 平台：公众号封面 (2.35:1)
"""
    },
    {
        "filename": "stage1.txt",
        "system": style_light,
        "content": """
**内容**：
第一阶段：独行时代 (Human Driving)
- 场景：复古风格，一位司机全神贯注地驾驶，周围路况复杂
- 隐喻：方向盘在自己手中，路在脚下
- 核心：独立承担疲劳与风险
"""
    },
    {
        "filename": "stage2.txt",
        "system": style_light,
        "content": """
**内容**：
第二阶段：辅助驾驶 (AI Copilot)
- 场景：驾驶员依然手握方向盘，但旁边有一个全息投影的机器人指着地图
- 隐喻：AI 是智能副驾，提供导航和提醒
- 核心：人类主导，AI 辅助
"""
    },
    {
        "filename": "stage3.txt",
        "system": style_light,
        "content": """
**内容**：
第三阶段：人机共驾 (AI Pilot)
- 场景：驾驶座上坐着 AI，人类坐在副驾或后排，手持平板电脑指挥，神态轻松
- 隐喻：AI 接管主驾，人类晋升指挥官
- 核心：人类监督与决策
"""
    },
    {
        "filename": "stage4.txt",
        "system": style_light,
        "content": """
**内容**：
第四阶段：全自动驾驶 (Auto Pilot)
- 场景：充满科幻感的无人驾驶舱，人类在舒适的座椅上睡觉或欣赏窗外的星空
- 隐喻：设定目的地，然后安心入睡
- 核心：AI 完全自主，人类享受自由
"""
    }
]

for p in prompts:
    full_prompt = f"{p['system']}\n\n{p['content']}"
    with open(os.path.join(OUTPUT_DIR, p['filename']), 'w', encoding='utf-8') as f:
        f.write(full_prompt)
    print(f"Generated {p['filename']}")
