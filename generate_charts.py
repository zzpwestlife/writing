import os

# Ensure directory exists
output_dir = "image/summary"
os.makedirs(output_dir, exist_ok=True)

def create_bar_chart_svg(filename, title, data, x_label, y_label):
    width = 800
    height = 500
    margin_left = 150
    margin_bottom = 50
    margin_top = 80
    margin_right = 50
    
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    
    max_val = max([v for k, v in data])
    bar_height = chart_height / len(data)
    bar_padding = 10
    actual_bar_height = bar_height - bar_padding
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Background
    svg += f'<rect width="100%" height="100%" fill="white"/>'
    
    # Title
    svg += f'<text x="{width/2}" y="40" text-anchor="middle" font-size="24" font-weight="bold" font-family="sans-serif">{title}</text>'
    
    # Axes
    svg += f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="black" stroke-width="2"/>'
    svg += f'<line x1="{margin_left}" y1="{height-margin_bottom}" x2="{width-margin_right}" y2="{height-margin_bottom}" stroke="black" stroke-width="2"/>'
    
    # Bars
    for i, (name, value) in enumerate(data):
        y = margin_top + i * bar_height + bar_padding/2
        bar_w = (value / max_val) * chart_width
        
        # Color based on value
        color = "#e74c3c" if value >= 80 else "#f39c12" if value >= 40 else "#2ecc71"
        
        svg += f'<rect x="{margin_left}" y="{y}" width="{bar_w}" height="{actual_bar_height}" fill="{color}"/>'
        svg += f'<text x="{margin_left - 10}" y="{y + actual_bar_height/2 + 5}" text-anchor="end" font-size="14" font-family="sans-serif">{name}</text>'
        svg += f'<text x="{margin_left + bar_w + 10}" y="{y + actual_bar_height/2 + 5}" text-anchor="start" font-size="14" font-family="sans-serif">{value}%</text>'

    # X Axis Label
    svg += f'<text x="{width/2 + margin_left/2}" y="{height-10}" text-anchor="middle" font-size="16" font-family="sans-serif">{x_label}</text>'
    
    svg += '</svg>'
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated {filename}")

def create_quadrant_chart_svg(filename, title, points):
    # Points: list of (name, x_val, y_val, color)
    # X: Greenshoe Usage (Low -> High)
    # Y: Stock Performance (Poor -> Good)
    
    width = 800
    height = 600
    margin = 60
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="100%" height="100%" fill="white"/>'
    svg += f'<text x="{width/2}" y="40" text-anchor="middle" font-size="24" font-weight="bold" font-family="sans-serif">{title}</text>'
    
    # Grid lines
    mid_x = width / 2
    mid_y = height / 2 + 20
    
    svg += f'<line x1="{margin}" y1="{mid_y}" x2="{width-margin}" y2="{mid_y}" stroke="gray" stroke-width="2" stroke-dasharray="5,5"/>'
    svg += f'<line x1="{mid_x}" y1="{margin+40}" x2="{mid_x}" y2="{height-margin}" stroke="gray" stroke-width="2" stroke-dasharray="5,5"/>'
    
    # Quadrant Labels
    svg += f'<text x="{width-margin}" y="{mid_y-10}" text-anchor="end" font-weight="bold" fill="gray">表现优异</text>'
    svg += f'<text x="{width-margin}" y="{mid_y+20}" text-anchor="end" font-weight="bold" fill="gray">表现不佳</text>'
    svg += f'<text x="{margin}" y="{margin+50}" text-anchor="start" font-weight="bold" fill="gray">绿鞋用量少</text>'
    svg += f'<text x="{width-margin}" y="{margin+50}" text-anchor="end" font-weight="bold" fill="gray">绿鞋用量多</text>'

    # Plot points
    # Map input 0-100 to canvas coordinates
    # X: 0 -> margin, 100 -> width-margin
    # Y: -50 -> height-margin, 50 -> margin+40 (inverted Y)
    
    for name, usage, perf, color in points:
        # Normalize usage (0-100)
        cx = margin + (usage / 100) * (width - 2*margin)
        
        # Normalize performance (-50 to 50 approx range for display)
        # perf is roughly -30 to +30. Let's map -50 to height-margin, +50 to margin+40
        cy = (height - margin) - ((perf + 50) / 100) * (height - 2*margin - 40)
        
        svg += f'<circle cx="{cx}" cy="{cy}" r="6" fill="{color}" stroke="black" stroke-width="1"/>'
        svg += f'<text x="{cx+8}" y="{cy+4}" font-size="12" font-family="sans-serif">{name}</text>'

    svg += '</svg>'
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated {filename}")

# Data for Chart 1: Top Usage (First Day/Early)
usage_data = [
    ("绿茶集团", 100),
    ("手回集团", 100),
    ("遇见小面", 100),
    ("颖通控股", 100),
    ("迅策", 90),
    ("古茗", 81),
    ("安井食品", 57),
    ("广和通", 45),
    ("龙旗科技", 42),
    ("赛力斯", 40),
]

# Data for Chart 2: Outcome Scatter (Approximate data for visualization)
# Usage (0-100), Performance (-50 to 50 score)
# Color: Red (Bad), Green (Good), Yellow (Neutral)
scatter_data = [
    ("曹操出行", 30, 40, "#2ecc71"), # Good perf, mod usage
    ("卧安机器人", 24, 30, "#2ecc71"),
    ("天岳先进", 3, 20, "#2ecc71"),
    ("三一重工", 12, 5, "#f1c40f"), # Stable
    ("京东工业", 33, 0, "#f1c40f"), # Stable
    ("龙旗科技", 42, 0, "#f1c40f"), # Stable at IPO price
    ("古茗", 81, -10, "#e74c3c"), # Initial drop
    ("手回集团", 100, -30, "#e74c3c"), # Drop
    ("绿茶集团", 100, -25, "#e74c3c"), # Drop
    ("禾赛", 6, -40, "#95a5a6"), # Gave up
    ("希迪智驾", 0, -45, "#95a5a6"), # Gave up
    ("智谱", 7, 10, "#f1c40f"), # Recovered
]

if __name__ == "__main__":
    create_bar_chart_svg("top_usage.svg", "IPO首日/初期绿鞋资金消耗比例 TOP10", usage_data, "消耗比例 (%)", "股票名称")
    create_quadrant_chart_svg("matrix_analysis.svg", "绿鞋用量与股价表现矩阵分析", scatter_data)
