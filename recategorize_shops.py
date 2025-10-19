import csv
import json
from collections import defaultdict

# 正しいカテゴリマッピング（一般的なショップ分類から推測）
def get_correct_category(shop_name, shop_explanation):
    name_lower = shop_name.lower()
    desc_lower = shop_explanation.lower()
    
    # 明確なカテゴリ判定
    if any(word in name_lower or word in desc_lower for word in ['u-next', '動画配信', 'hulu', 'netflix', 'dtv', 'dazn', 'wowow']):
        return 'エンタメ・動画配信'
    elif any(word in name_lower or word in desc_lower for word in ['じゃらん', 'エクスペディア', 'jtb', '旅行', 'ホテル', '宿泊', 'トラベル', 'ツアー', '航空券']):
        return '旅行'
    elif any(word in name_lower or word in desc_lower for word in ['dhc', 'ホットペッパービューティ', '美容', 'コスメ', '化粧品', 'ヘアサロン']):
        return '美容・健康'
    elif any(word in name_lower or word in desc_lower for word in ['リクナビ', '転職', '求人', '派遣', 'キャリア']):
        return '転職・求人'
    elif any(word in name_lower or word in desc_lower for word in ['z会', '進研ゼミ', '学習', '教育', '資格', 'スタディ', '通信教育']):
        return '教育・資格・学習'
    elif any(word in name_lower or word in desc_lower for word in ['ウチダス', 'スマートスクール', '学校用品', '教育用品']):
        return '学校・教育用品'
    elif any(word in name_lower or word in desc_lower for word in ['ニッセン', 'ベルメゾン', 'セシール', 'ファッション']):
        return 'ファッション・通販'
    elif any(word in name_lower or word in desc_lower for word in ['yahoo', 'ショッピング', 'アスクル', '楽天', 'amazon', 'ロフト']):
        return 'ショッピングモール・総合通販'
    elif any(word in name_lower or word in desc_lower for word in ['セブンネット', 'タワーレコード', 'tsutaya', '書籍', '本', ' cd', ' dvd', 'ブック']):
        return '書籍・CD・DVD'
    elif any(word in name_lower or word in desc_lower for word in ['アカチャンホンポ', 'トイザらス', 'ベビー', 'キッズ', '子供', '赤ちゃん']):
        return 'ベビー・キッズ'
    elif any(word in name_lower or word in desc_lower for word in ['ノジマ', 'レノボ', 'パソコン', '家電', ' pc', 'デジタル', 'カメラ', 'dell']):
        return 'PC・家電'
    elif any(word in name_lower or word in desc_lower for word in ['車', 'バイク', 'カー', '買取', '中古車', '自動車']):
        return 'クルマ・バイク・買取'
    elif any(word in name_lower or word in desc_lower for word in ['ペット', '花', 'フラワー', 'イイハナ']):
        return 'ペット・花'
    elif any(word in name_lower or word in desc_lower for word in ['食品', '酒', 'グルメ', 'お取り寄せ', 'デリバリー', 'ピザ', '弁当']):
        return '食品・お取り寄せ'
    elif any(word in name_lower or word in desc_lower for word in ['住宅', 'リフォーム', 'インテリア', '家具', '引越']):
        return '住宅・インテリア'
    elif any(word in name_lower or word in desc_lower for word in ['インターネット', 'wifi', 'スマホ', ' sim', 'プロバイダ', 'モバイル']):
        return 'インターネット・通信'
    elif any(word in name_lower or word in desc_lower for word in ['文具', '雑貨', 'ステーショナリー']):
        return 'ステーショナリー・雑貨'
    else:
        return 'その他'

# CSVファイルを読み込む
shops_by_category = defaultdict(list)

with open('Companies Oct 9 2025.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['is_valid'] == '1' and row['delete_flag'] == '0':
            shop_name = row['name']
            shop_explanation = row['explanation']
            
            # 正しいカテゴリを判定
            category_name = get_correct_category(shop_name, shop_explanation)
            
            shop = {
                'id': row['company_id'],
                'name': shop_name,
                'identifier': row['identifier'],
                'category_name': category_name,
                'logo_img_pc': row['logo_img_pc'],
                'logo_img_mb': row['logo_img_mb'],
                'explanation': shop_explanation,
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
            shops_by_category[category_name].append(shop)

# Sort shops within each category
for category in shops_by_category:
    shops_by_category[category].sort(key=lambda x: (x['order'], x['name']))

# Save to JSON
with open('shops_data_corrected.json', 'w', encoding='utf-8') as f:
    json.dump(dict(shops_by_category), f, ensure_ascii=False, indent=2)

print('データを再分類しました:')
for category, shop_list in sorted(shops_by_category.items()):
    print(f'{category}: {len(shop_list)}件')
    
# デバッグ: U-NEXTがどのカテゴリに分類されたか確認
for category, shops in shops_by_category.items():
    for shop in shops:
        if 'U-NEXT' in shop['name']:
            print(f"\nU-NEXTは'{category}'に分類されました")