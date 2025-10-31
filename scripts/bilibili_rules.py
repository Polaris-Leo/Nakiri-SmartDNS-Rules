import requests
import yaml
import os
from datetime import datetime

# 输出文件夹和文件名
output_dir = "ios_rules"
output_file_name = "bilibili.conf"
output_file_path = os.path.join(output_dir, output_file_name)

# 源规则 URL
url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/BiliBili/BiliBili.yaml"

# 有效类型
valid_types = ["DOMAIN-SUFFIX", "DOMAIN", "DOMAIN-KEYWORD"]

print(f"[{datetime.now()}] Fetching Bilibili rules from {url}...")
domain_list = []

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = yaml.safe_load(response.text)
    payload = data.get('payload', [])
    for item in payload:
        parts = item.split(',')
        if len(parts) == 2 and parts[0] in valid_types:
            domain_list.append(parts[1].strip())

except Exception as e:
    print(f"An error occurred: {e}")

os.makedirs(output_dir, exist_ok=True)
with open(output_file_path, 'w', encoding='utf-8') as f:
    for d in domain_list:
        f.write(d + '\n')

print(f"[{datetime.now()}] Processed {len(domain_list)} Bilibili domains → {output_file_path}")
