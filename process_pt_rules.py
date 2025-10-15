import requests
import yaml
import os # 导入 os 模块

# 定义输出文件夹和文件名
output_dir = "ios_rules"
output_file_name = "pt_domains.conf"
output_file_path = os.path.join(output_dir, output_file_name)

# 源文件 URL
url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/PrivateTracker/PrivateTracker.yaml"

# 定义需要提取的规则类型
valid_types = ["DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"]

print(f"Fetching rules from {url}...")

try:
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 发送请求获取文件内容
    response = requests.get(url)
    response.raise_for_status()

    # 使用 PyYAML 解析 YAML 内容
    data = yaml.safe_load(response.text)

    # 提取 payload 列表
    payload = data.get('payload', [])
    
    domain_list = []
    if payload:
        for item in payload:
            parts = item.split(',')
            if len(parts) == 2 and parts[0] in valid_types:
                domain_list.append(parts[1].strip())

    if not domain_list:
        print("Warning: No domains were extracted. The source format might have changed.")
    
    # 将提取的域名写入文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for domain in domain_list:
            f.write(domain + '\n')
            
    print(f"Successfully processed {len(domain_list)} domains.")
    print(f"Result saved to {output_file_path}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error parsing YAML file: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)
