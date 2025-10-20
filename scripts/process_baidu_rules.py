import requests
import yaml
import os

# 定义输出文件夹和文件名
output_dir = "ios_rules"
output_file_name = "baidu.conf" # <--- 输出文件为 baidu.conf
output_file_path = os.path.join(output_dir, output_file_name)

# 源文件 URL (已更新为 Baidu 规则)
url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Baidu/Baidu.yaml"

# 定义需要提取的规则类型
# 注意：Baidu.yaml 文件中只有 DOMAIN-SUFFIX
valid_types = ["DOMAIN-SUFFIX"]

print(f"Fetching Baidu rules from {url}...")
domain_list = []

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
    print(f"An error occurred during processing: {e}")

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 无论是否成功获取域名，都创建或覆盖文件
with open(output_file_path, 'w', encoding='utf-8') as f:
    if domain_list:
        for domain in domain_list:
            f.write(domain + '\n')
        print(f"Successfully processed {len(domain_list)} Baidu domains.")
    else:
        print("Warning: No Baidu domains were extracted. An empty conf file will be created.")
        
print(f"Result saved to {output_file_path}")
