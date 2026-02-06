import svgwrite
import math
import os
import random

# Data for 29 Stocks
# Usage: 0-100%
# Perf: -60 (Deep Dive) to +100 (Moon)
# Updated with user provided specific data
raw_data = [
    # Part 1
    ("古茗", 100, 80), # User confirmed 4 days 100%
    ("赤峰黄金", 100, 40), # User confirmed 4 days 100%
    ("绿茶集团", 100, -50),
    ("手回集团", 100, -50),
    ("海天味业", 20, -10),
    ("三花智控", 30, 10),
    ("曹操出行", 40, 60),
    ("圣贝拉", 35, -30), # User: 4.7+9+9+10+2 = 34.7%
    # Part 2
    ("颖通控股", 100, -50),
    ("奥克斯电器", 32, -40),
    ("云知声", 14, 10),
    ("天岳先进", 3, 30),
    ("大行科工", 5, -30),
    ("安井食品", 57, 60),
    ("禾赛", 6, -50),
    ("奇瑞汽车", 8, -10),
    # Part 3
    ("赛力斯", 40, -20),
    ("文远知行", 40, -20),
    ("小马智行", 75, -20), # User: 43+20+2% daily. Est ~75% total
    ("希迪智驾", 70, -60), # User: 50+6+7+7 = 70%
    ("遇见小面", 100, -50),
    ("广和通", 45, -40),
    ("京东工业", 33, 0),
    ("三一重工", 12, -5),
    # Part 4
    ("迅策", 90, 5),
    ("卧安机器人", 24, 90),
    ("智谱", 7, 80),
    ("豪威集团", 11, -10), # User: 5.5+5.5 = 11%
    ("龙旗科技", 77, 0),
]

def create_bar_chart_svg(filename, title, data, x_label, y_label):
    dwg = svgwrite.Drawing(filename, size=(900, 800))
    
    # Sort data by usage descending
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    top_10 = sorted_data[:10]
    
    width = 900
    height = 800
    margin_left = 150
    margin_right = 50
    margin_top = 80
    margin_bottom = 50
    
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    
    bar_height = 40
    gap = 20
    
    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
    
    # Title
    dwg.add(dwg.text(title, insert=(width/2, 40), text_anchor="middle", font_size=24, font_weight="bold", font_family="sans-serif"))
    
    # Axes
    # dwg.add(dwg.line(start=(margin_left, margin_top), end=(margin_left, height - margin_bottom), stroke="black", stroke_width=2))
    # dwg.add(dwg.line(start=(margin_left, height - margin_bottom), end=(width - margin_right, height - margin_bottom), stroke="black", stroke_width=2))
    
    max_val = 100
    
    for i, (name, val) in enumerate(top_10):
        y = margin_top + i * (bar_height + gap)
        bar_w = (val / max_val) * chart_width
        
        # Label
        dwg.add(dwg.text(name, insert=(margin_left - 10, y + bar_height/2 + 5), text_anchor="end", font_size=16, font_family="sans-serif"))
        
        # Bar
        color = "#e74c3c" if val >= 80 else "#f39c12" if val >= 50 else "#3498db"
        dwg.add(dwg.rect(insert=(margin_left, y), size=(bar_w, bar_height), fill=color, rx=5, ry=5))
        
        # Value
        dwg.add(dwg.text(f"{val}%", insert=(margin_left + bar_w + 10, y + bar_height/2 + 5), font_size=14, font_family="sans-serif", font_weight="bold"))

    dwg.save()
    print(f"Generated {filename}")

