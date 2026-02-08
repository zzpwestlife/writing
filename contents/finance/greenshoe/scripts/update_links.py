import re
import os

# ---------------- 配置区域 ----------------
# 如果您更换了 GitHub 账号或仓库，请在此修改
NEW_GITHUB_USER = "zzpwestlife"  # 您的 GitHub 用户名
NEW_REPO_NAME = "writing"        # 您的仓库名
NEW_BRANCH = "main"              # 分支名
# ----------------------------------------

TARGET_FILES = [
    "../content/港股_IPO_绿鞋机制深度解析_wechat.md",
    "../content/港股_IPO_绿鞋机制深度解析_part2_wechat.md",
    "../content/港股_IPO_绿鞋机制深度解析_part3_wechat.md",
    "../content/港股_IPO_绿鞋机制深度解析_part4_wechat.md",
    "../content/港股_IPO_绿鞋机制_阶段性复盘总结_wechat.md"
]

def update_links():
    base_url = f"https://raw.githubusercontent.com/{NEW_GITHUB_USER}/{NEW_REPO_NAME}/{NEW_BRANCH}/"
    
    print(f"准备将图片链接更新为: {base_url}...")

    for file_path in TARGET_FILES:
        if not os.path.exists(file_path):
            print(f"跳过（文件不存在）: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 正则替换：匹配 https://raw.githubusercontent.com/.*?/.*?/.*?/
        # 并替换为新的 base_url
        new_content = re.sub(
            r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/',
            base_url,
            content
        )
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已更新: {file_path}")
        else:
            print(f"无需更新: {file_path}")

if __name__ == "__main__":
    update_links()
