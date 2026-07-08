import csv
import os

def generate_md():
    categories = {
        1: "インテリア・生活雑貨・ペット用品",
        2: "買取・中古品販売",
        3: "キッズ・ベビー・おもちゃ",
        4: "レジャー・エンタメ・体験",
        5: "食品・飲料・グルメ予約",
        6: "ファッション・アパレル",
        7: "フラワー・ギフト",
        8: "サービス・その他",
        9: "家電・PC・カメラ",
        10: "スポーツ・アウトドア",
        11: "総合通販・百貨店",
        12: "美容・コスメ・健康",
        13: "本・音楽・ゲーム",
        14: "旅行・宿泊予約",
        16: "教育用品",
        17: "動画配信サービス",
        18: "教育・学習サービス",
        21: "その他"
    }

    # Ensure we use the correct file
    filename = '20251210_companies_fixed.csv'
    if not os.path.exists(filename):
        filename = '20251210_companies.csv'
        print(f"Fixed file not found, using {filename}")

    shops_by_category = {k: [] for k in categories.keys()}
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check validity
            if row.get('is_valid') == '1' and row.get('delete_flag') == '0':
                try:
                    cat_id = int(row['category_id']) if row.get('category_id') and row['category_id'] != 'NULL' else 21
                except:
                    cat_id = 21 # Default to Others
                
                if cat_id not in categories:
                    cat_id = 21

                # Format interest rate string: Front + Rate + Unit + After
                # careful with None/NULL
                def safe_str(s):
                    return s if s and s != 'NULL' else ''
                
                rate_str = f"{safe_str(row.get('ir_text_front', ''))} {safe_str(row.get('interest_rate', ''))}{safe_str(row.get('ir_unit', ''))} {safe_str(row.get('ir_text_after', ''))}"
                rate_str = rate_str.strip().replace('\n', ' ')

                shop = {
                    'name': row['name'],
                    'explanation': safe_str(row['explanation']).replace('\n', '<br>'),
                    'rate': rate_str,
                    'order': int(row['order']) if row.get('order') and row['order'] != 'NULL' else 9999
                }
                shops_by_category[cat_id].append(shop)

    # Sort shops in each category
    for cat_id in shops_by_category:
        shops_by_category[cat_id].sort(key=lambda x: (x['order'], x['name']))

    # Generate Markdown
    md_content = "# 2025年12月時点 掲載ショップ一覧\n\n"
    
    total_shops = 0

    for cat_id, cat_name in categories.items():
        shops = shops_by_category.get(cat_id, [])
        if not shops:
            continue
            
        md_content += f"## {cat_name} ({len(shops)}店舗)\n\n"
        md_content += "| ショップ名 | 支援金設定 | 説明 |\n"
        md_content += "| --- | --- | --- |\n"
        
        for shop in shops:
            # Escape pipes in content
            name = shop['name'].replace('|', '\|')
            rate = shop['rate'].replace('|', '\|')
            expl = shop['explanation'].replace('|', '\|')
            
            md_content += f"| {name} | {rate} | {expl} |\n"
        
        md_content += "\n"
        total_shops += len(shops)

    md_content += f"\n**合計店舗数: {total_shops}**\n"

    output_file = '2025年12月時点_掲載ショップ一覧.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Generated {output_file} with {total_shops} shops.")

if __name__ == "__main__":
    generate_md()
