#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict

# CSVファイルを読み込む
csv_file = "Companies Oct 9 2025.csv"
category_shops = defaultdict(list)

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # is_valid=1 かつ delete_flag=0 の有効なショップのみを抽出
        if row['is_valid'] == '1' and row['delete_flag'] == '0':
            # category_idがNULLまたは空の場合はスキップ
            if row['category_id'] and row['category_id'] != 'NULL':
                try:
                    category_id = int(row['category_id'])
                    shop_name = row['name']
                    category_shops[category_id].append(shop_name)
                except ValueError:
                    print(f"警告: 無効なcategory_id '{row['category_id']}' for shop '{row['name']}'")

# カテゴリIDごとに所属ショップを表示
print("カテゴリ別ショップ一覧（有効なショップのみ）\n")
print("=" * 80)

for category_id in sorted(category_shops.keys()):
    shops = category_shops[category_id]
    print(f"\nカテゴリID: {category_id} （{len(shops)}件）")
    print("-" * 40)
    
    # ショップを5つずつ表示して分析しやすくする
    for i, shop in enumerate(shops, 1):
        print(f"  {i:2d}. {shop}")
    
    # カテゴリの推測
    print(f"\n  → カテゴリ推測: ", end="")
    
    # ショップ名から共通のテーマを見つける
    if category_id == 1:
        print("インテリア・生活雑貨・ペット用品")
    elif category_id == 2:
        print("買取・中古品販売")
    elif category_id == 3:
        print("キッズ・ベビー・おもちゃ")
    elif category_id == 4:
        print("レジャー・エンタメ・体験")
    elif category_id == 5:
        print("食品・飲料・グルメ予約")
    elif category_id == 6:
        print("ファッション・アパレル")
    elif category_id == 7:
        print("フラワー・ギフト")
    elif category_id == 8:
        print("サービス・人材・その他")
    elif category_id == 9:
        print("家電・PC・カメラ・デジタル機器")
    elif category_id == 10:
        print("スポーツ・アウトドア・ゴルフ")
    elif category_id == 11:
        print("総合通販・モール・百貨店")
    elif category_id == 12:
        print("美容・コスメ・健康")
    elif category_id == 13:
        print("本・音楽・ゲーム・エンタメ")
    elif category_id == 14:
        print("旅行・宿泊・航空券")
    elif category_id == 16:
        print("教育用品・学校用品")
    elif category_id == 17:
        print("動画配信・エンタメサービス")
    elif category_id == 18:
        print("教育・学習・受験")
    elif category_id == 21:
        print("その他サービス")
    
print("\n" + "=" * 80)