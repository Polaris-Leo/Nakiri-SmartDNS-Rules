import requests
import os
from datetime import datetime

# 输出目录和文件
output_dir = "smartdns_domain_lists"
output_file_name = "china.conf"
output_file_path = os.path.join(output_dir, output_file_name)

# 源 URL
url = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/refs/heads/master/accelerated-domains.china.conf"

print(f"[{datetime.now()}] Fetching China accelerated domain list from {url}...")

domain_list = []

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    for line in response.text.splitlines():
        line = line.strip()
        # 提取 "server=/example.com/" 这一部分
        if line.startswith("server=/") and "/" in line[8:]:
            try:
                domain = line.split("/")[1]
                if domain and not domain.startswith("#"):
                    domain_list.append(domain)
            except Exception:
                pass

except Exception as e:
    print(f"An error occurred: {e}")

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 写入文件
with open(output_file_path, "w", encoding="utf-8") as f:
    for d in domain_list:
        f.write(d + "\n")

print(f"[{datetime.now()}] Processed {len(domain_list)} China domains → {output_file_path}")
