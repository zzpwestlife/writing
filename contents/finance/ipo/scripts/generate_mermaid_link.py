import base64

graph = """graph TD
    A[总股本 Total Share Capital] --> B[非上市流通股 Unlisted Shares]
    A --> C[全球发售 Global Offering]
    B --> B1[创始人/管理层]
    B --> B2[Pre-IPO 投资者]
    C --> D[基石投资者 Cornerstone]
    C --> E[流通部分 Tradable Portion]
    E --> F[国际配售 Institutional]
    E --> G[公开发售 Public Offer]
    E --> H[绿鞋 Green Shoe]
    
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#bfb,stroke:#333,stroke-width:2px"""

graph_bytes = graph.encode('utf-8')
base64_bytes = base64.urlsafe_b64encode(graph_bytes)
base64_string = base64_bytes.decode('ascii')

print(f"https://mermaid.ink/img/{base64_string}")
