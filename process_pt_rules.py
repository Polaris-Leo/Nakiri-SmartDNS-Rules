import requests
import yaml
import os

# 定义输出文件夹和文件名（后缀已改为 .conf）
output_dir = "ios_rules"
output_file_name = "pt_domains.conf" # <--- 文件名已更改
output_file_path = os.path.join(output_dir, output_file_name)

# 源文件 URL
url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/PrivateTracker/PrivateTracker.yaml"

# 定义需要提取的规则类型
valid_types = ["DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"]

print(f"Fetching rules from {url}...")
domain_list = [] # 将列表初始化移到 try 外部

try:
    # 发送请求获取文件内容
    response = requests.get(url)
    response.raise_for_status()

    # 使用 PyYAML 解析 YAML 内容
    data = yaml.safe_load(response.text)

    # 提取 payload 列表
    payload = data.get('payload', [])
    
    if payload:
        for item in payload:
            parts = item.split(',')
            if len(parts) == 2 and parts[0] in valid_types:
                domain_list.append(parts[1].strip())

except Exception as e:
    # 即使在处理过程中发生错误，也打印日志，但流程会继续以创建文件
    print(f"An error occurred during processing: {e}")

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 无论是否成功获取域名，都创建或覆盖文件
# 这样可以保证即使列表为空，文件也存在
with open(output_file_path, 'w', encoding='utf-8') as f:
    if domain_list:
        for domain in domain_list:
            f.write(domain + '\n')
        print(f"Successfully processed {len(domain_list)} domains.")
    else:
        # 如果列表为空，写入一个空文件并打印警告
        print("Warning: No domains were extracted. An empty conf file will be created.")
        
print(f"Result saved to {output_file_path}")
