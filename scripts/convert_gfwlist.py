# convert_gfwlist_final.py

import re
import os

def sanitize_filename(name):
    """
    清理字符串，使其可以安全地用作文件名。
    """
    name = re.sub(r'[\\/*?:"<>|()]', "", name)
    name = name.replace(' ', '_').replace('&', 'and')
    return name[:100].strip('_.-')

def extract_domain(rule):
    """
    从 GFWList 规则中提取干净的域名。
    """
    if rule.startswith('!') or rule.startswith('[') or rule.startswith('@@') or re.match(r'^\d{1,3}(\.\d{1,3}){3}', rule):
        return None

    if rule.startswith('/'): # Regex rules
        return None

    if rule.startswith('||'):
        domain = rule[2:]
    elif rule.startswith('|http://') or rule.startswith('|https://'):
        domain = rule.split('/')[2]
    elif rule.startswith('.'):
        domain = rule[1:]
    else:
        domain = rule

    domain = domain.split('/')[0].split(':')[0].replace('*', '')
    
    if '.' not in domain or len(domain.split('.')[-1]) < 2:
        return None
        
    if domain.startswith('.'):
        domain = domain[1:]
        
    return domain.strip() if domain else None


def process_gfwlist_final(input_file, output_dir):
    """
    处理 GFWList 文件，生成符合 SmartDNS -file 选项的纯域名列表文件。
    """
    SPECIFIC_GROUPS = {
        'Akamai', 'Amazon', 'AOL', 'BBC', 'Bloomberg', 'Cloudflare',
        'Facebook', 'GitHub', 'Google', 'Microsoft', 'NYTimes', 
        'Steam', 'Telegram', 'Tiktok', 'Twitch', 'TwitterX', 
        'VOA', 'Yahoo', 'Wikipedia_Related',
        'Digital_Currency_Exchange_CRYPTO',
    }

    if not os.path.exists(output_dir):
        print(f"创建输出目录: {output_dir}")
        os.makedirs(output_dir)

    specific_groups_data = {group: set() for group in SPECIFIC_GROUPS}
    general_domains = set()
    
    current_group = 'Uncategorized'
    is_in_wiki_section = False

    print(f"开始读取和解析文件: {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue

                is_group_header = False
                group_match = re.search(r'^![-#]+\s*(.+?)\s*[-#]+$', line)
                if group_match:
                    sanitized_group = sanitize_filename(group_match.group(1).strip())
                    is_group_header = True
                    if 'Wikipedia_Related' in sanitized_group:
                        current_group = 'Wikipedia_Related'
                        is_in_wiki_section = True
                    else:
                        current_group = sanitized_group
                        is_in_wiki_section = False

                subgroup_match = re.search(r'^!!-{3,}\s*(.+?)\s*-{3,}$', line)
                if subgroup_match:
                    current_group = sanitize_filename(subgroup_match.group(1).strip())
                    is_in_wiki_section = False
                    is_group_header = True

                if is_group_header: continue

                domain = extract_domain(line)
                if domain:
                    effective_group = 'Wikipedia_Related' if is_in_wiki_section else current_group
                    
                    if effective_group in SPECIFIC_GROUPS:
                        specific_groups_data[effective_group].add(domain)
                    else:
                        general_domains.add(domain)

    except FileNotFoundError:
        print(f"\n错误: 输入文件 '{input_file}' 不存在。")
        return
    except Exception as e:
        print(f"\n处理文件时发生错误: {e}")
        return

    print("\n开始生成纯域名列表文件...")
    
    # 1. 准备并写入主合并文件
    all_domains = set(general_domains)
    for group_domains in specific_groups_data.values():
        all_domains.update(group_domains)
    
    master_filename = os.path.join(output_dir, "gfwlist-merged.conf")
    sorted_all_domains = sorted(list(all_domains))
    
    with open(master_filename, 'w', encoding='utf-8') as f:
        f.write("# GFWList Merged - Plain domain list for SmartDNS\n")
        f.write(f"# Total domains: {len(sorted_all_domains)}\n\n")
        for domain in sorted_all_domains:
            f.write(f"{domain}\n") # <--- 核心改动在这里
    print(f"✅ 已生成主合并列表: {master_filename} (包含 {len(sorted_all_domains)} 个域名)")

    # 2. 写入特定的分组文件
    for group_name, domains in specific_groups_data.items():
        if not domains: continue
            
        output_filename = os.path.join(output_dir, f"{group_name}.conf")
        sorted_domains = sorted(list(domains))
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"# {group_name} - Plain domain list for SmartDNS\n")
            f.write(f"# Total domains: {len(sorted_domains)}\n\n")
            for domain in sorted_domains:
                f.write(f"{domain}\n") # <--- 核心改动在这里
        print(f"✅ 已生成特定列表: {output_filename} (包含 {len(sorted_domains)} 个域名)")
        
    print("\n处理完成！所有纯域名列表文件已生成。")

if __name__ == '__main__':
    INPUT_FILENAME = 'list.txt'
    OUTPUT_DIRECTORY = 'smartdns_domain_lists'
    process_gfwlist_final(INPUT_FILENAME, OUTPUT_DIRECTORY)
