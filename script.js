// グローバル変数
let allShopsData = {};
let currentCategory = 'all';
let showRecommended = false;

// ページ読み込み時の処理
document.addEventListener('DOMContentLoaded', function() {
    // ローカルファイルの場合、JSONを直接埋め込む必要があるため
    // 一旦ダミーデータで初期化して、shops_data.jsファイルを作成する
    console.log('ページ読み込み開始');
    
    // shops_data.jsファイルを動的に読み込む
    const script = document.createElement('script');
    script.src = 'shops_data.js';
    script.onload = function() {
        console.log('データ読み込み完了');
        // カテゴリボタンを作成
        createCategoryButtons();
        
        // 初期表示
        displayShops();
        
        // イベントリスナー設定
        setupEventListeners();
    };
    script.onerror = function() {
        console.error('データの読み込みに失敗しました');
        document.getElementById('shopsContainer').innerHTML = 
            '<p style="text-align: center; padding: 2rem; color: red;">データの読み込みに失敗しました。</p>';
    };
    document.head.appendChild(script);
});

// カテゴリボタンを作成
function createCategoryButtons() {
    const container = document.getElementById('categoryButtons');
    
    // 「すべて」ボタンを追加
    const allBtn = createButton('すべて', 'all', true);
    container.appendChild(allBtn);
    
    // カテゴリごとのボタンを追加
    Object.keys(allShopsData).sort().forEach(category => {
        const btn = createButton(category, category, false);
        container.appendChild(btn);
    });
}

// ボタン要素を作成
function createButton(text, value, isActive) {
    const btn = document.createElement('button');
    btn.className = 'category-btn' + (isActive ? ' active' : '');
    btn.textContent = text;
    btn.dataset.category = value;
    btn.addEventListener('click', handleCategoryClick);
    return btn;
}

// カテゴリボタンクリック処理
function handleCategoryClick(e) {
    // アクティブクラスを切り替え
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');
    
    // 現在のカテゴリを更新
    currentCategory = e.target.dataset.category;
    
    // ショップを再表示
    displayShops();
}

// ショップを表示
function displayShops() {
    const container = document.getElementById('shopsContainer');
    container.innerHTML = '';
    
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    
    if (currentCategory === 'all') {
        // すべてのカテゴリを表示
        Object.entries(allShopsData).forEach(([category, shops]) => {
            const filteredShops = filterShops(shops, searchTerm);
            if (filteredShops.length > 0) {
                const section = createCategorySection(category, filteredShops);
                container.appendChild(section);
            }
        });
    } else {
        // 特定のカテゴリのみ表示
        const shops = allShopsData[currentCategory] || [];
        const filteredShops = filterShops(shops, searchTerm);
        if (filteredShops.length > 0) {
            const section = createCategorySection(currentCategory, filteredShops);
            container.appendChild(section);
        }
    }
    
    // 検索結果が0件の場合
    if (container.children.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 2rem;">該当するショップが見つかりませんでした。</p>';
    }
}

// ショップをフィルタリング
function filterShops(shops, searchTerm) {
    return shops.filter(shop => {
        // おすすめフィルター
        if (showRecommended && !shop.is_recommend) {
            return false;
        }
        
        // 検索フィルター
        if (searchTerm && !shop.name.toLowerCase().includes(searchTerm)) {
            return false;
        }
        
        return true;
    });
}

// カテゴリセクションを作成
function createCategorySection(categoryName, shops) {
    const section = document.createElement('div');
    section.className = 'category-section';
    
    // カテゴリヘッダー
    const header = document.createElement('div');
    header.className = 'category-header';
    header.innerHTML = `
        <h3>${categoryName}</h3>
        <span class="shop-count">${shops.length}件</span>
    `;
    section.appendChild(header);
    
    // ショップグリッド
    const grid = document.createElement('div');
    grid.className = 'shops-grid';
    
    shops.forEach(shop => {
        const card = createShopCard(shop);
        grid.appendChild(card);
    });
    
    section.appendChild(grid);
    return section;
}

