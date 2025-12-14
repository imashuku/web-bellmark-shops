import json
import html

# ============================================
# 設定（毎月の更新時はここだけ変更）
# ============================================
CURRENT_DATE = "2025年12月現在"
# ============================================

# JSONデータを読み込む
with open('shops_data.json', 'r', encoding='utf-8') as f:
    shops_data = json.load(f)

# 総店舗数を自動計算
total_shops = sum(len(shops) for shops in shops_data.values())

# 高還元ショップTOP10を抽出（%と点を別々に）
all_shops_percent = []
all_shops_points = []
for category, shops in shops_data.items():
    for shop in shops:
        if shop['interest_rate']:
            shop_data = {
                **shop,
                'category': category,
                'rate_float': float(shop['interest_rate'])
            }
            if shop['ir_unit'] == '%':
                all_shops_percent.append(shop_data)
            elif shop['ir_unit'] == '点':
                all_shops_points.append(shop_data)

top_shops_percent = sorted(all_shops_percent, key=lambda x: x['rate_float'], reverse=True)[:10]
top_shops_points = sorted(all_shops_points, key=lambda x: x['rate_float'], reverse=True)[:10]

# HTMLを生成
html_content = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ウェブベルマーク 掲載ショップ一覧</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "BIZ UDPGothic", Meiryo, sans-serif;
            line-height: 1.7;
            color: #1a1a1a;
            background-color: #fff;
        }

        .container {
            max-width: 960px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* ヘッダー */
        header {
            background-color: #1e3a5f;
            color: white;
            padding: 48px 0 40px;
            text-align: center;
        }

        header h1 {
            font-size: 1.5rem;
            margin-bottom: 8px;
            font-weight: 500;
            letter-spacing: 0.08em;
        }

        .hero-subtitle {
            font-size: 0.875rem;
            opacity: 0.8;
            margin-bottom: 24px;
            font-weight: 300;
        }

        .hero-number {
            font-size: 3.5rem;
            font-weight: 600;
            line-height: 1;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
        }

        .hero-number-label {
            font-size: 0.8rem;
            opacity: 0.7;
            letter-spacing: 0.1em;
        }

        .date-note {
            font-size: 0.75rem;
            opacity: 0.5;
            margin-top: 24px;
        }

        /* 検索・フィルター */
        .filter-section {
            padding: 24px 0;
            border-bottom: 1px solid #e5e5e5;
            margin-bottom: 32px;
        }

        #searchBox {
            width: 100%;
            max-width: 400px;
            padding: 12px 16px;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            font-size: 0.9375rem;
            margin-bottom: 12px;
            transition: border-color 0.2s;
        }

        #searchBox:focus {
            outline: none;
            border-color: #1e3a5f;
        }

        .filter-options {
            font-size: 0.875rem;
            color: #555;
        }

        .filter-options label {
            display: inline-flex;
            align-items: center;
            cursor: pointer;
        }

        .filter-options input[type="checkbox"] {
            margin-right: 8px;
            width: 16px;
            height: 16px;
        }

        /* カテゴリ */
        .category-section {
            margin-bottom: 48px;
        }

        .category-header {
            display: flex;
            align-items: baseline;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid #e5e5e5;
        }

        .category-header h2 {
            color: #1a1a1a;
            font-size: 1.125rem;
            font-weight: 600;
        }

        .shop-count {
            color: #888;
            font-size: 0.8125rem;
        }

        /* ショップグリッド */
        .shops-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }

        .shop-card {
            background-color: #fff;
            border: 1px solid #e5e5e5;
            border-radius: 6px;
            padding: 20px;
            transition: border-color 0.2s;
            position: relative;
        }

        .shop-card:hover {
            border-color: #1e3a5f;
        }

        .shop-card.recommended {
            border-color: #1e3a5f;
            background-color: #f8fafc;
        }

        .recommended-badge {
            position: absolute;
            top: 12px;
            right: 12px;
            background-color: #1e3a5f;
            color: white;
            padding: 2px 10px;
            border-radius: 3px;
            font-size: 0.6875rem;
            font-weight: 500;
            letter-spacing: 0.05em;
        }

        .shop-name {
            font-size: 1rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 8px;
            line-height: 1.4;
            padding-right: 60px;
        }

        .shop-card.recommended .shop-name {
            padding-right: 80px;
        }

        .shop-description {
            font-size: 0.8125rem;
            color: #666;
            line-height: 1.6;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .shop-reward {
            padding: 12px 0 0;
            border-top: 1px solid #eee;
        }

        .reward-rate {
            color: #1a1a1a;
            font-size: 0.8125rem;
        }

        .reward-rate .rate-number {
            color: #c41e3a;
            font-weight: 700;
            font-size: 1.5rem;
            letter-spacing: -0.02em;
        }

        .reward-rate .rate-unit {
            color: #c41e3a;
            font-weight: 600;
            font-size: 1rem;
        }

        /* 高還元ショップセクション */
        .top-shops-section {
            margin-bottom: 48px;
            padding-bottom: 48px;
            border-bottom: 1px solid #e5e5e5;
        }

        .top-shops-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 32px;
        }

        .top-shops-column .section-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 4px;
        }

        .top-shops-column .section-desc {
            font-size: 0.75rem;
            color: #888;
            margin-bottom: 16px;
        }

        .top-shops-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .top-shop-card {
            background-color: #fff;
            border: 1px solid #e5e5e5;
            border-radius: 6px;
            padding: 12px 16px;
            transition: border-color 0.2s;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .top-shop-card:hover {
            border-color: #1e3a5f;
        }

        .top-shop-rank {
            font-size: 0.75rem;
            color: #888;
            min-width: 32px;
        }

        .top-shop-info {
            flex: 1;
            min-width: 0;
        }

        .top-shop-name {
            font-size: 0.8125rem;
            font-weight: 600;
            color: #1a1a1a;
            line-height: 1.3;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .top-shop-category {
            font-size: 0.6875rem;
            color: #888;
        }

        .top-shop-rate {
            color: #c41e3a;
            font-weight: 700;
            font-size: 1.125rem;
            white-space: nowrap;
        }

        .top-shop-rate .rate-unit {
            font-size: 0.75rem;
        }

        @media (max-width: 768px) {
            .top-shops-row {
                grid-template-columns: 1fr;
                gap: 32px;
            }
        }

        /* フッター */
        footer {
            background-color: #f5f5f5;
            color: #888;
            text-align: center;
            padding: 24px 0;
            margin-top: 64px;
            font-size: 0.75rem;
        }

        /* アクションボタン */
        .action-buttons {
            position: fixed;
            bottom: 24px;
            right: 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 999;
        }

        .action-btn {
            background-color: #1e3a5f;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8125rem;
            transition: background-color 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .action-btn:hover {
            background-color: #2d4a6f;
        }

        .share-menu {
            position: absolute;
            bottom: 100%;
            right: 0;
            background-color: white;
            border: 1px solid #e5e5e5;
            border-radius: 6px;
            padding: 8px;
            margin-bottom: 8px;
            display: none;
            min-width: 180px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .share-menu.show {
            display: block;
        }

        .share-option {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.15s;
            text-decoration: none;
            color: #333;
            font-size: 0.8125rem;
        }

        .share-option:hover {
            background-color: #f5f5f5;
        }

        /* レスポンシブ */
        @media (max-width: 600px) {
            header {
                padding: 36px 0 32px;
            }

            header h1 {
                font-size: 1.25rem;
            }

            .hero-number {
                font-size: 2.5rem;
            }

            .container {
                padding: 0 16px;
            }

            .shops-grid {
                grid-template-columns: 1fr;
            }

            .action-buttons {
                bottom: 16px;
                right: 16px;
            }
        }

        .hidden {
            display: none;
        }

        /* 印刷用CSS */
        @media print {
            header, .filter-section, .action-buttons, footer, .top-shops-section {
                display: none !important;
            }

            .container {
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            .category-section {
                page-break-inside: avoid;
                margin-bottom: 16px !important;
            }

            .category-header {
                page-break-after: avoid;
            }

            .shops-grid {
                display: block !important;
            }

            .shop-card {
                display: inline-block !important;
                width: 48% !important;
                margin: 0 1% 8px !important;
                page-break-inside: avoid;
                vertical-align: top;
                border: 1px solid #ccc !important;
                padding: 8px !important;
            }

            .shop-name {
                font-size: 0.85rem !important;
            }

            .shop-description {
                font-size: 0.7rem !important;
                -webkit-line-clamp: 2;
            }

            .shop-reward {
                padding: 4px !important;
            }

            body {
                font-size: 9pt !important;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>ウェブベルマーク 掲載ショップ一覧</h1>
            <p class="hero-subtitle">いつものネットショッピングが、学校への支援に</p>
            <div class="hero-number">''' + str(total_shops) + '''</div>
            <div class="hero-number-label">提携ショップ</div>
            <p class="date-note">''' + CURRENT_DATE + '''</p>
        </div>
    </header>

    <main>
        <div class="container">
            <div class="filter-section">
                <input type="text" id="searchBox" placeholder="ショップ名で検索..." onkeyup="filterShops()">
                <div class="filter-options">
                    <label>
                        <input type="checkbox" id="showRecommended" onchange="filterShops()">
                        <span>おすすめショップのみ表示</span>
                    </label>
                </div>
            </div>

            <!-- 高還元ショップTOP10 -->
            <div class="top-shops-section" id="topShopsSection">
                <div class="top-shops-row">
                    <div class="top-shops-column">
                        <h2 class="section-title">還元率 TOP10</h2>
                        <p class="section-desc">購入金額に対する還元率が高いショップ</p>
                        <div class="top-shops-list">
'''

# 還元率TOP10を生成
for i, shop in enumerate(top_shops_percent, 1):
    shop_name_escaped = html.escape(shop['name'])
    category_escaped = html.escape(shop['category'])
    rate = shop['rate_float']
    html_content += f'''
                            <div class="top-shop-card">
                                <div class="top-shop-rank">No.{i}</div>
                                <div class="top-shop-info">
                                    <div class="top-shop-name">{shop_name_escaped}</div>
                                    <div class="top-shop-category">{category_escaped}</div>
                                </div>
                                <div class="top-shop-rate"><span class="rate-number">{rate:.2f}</span><span class="rate-unit">%</span></div>
                            </div>
'''

html_content += '''
                        </div>
                    </div>
                    <div class="top-shops-column">
                        <h2 class="section-title">還元点数 TOP10</h2>
                        <p class="section-desc">利用に対する還元点数が多いショップ</p>
                        <div class="top-shops-list">
'''

# 還元点数TOP10を生成
for i, shop in enumerate(top_shops_points, 1):
    shop_name_escaped = html.escape(shop['name'])
    category_escaped = html.escape(shop['category'])
    rate = int(shop['rate_float'])
    html_content += f'''
                            <div class="top-shop-card">
                                <div class="top-shop-rank">No.{i}</div>
                                <div class="top-shop-info">
                                    <div class="top-shop-name">{shop_name_escaped}</div>
                                    <div class="top-shop-category">{category_escaped}</div>
                                </div>
                                <div class="top-shop-rate"><span class="rate-number">{rate:,}</span><span class="rate-unit">点</span></div>
                            </div>
'''

html_content += '''
                        </div>
                    </div>
                </div>
            </div>

            <div id="shopsContainer">
'''

# 小学生の保護者向けのカテゴリ順序を定義
category_order = [
    "総合通販・百貨店",  # アスクルを含む、日常的に使う総合通販
    "教育用品",  # 学校用品（ウチダス、スマートスクール）
    "教育・学習サービス",  # Z会、進研ゼミなど
    "本・音楽・ゲーム",  # 教育書籍、参考書、児童書
    "キッズ・ベビー・おもちゃ",  # 子供用品
    "ファッション・アパレル",  # 子供服・大人服
    "食品・飲料・グルメ予約",  # 日常の食品購入
    "美容・コスメ・健康",  # 保護者自身のニーズ
    "スポーツ・アウトドア",  # 子供のスポーツ用品
    "インテリア・生活雑貨・ペット用品",  # 生活必需品
    "家電・PC・カメラ",  # 家電製品
    "旅行・宿泊予約",  # 家族旅行
    "フラワー・ギフト",  # 学校行事のお花など
    "レジャー・エンタメ・体験",  # 週末の家族レジャー
    "動画配信サービス",  # 子供向けコンテンツ
    "サービス・その他",  # その他サービス
    "買取・中古品販売",  # 不用品処分
    "その他"  # その他
]

# カテゴリ順序に基づいてショップを表示
for category in category_order:
    if category in shops_data:
        shops = shops_data[category]
        html_content += f'''
                <div class="category-section" data-category="{html.escape(category)}">
                    <div class="category-header">
                        <h2>{html.escape(category)}</h2>
                        <span class="shop-count">{len(shops)}件</span>
                    </div>
                    <div class="shops-grid">
'''

        for shop in shops:
            is_recommended = 'recommended' if shop['is_recommend'] else ''
            recommended_badge = '<span class="recommended-badge">おすすめ</span>' if shop['is_recommend'] else ''

            # 支援金情報のフォーマット（視覚的強調用にHTMLタグを使用）
            if shop['interest_rate'] and shop['ir_unit']:
                rate = float(shop['interest_rate'])
                if shop['ir_unit'] == '%':
                    # パーセントの場合は小数点第2位まで表示
                    reward_info = f'<span class="rate-number">{rate:.2f}</span><span class="rate-unit">%</span>'
                elif shop['ir_unit'] == '点':
                    # 点数の場合は整数表示
                    reward_info = f'<span class="rate-number">{int(rate):,}</span><span class="rate-unit">点</span>'
                else:
                    reward_info = f'<span class="rate-number">{shop["interest_rate"]}</span><span class="rate-unit">{shop["ir_unit"]}</span>'
            else:
                reward_info = ''

            # 支援金の前後の文言を短縮（改行も削除）
            ir_text_front = shop['ir_text_front'].replace('支援金は\n', '').replace('支援金は', '').replace('\\n', '').replace('\n', '').strip()

            # 説明文の改行も削除
            description = shop['explanation'].replace('\\n', ' ').replace('\n', ' ').strip()

            html_content += f'''
                        <div class="shop-card {is_recommended}" data-name="{html.escape(shop['name'].lower())}">
                            {recommended_badge}
                            <h3 class="shop-name">{html.escape(shop['name'])}</h3>
                            <p class="shop-description">{html.escape(description)}</p>
                            <div class="shop-reward">
                                <span class="reward-rate">{html.escape(ir_text_front)} {reward_info}</span>
                            </div>
                        </div>
'''

        html_content += '''
                    </div>
                </div>
'''

# 印刷用の日付も変数から生成
html_content += '''
            </div>
        </div>
    </main>

    <!-- アクションボタン -->
    <div class="action-buttons">
        <div style="position: relative;">
            <button class="action-btn" id="shareBtn" onclick="toggleShareMenu()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/>
                </svg>
                共有
            </button>
            <div class="share-menu" id="shareMenu">
                <a href="#" class="share-option" onclick="shareToLine()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="#00B900">
                        <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.105.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.627-.63.348 0 .631.285.631.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/>
                    </svg>
                    LINEで送る
                </a>
                <a href="#" class="share-option" onclick="shareToTwitter()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="#1DA1F2">
                        <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                    X(Twitter)で共有
                </a>
                <a href="#" class="share-option" onclick="shareToFacebook()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="#1877F2">
                        <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                    </svg>
                    Facebookで共有
                </a>
                <a href="#" class="share-option" onclick="copyToClipboard()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="#666">
                        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                    </svg>
                    URLをコピー
                </a>
            </div>
        </div>
        <button class="action-btn" onclick="printPage()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/>
            </svg>
            印刷・PDF保存
        </button>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 ウェブベルマーク. All rights reserved.</p>
        </div>
    </footer>

    <script>
        // 印刷用の日付（Pythonから埋め込み）
        const PRINT_DATE = "''' + CURRENT_DATE + '''";

        function filterShops() {
            const searchText = document.getElementById('searchBox').value.toLowerCase();
            const showRecommended = document.getElementById('showRecommended').checked;

            const sections = document.querySelectorAll('.category-section');

            sections.forEach(section => {
                const cards = section.querySelectorAll('.shop-card');
                let visibleCount = 0;

                cards.forEach(card => {
                    const name = card.dataset.name;
                    const isRecommended = card.classList.contains('recommended');

                    const matchesSearch = !searchText || name.includes(searchText);
                    const matchesRecommended = !showRecommended || isRecommended;

                    if (matchesSearch && matchesRecommended) {
                        card.classList.remove('hidden');
                        visibleCount++;
                    } else {
                        card.classList.add('hidden');
                    }
                });

                // カテゴリ全体を表示/非表示
                if (visibleCount === 0) {
                    section.classList.add('hidden');
                } else {
                    section.classList.remove('hidden');
                }
            });
        }

        // 共有メニューの表示/非表示
        function toggleShareMenu() {
            const menu = document.getElementById('shareMenu');
            menu.classList.toggle('show');
            event.stopPropagation();
        }

        // クリック外でメニューを閉じる
        document.addEventListener('click', function(event) {
            const menu = document.getElementById('shareMenu');
            const shareBtn = document.getElementById('shareBtn');
            if (!shareBtn.contains(event.target)) {
                menu.classList.remove('show');
            }
        });

        // LINEで共有
        function shareToLine() {
            const url = encodeURIComponent(window.location.href);
            const text = encodeURIComponent('ウェブベルマーク掲載ショップ一覧 - お買い物で学校を応援！');
            window.open(`https://line.me/R/msg/text/?${text}%0D%0A${url}`, '_blank');
            return false;
        }

        // Twitterで共有
        function shareToTwitter() {
            const url = encodeURIComponent(window.location.href);
            const text = encodeURIComponent('ウェブベルマーク掲載ショップ一覧 - お買い物で学校を応援できます！ #ウェブベルマーク');
            window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank');
            return false;
        }

        // Facebookで共有
        function shareToFacebook() {
            const url = encodeURIComponent(window.location.href);
            window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
            return false;
        }

        // URLをコピー
        function copyToClipboard() {
            const url = window.location.href;
            navigator.clipboard.writeText(url).then(function() {
                alert('URLをコピーしました！');
            }, function(err) {
                // フォールバック
                const textArea = document.createElement('textarea');
                textArea.value = url;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('URLをコピーしました！');
            });
            return false;
        }

        // 印刷機能
        function printPage() {
            // 印刷前に全カテゴリを表示
            const hiddenSections = document.querySelectorAll('.category-section.hidden');
            hiddenSections.forEach(section => {
                section.classList.remove('hidden');
            });

            // タイトルを追加
            const printTitle = document.createElement('div');
            printTitle.innerHTML = '<h1 style="text-align: center; margin-bottom: 5px;">ウェブベルマーク 掲載ショップ一覧</h1><p style="text-align: center; margin-bottom: 20px; font-size: 0.9rem; color: #666;">' + PRINT_DATE + '</p>';
            printTitle.style.display = 'none';
            printTitle.classList.add('print-title');
            document.body.insertBefore(printTitle, document.body.firstChild);

            // 印刷用スタイルを適用
            window.print();

            // 印刷後に元に戻す
            setTimeout(() => {
                filterShops();
                document.querySelector('.print-title').remove();
            }, 100);
        }

        // Web Share API対応（モバイル）
        if (navigator.share) {
            // モバイルの場合はネイティブ共有も使える
            const shareBtn = document.getElementById('shareBtn');
            shareBtn.addEventListener('click', async (e) => {
                if (e.shiftKey) { // Shiftキーを押しながらクリックした場合はメニューを表示
                    return;
                }
                try {
                    await navigator.share({
                        title: 'ウェブベルマーク掲載ショップ一覧',
                        text: 'お買い物で学校を応援できます！',
                        url: window.location.href
                    });
                    e.preventDefault();
                    e.stopPropagation();
                } catch(err) {
                    // Web Share APIが使えない場合はメニューを表示
                    console.log('Web Share API not supported');
                }
            });
        }

        // 印刷用スタイルを追加
        const printStyle = document.createElement('style');
        printStyle.innerHTML = `
            @media print {
                .print-title {
                    display: block !important;
                    page-break-after: avoid;
                }
            }
        `;
        document.head.appendChild(printStyle);
    </script>
</body>
</html>
'''

# HTMLファイルを保存
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"index.htmlを生成しました（{total_shops}店舗、{CURRENT_DATE}）")
