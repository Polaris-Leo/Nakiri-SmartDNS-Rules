import requests
import yaml
import os
from datetime import datetime

CONFIG_PATH = os.path.join("scripts", "ios_rules_config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def fetch_payload(url):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = yaml.safe_load(resp.text)
    return data.get("payload", [])

def extract_domains(payload, valid_types):
    domains = set()

    for item in payload:
        parts = item.split(",", 1)
        if len(parts) != 2:
            continue

        rule_type, value = parts
        rule_type = rule_type.strip()
        value = value.strip()

        if rule_type in valid_types and value:
            domains.add(value)

    return sorted(domains)

def write_output(domains, output_conf):
    output_file = output_conf["file"]
    fmt = output_conf.get("format", "domain")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for d in domains:
            if fmt == "domain":
                f.write(d + "\n")
            elif fmt == "smartdns":
                # 预留：server=/example.com/1.1.1.1
                f.write(f"server=/{d}/\n")
            else:
                raise ValueError(f"Unknown output format: {fmt}")

def process_rule(rule, valid_types):
    name = rule["name"]

    if not rule.get("enabled", True):
        print(f"[SKIP] {name} is disabled")
        return

    url = rule["source"]["url"]
    output = rule["output"]

    print(f"\n[{datetime.now()}] ▶ Processing {name}")
    print(f"Source: {url}")

    try:
        payload = fetch_payload(url)
        domains = extract_domains(payload, valid_types)
        write_output(domains, output)
        print(f"[OK] {name}: {len(domains)} domains")

    except Exception as e:
        print(f"[ERROR] {name}: {e}")

def main():
    print(f"[{datetime.now()}] iOS rules update started")

    config = load_config()
    valid_types = set(config["global"]["valid_types"])

    for rule in config.get("rules", []):
        process_rule(rule, valid_types)

    print(f"\n[{datetime.now()}] All rules processed")

if __name__ == "__main__":
    main()