// ショップカードを作成
function createShopCard(shop) {
    const card = document.createElement('div');
    card.className = 'shop-card' + (shop.is_recommend ? ' recommended' : '');
    
    // おすすめバッジ
    const badge = shop.is_recommend ? '<span class="recommended-badge">おすすめ</span>' : '';
    
    // ロゴ画像のパス処理
    const logoPath = shop.logo_img_pc ? shop.logo_img_pc.replace('public/', '') : '';
    
    // 支援金情報
    const rewardInfo = formatRewardInfo(shop);
    
    card.innerHTML = `
        ${badge}
        ${logoPath ? `<img src="${logoPath}" alt="${shop.name}" class="shop-logo" onerror="this.style.display='none'">` : ''}
        <h4 class="shop-name">${shop.name}</h4>
        <p class="shop-description">${shop.explanation}</p>
        <div class="shop-reward">
            <div>${shop.ir_text_front}</div>
            <span class="reward-rate">${rewardInfo}</span>
            <div>${shop.ir_text_after}</div>
        </div>
        <a href="#" class="shop-link" data-shop-id="${shop.id}" onclick="showShopDetail(event, ${shop.id})">詳細を見る</a>
    `;
    
    return card;
}

// 支援金情報をフォーマット
function formatRewardInfo(shop) {
    if (shop.interest_rate && shop.ir_unit) {
        if (shop.ir_unit === '%') {
            return `${shop.interest_rate}${shop.ir_unit}`;
        } else {
            return `${shop.interest_rate}${shop.ir_unit}`;
        }
    }
    return '';
}

// ショップ詳細を表示
function showShopDetail(event, shopId) {
    event.preventDefault();
    
    // ショップを検索
    let targetShop = null;
    for (const shops of Object.values(allShopsData)) {
        targetShop = shops.find(shop => shop.id == shopId);
        if (targetShop) break;
    }
    
    if (!targetShop) return;
    
    // モーダルに詳細情報を表示
    const modal = document.getElementById('shopModal');
    const modalBody = document.getElementById('modalBody');
    
    const logoPath = targetShop.logo_img_pc ? targetShop.logo_img_pc.replace('public/', '') : '';
    const rewardInfo = formatRewardInfo(targetShop);
    
    modalBody.innerHTML = `
        <h2>${targetShop.name}</h2>
        ${logoPath ? `<img src="${logoPath}" alt="${targetShop.name}" style="max-width: 200px; margin: 1rem 0;">` : ''}
        <p style="margin-bottom: 1rem;">${targetShop.explanation}</p>
        
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
            <h3 style="color: #667eea; margin-bottom: 0.5rem;">支援金情報</h3>
            <p>${targetShop.ir_text_front} <strong style="color: #e74c3c; font-size: 1.2rem;">${rewardInfo}</strong> ${targetShop.ir_text_after}</p>
        </div>
        
        ${targetShop.annotation ? `
        <div style="margin-bottom: 1rem;">
            <h4 style="color: #555; margin-bottom: 0.5rem;">注意事項</h4>
            <p style="font-size: 0.9rem; color: #666; white-space: pre-wrap;">${targetShop.annotation}</p>
        </div>
        ` : ''}
        
        ${targetShop.annotation_modal ? `
        <div style="background-color: #ffe6e6; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
            <p style="font-size: 0.9rem; color: #d9534f; white-space: pre-wrap;">${targetShop.annotation_modal}</p>
        </div>
        ` : ''}
        
        <a href="${targetShop.promo_url_pc}" target="_blank" class="shop-link" style="display: inline-block; margin-top: 1rem;">ショップサイトへ移動</a>
    `;
    
    modal.style.display = 'block';
}

// イベントリスナー設定
function setupEventListeners() {
    // 検索ボックス
    document.getElementById('searchBox').addEventListener('input', displayShops);
    
    // おすすめフィルター
    document.getElementById('showRecommended').addEventListener('change', function(e) {
        showRecommended = e.target.checked;
        displayShops();
    });
    
    // モーダルクローズボタン
    document.querySelector('.close').addEventListener('click', function() {
        document.getElementById('shopModal').style.display = 'none';
    });
    
    // モーダル外クリックで閉じる
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('shopModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}