def create_quadrant_chart_svg(filename, title, points):
    dwg = svgwrite.Drawing(filename, size=(900, 700))
    width = 900
    height = 700
    margin = 80
    
    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
    
    # Title
    dwg.add(dwg.text(title, insert=(width/2, 40), text_anchor="middle", font_size=24, font_weight="bold", font_family="sans-serif"))
    
    # Axis Ranges
    # X: Usage 0 to 100
    # Y: Perf -60 to 100
    
    def get_x(usage):
        return margin + (usage / 100) * (width - 2 * margin)
    
    def get_y(perf):
        # Invert Y: Top is high perf (+100), Bottom is low perf (-60)
        # Range = 160
        # Normalizing: (perf - (-60)) / 160 = (perf + 60) / 160
        # SVG Y = height - margin - norm * chart_height
        chart_h = height - 2 * margin
        norm = (perf + 60) / 160
        return (height - margin) - norm * chart_h

    origin_x = get_x(50) # Midpoint of usage? Or 50%? Let's use 50% usage as separator
    origin_y = get_y(0)  # 0% performance
    
    # Quadrant Background Colors (Lighter opacity for better visibility)
    # Top Left (Low Usage, High Perf): Greenish
    dwg.add(dwg.rect(insert=(margin, margin), size=(origin_x - margin, origin_y - margin), fill="#e8f8f5", opacity=0.3))
    # Top Right (High Usage, High Perf): Yellowish
    dwg.add(dwg.rect(insert=(origin_x, margin), size=(width - margin - origin_x, origin_y - margin), fill="#fef9e7", opacity=0.3))
    # Bottom Left (Low Usage, Low Perf): Greyish
    dwg.add(dwg.rect(insert=(margin, origin_y), size=(origin_x - margin, height - margin - origin_y), fill="#f4f6f7", opacity=0.3))
    # Bottom Right (High Usage, Low Perf): Reddish
    dwg.add(dwg.rect(insert=(origin_x, origin_y), size=(width - margin - origin_x, height - margin - origin_y), fill="#fdedec", opacity=0.3))
    
    # Axes Lines
    dwg.add(dwg.line(start=(margin, origin_y), end=(width - margin, origin_y), stroke="#7f8c8d", stroke_width=2, stroke_dasharray="5,5"))
    dwg.add(dwg.line(start=(origin_x, margin), end=(origin_x, height - margin), stroke="#7f8c8d", stroke_width=2, stroke_dasharray="5,5"))
    
    # Quadrant Labels (Adjusted positions to corners to avoid data overlap)
    dwg.add(dwg.text("躺赢/真金", insert=(margin + 20, margin + 30), font_size=16, font_weight="bold", fill="#27ae60", opacity=0.8))
    dwg.add(dwg.text("逆袭/大力出奇迹", insert=(width - margin - 150, margin + 30), font_size=16, font_weight="bold", fill="#f39c12", opacity=0.8))
    dwg.add(dwg.text("弃疗/无力回天", insert=(margin + 20, height - margin - 10), font_size=16, font_weight="bold", fill="#95a5a6", opacity=0.8))
    dwg.add(dwg.text("泥潭/肉包子打狗", insert=(width - margin - 150, height - margin - 10), font_size=16, font_weight="bold", fill="#c0392b", opacity=0.8))
    
    # Axis Labels
    dwg.add(dwg.text("绿鞋使用率 (0% -> 100%)", insert=(width/2, height - 20), text_anchor="middle", font_size=14))
    dwg.add(dwg.text("上市至今涨跌幅", insert=(20, height/2), text_anchor="middle", font_size=14, transform=f"rotate(-90 20 {height/2})"))
    
    # Prepare Labels with Collision Avoidance
    labels = []
    for name, usage, perf in points:
        cx = get_x(usage)
        cy = get_y(perf)
        # Determine color based on perf
        color = "#2ecc71" if perf > 0 else "#e74c3c" if perf < 0 else "#95a5a6"
        labels.append({
            'name': name,
            'cx': cx,
            'cy': cy,
            'usage': usage,
            'perf': perf,
            'color': color,
            'lx': cx + 8,     # Initial Label X
            'ly': cy + 4,     # Initial Label Y (baseline)
            'w': len(name) * 12, # Approx width
            'h': 14           # Approx height
        })

    # Sort labels by Y primarily, then X. This helps in stacking from top to bottom.
    labels.sort(key=lambda k: (k['cy'], k['cx']))

    # Simple Iterative Collision Resolution
    # We only adjust Y to stack labels. If Y shifts too much, we might shift X? 
    # For this chart, simple vertical stacking is best for points at same location.
    
    def is_overlap(l1, l2):
        # l1, l2 are label dicts
        # Rect: x, y-10, w, h
        r1 = (l1['lx'], l1['ly'] - 10, l1['w'], l1['h'])
        r2 = (l2['lx'], l2['ly'] - 10, l2['w'], l2['h'])
        
        return not (r1[0] + r1[2] < r2[0] or \
                    r1[0] > r2[0] + r2[2] or \
                    r1[1] + r1[3] < r2[1] or \
                    r1[1] > r2[1] + r2[3])

    for i in range(len(labels)):
        current = labels[i]
        
        # Max iterations to find a spot
        for attempt in range(50):
            overlap = False
            for j in range(len(labels)):
                if i == j: continue
                other = labels[j]
                
                # Check intersection
                if is_overlap(current, other):
                    overlap = True
                    # Conflict! Move current label down
                    # But if we move it down, we might overlap with next one.
                    # It's better to verify against ALL labels, but we can only ensure non-overlap with processed ones?
                    # Actually, we can just check against everyone. 
                    # If overlap, move down by fixed step.
                    current['ly'] += 15
                    
                    # If moved too far down relative to point, maybe move to left side?
                    if current['ly'] - current['cy'] > 100:
                         # Reset Y and move Left
                         current['ly'] = current['cy'] + 4
                         current['lx'] = current['cx'] - current['w'] - 8
                         # Add flag to prevent infinite ping-pong?
                         # For now, just keep moving down is safer for "list" effect.
                    break
            
            if not overlap:
                break

    # Draw Points
    for l in labels:
        dwg.add(dwg.circle(center=(l['cx'], l['cy']), r=5, fill=l['color'], stroke="white", stroke_width=1))

    # Draw Connecting Lines (if label moved far)
    for l in labels:
        dist = math.sqrt((l['lx'] - l['cx'])**2 + (l['ly'] - l['cy'])**2)
        if dist > 20:
            # Draw line from point to label
            # Adjust start/end to look good
            label_center_y = l['ly'] - 5
            label_left_x = l['lx']
            label_right_x = l['lx'] + l['w']
            
            # If label is to the right
            if l['lx'] > l['cx']:
                dwg.add(dwg.line(start=(l['cx'], l['cy']), end=(label_left_x - 2, label_center_y), stroke="#bdc3c7", stroke_width=1))
            else:
                 dwg.add(dwg.line(start=(l['cx'], l['cy']), end=(label_right_x + 2, label_center_y), stroke="#bdc3c7", stroke_width=1))

    # Draw Labels with Halo for readability
    for l in labels:
        # Halo (thick white stroke)
        dwg.add(dwg.text(l['name'], insert=(l['lx'], l['ly']), font_size=10, font_family="sans-serif", 
                         fill="white", stroke="white", stroke_width=3, stroke_opacity=0.8))
        # Actual Text
        dwg.add(dwg.text(l['name'], insert=(l['lx'], l['ly']), font_size=10, font_family="sans-serif", 
                         fill="#2c3e50"))

    dwg.save()
    print(f"Generated {filename}")

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs("绿鞋/image/summary", exist_ok=True)
    
    # 1. Bar Chart Data (Name, Usage)
    usage_data = [(d[0], d[1]) for d in raw_data]
    create_bar_chart_svg("绿鞋/image/summary/top_usage.svg", "29只港股IPO绿鞋资金累计消耗比例 TOP10", usage_data, "累计消耗比例 (%)", "股票名称")
    
    # 2. Quadrant Chart Data (Name, Usage, Perf)
    create_quadrant_chart_svg("绿鞋/image/summary/matrix_analysis.svg", "绿鞋用量与股价表现矩阵分析 (29只样本)", raw_data)
