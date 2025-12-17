import os
import requests
from datetime import datetime

# === 文件与路径配置 ===
output_dir = "smartdns_domain_lists"
output_file = "china-merged.conf"
output_path = os.path.join(output_dir, output_file)

# === 数据源 ===
china_url = "https://raw.githubusercontent.com/Polaris-Leo/Nakiri-SmartDNS-Rules/main/smartdns_domain_lists/china.conf"
other_urls = [
    "https://raw.githubusercontent.com/Polaris-Leo/Nakiri-SmartDNS-Rules/main/ios_rules/baidu.conf",
    "https://raw.githubusercontent.com/Polaris-Leo/Nakiri-SmartDNS-Rules/main/ios_rules/bilibili.conf",
    "https://raw.githubusercontent.com/Polaris-Leo/Nakiri-SmartDNS-Rules/main/ios_rules/pt_domains.conf",
    "https://raw.githubusercontent.com/Polaris-Leo/Nakiri-SmartDNS-Rules/refs/heads/main/ios_rules/hoyoverse.conf"
]

print(f"[{datetime.now()}] Starting merge process...")

def fetch_domains(url):
    """读取远程文件并返回域名集合"""
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        lines = [line.strip() for line in r.text.splitlines() if line.strip() and not line.startswith("#")]
        return set(lines)
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return set()

# === 读取 china.conf ===
china_domains = fetch_domains(china_url)
print(f"✅ Loaded {len(china_domains)} China domains.")

# === 读取需要排除的域名文件 ===
exclude_domains = set()
for url in other_urls:
    d = fetch_domains(url)
    exclude_domains |= d
    print(f"✅ Excluded {len(d)} domains from {url}")

# === 去重合并 ===
merged_domains = sorted(china_domains - exclude_domains)
print(f"✅ Final domain count: {len(merged_domains)}")

# === 输出文件 ===
os.makedirs(output_dir, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    for d in merged_domains:
        f.write(d + "\n")

print(f"[{datetime.now()}] Finished: {output_path}")
