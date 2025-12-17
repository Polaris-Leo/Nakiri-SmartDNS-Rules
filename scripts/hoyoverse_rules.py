import requests
import yaml
import os
from datetime import datetime

# =====================
# 输出配置
# =====================
output_dir = "ios_rules"
output_file_name = "hoyoverse.conf"
output_file_path = os.path.join(output_dir, output_file_name)

# =====================
# 源规则 URL
# =====================
url = (
    "https://raw.githubusercontent.com/blackmatrix7/"
    "ios_rule_script/master/rule/Clash/HoYoverse/HoYoverse.yaml"
)

# =====================
# 允许的规则类型
# =====================
valid_types = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD"
}

print(f"[{datetime.now()}] Fetching HoYoverse rules from {url}")

domain_list = []

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = yaml.safe_load(response.text)
    payload = data.get("payload", [])

    for item in payload:
        # 例：DOMAIN-SUFFIX,mihoyo.com
        parts = item.split(",", 1)
        if len(parts) != 2:
            continue

        rule_type, value = parts
        rule_type = rule_type.strip()
        value = value.strip()

        if rule_type in valid_types and value:
            domain_list.append(value)

except Exception as e:
    print(f"[ERROR] Failed to fetch or parse rules: {e}")

# =====================
# 写入文件
# =====================
os.makedirs(output_dir, exist_ok=True)

with open(output_file_path, "w", encoding="utf-8") as f:
    for domain in sorted(set(domain_list)):
        f.write(domain + "\n")

print(
    f"[{datetime.now()}] "
    f"Processed {len(set(domain_list))} HoYoverse domains → {output_file_path}"
)
