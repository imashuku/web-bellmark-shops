import csv
import json
from collections import defaultdict

def parse_shops():
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
    
    shops_by_category = defaultdict(list)
    
    with open('Companies Oct 9 2025.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['is_valid'] == '1' and row['delete_flag'] == '0':
                try:
                    category_id = int(row['category_id']) if row['category_id'] and row['category_id'] != 'NULL' else None
                except:
                    category_id = None
                
                shop = {
                    'id': row['company_id'],
                    'name': row['name'],
                    'identifier': row['identifier'],
                    'category_id': category_id,
                    'category_name': categories.get(category_id, 'その他'),
                    'logo_img_pc': row['logo_img_pc'],
                    'logo_img_mb': row['logo_img_mb'],
                    'explanation': row['explanation'],
                    'is_recommend': row['is_recommend'] == '1',
                    'ir_text_front': row['ir_text_front'],
                    'interest_rate': row['interest_rate'],
                    'ir_unit': row['ir_unit'],
                    'ir_text_after': row['ir_text_after'],
                    'annotation': row['annotation'],
                    'annotation_modal': row['annotation_modal'],
                    'order': int(row['order']) if row['order'] else 9999,
                    'promo_url_pc': row['promo_url_pc'],
                    'promo_url_mb': row['promo_url_mb']
                }
                shops_by_category[shop['category_name']].append(shop)
    
    # Sort shops within each category by order
    for category in shops_by_category:
        shops_by_category[category].sort(key=lambda x: (x['order'], x['name']))
    
    return dict(shops_by_category)

if __name__ == "__main__":
    shops = parse_shops()
    with open('shops_data.json', 'w', encoding='utf-8') as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)
    
    print("データを抽出しました:")
    for category, shop_list in shops.items():
        print(f"{category}: {len(shop_list)}件")