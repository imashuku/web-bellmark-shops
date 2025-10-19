import json
import html

# JSONデータを読み込む
with open('shops_data.json', 'r', encoding='utf-8') as f:
    shops_data = json.load(f)

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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 15px;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            text-align: center;
        }

        header h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .lead {
            font-size: 1.1rem;
            opacity: 0.95;
        }

        .filter-section {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 2rem 0;
        }

        #searchBox {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
            margin-bottom: 1rem;
        }

        .filter-options label {
            display: flex;
            align-items: center;
            cursor: pointer;
        }

        .filter-options input[type="checkbox"] {
            margin-right: 0.5rem;
        }

        .category-section {
            margin-bottom: 3rem;
        }

        .category-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }

        .category-header h2 {
            color: #667eea;
            font-size: 1.5rem;
        }

        .shop-count {
            margin-left: auto;
            color: #666;
            font-size: 0.9rem;
        }

        .shops-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .shop-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .shop-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }

        .shop-card.recommended {
            border: 2px solid #ffd700;
        }

        .recommended-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: #ffd700;
            color: #333;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .shop-name {
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 0.5rem;
        }

        .shop-description {
            font-size: 0.9rem;
            color: #666;
            line-height: 1.5;
            margin-bottom: 1rem;
        }

        .shop-reward {
            background-color: #fff3cd;
            padding: 0.75rem;
            border-radius: 5px;
            margin-bottom: 0.5rem;
            text-align: center;
        }

        .reward-rate {
            color: #e74c3c;
            font-weight: bold;
            font-size: 1.2rem;
        }


        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 1.5rem 0;
            margin-top: 4rem;
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 1.5rem;
            }
            
            .shops-grid {
                grid-template-columns: 1fr;
            }
        }

        .hidden {
            display: none;
        }
        
        /* 共有・印刷ボタン */
        .action-buttons {
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 999;
        }
        
        .action-btn {
            background-color: #667eea;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 0.9rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        
        .share-menu {
            position: absolute;
            bottom: 100%;
            right: 0;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            padding: 0.5rem;
            margin-bottom: 10px;
            display: none;
            min-width: 200px;
        }
        
        .share-menu.show {
            display: block;
        }
        
        .share-option {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0.75rem;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
            text-decoration: none;
            color: #333;
        }
        
        .share-option:hover {
            background-color: #f0f0f0;
        }
        
        /* 印刷用CSS */
        @media print {
            header, .filter-section, .action-buttons, footer {
                display: none !important;
            }
            
            .category-nav {
                position: static !important;
                display: none !important;
            }
            
            .container {
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            .category-section {
                page-break-inside: avoid;
                margin-bottom: 20px !important;
            }
            
            .category-header {
                page-break-after: avoid;
                font-size: 1.2rem !important;
                margin-bottom: 10px !important;
            }
            
            .shops-grid {
                display: block !important;
            }
            
            .shop-card {
                display: inline-block !important;
                width: 48% !important;
                margin: 0 1% 10px !important;
                page-break-inside: avoid;
                vertical-align: top;
                box-shadow: none !important;
                border: 1px solid #ddd !important;
                padding: 10px !important;
            }
            
            .shop-name {
                font-size: 0.9rem !important;
            }
            
            .shop-description {
                font-size: 0.7rem !important;
                line-height: 1.3 !important;
            }
            
            .shop-reward {
                font-size: 0.8rem !important;
                padding: 5px !important;
            }
            
            body {
                font-size: 10pt !important;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>ウェブベルマーク 掲載ショップ一覧</h1>
            <p class="lead">お買い物をしながら、学校を応援できます</p>
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
            
            # 支援金情報のフォーマット
            if shop['interest_rate'] and shop['ir_unit']:
                rate = float(shop['interest_rate'])
                if shop['ir_unit'] == '%':
                    # パーセントの場合は小数点第2位まで表示
                    reward_info = f"{rate:.2f}%"
                elif shop['ir_unit'] == '点':
                    # 点数の場合は整数表示
                    reward_info = f"{int(rate)}点"
                else:
                    reward_info = f"{shop['interest_rate']}{shop['ir_unit']}"
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
                                <span class="reward-rate">{html.escape(ir_text_front)} {html.escape(reward_info)}</span>
                            </div>
                        </div>
'''
        
        html_content += '''
                    </div>
                </div>
'''

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
            printTitle.innerHTML = '<h1 style="text-align: center; margin-bottom: 20px;">ウェブベルマーク 掲載ショップ一覧</h1>';
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
with open('shops_list.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("shops_list.htmlを生成しました")