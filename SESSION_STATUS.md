# セッション状態記録

最終更新: 2025年11月

## プロジェクト概要

ウェブベルマークの掲載ショップ一覧を表示するWebアプリケーションです。CSVデータから店舗情報を処理し、カテゴリ別に閲覧できるWebインターフェースを生成します。

## 現在の状態

### データファイル
- **最新CSV**: `Companies Nov 17 2025_fixed.csv`
- **生成JSON**: `shops_data.json`
- **生成HTML**: `shops_list.html`（メイン出力ファイル）

### 主要スクリプト
1. **parse_csv.py**: CSVからJSONデータを生成
   - 入力: `Companies Nov 17 2025_fixed.csv`
   - 出力: `shops_data.json`
   - フィルタ条件: `is_valid=1`, `delete_flag=0`

2. **generate_html.py**: JSONから完全なHTMLページを生成
   - 入力: `shops_data.json`
   - 出力: `shops_list.html`
   - 機能: CSS/JS埋め込みのスタンドアロンHTML

3. **category_analysis.py**: カテゴリ分布の分析ツール

4. **recategorize_shops.py**: ショップ内容に基づく代替カテゴリ分類

### カテゴリマッピング
カテゴリID 1-21（欠番あり）を日本語名にマッピング：
- 1: インテリア・生活雑貨・ペット用品
- 2: 買取・中古品販売
- 3: キッズ・ベビー・おもちゃ
- 4: レジャー・エンタメ・体験
- 5: 食品・飲料・グルメ予約
- 6: ファッション・アパレル
- 7: フラワー・ギフト
- 8: サービス・その他
- 9: 家電・PC・カメラ（最多）
- 10: スポーツ・アウトドア
- 11: 総合通販・百貨店（アスクル含む）
- 12: 美容・コスメ・健康
- 13: 本・音楽・ゲーム
- 14: 旅行・宿泊予約
- 16: 教育用品
- 17: 動画配信サービス
- 18: 教育・学習サービス
- 21: その他

### 主要機能
- 📱 レスポンシブデザイン（PC・スマートフォン対応）
- 🔍 ショップ名検索機能
- ⭐ おすすめショップフィルター
- 📤 SNS共有機能（LINE、Twitter、Facebook）
- 🖨️ 印刷・PDF保存機能（A4サイズ最適化）
- 🏷️ カテゴリ別表示

## クイックスタート

### データを再生成する場合
```bash
# 1. CSVからJSONデータを生成
python3 parse_csv.py

# 2. HTMLファイルを生成
python3 generate_html.py

# 3. ブラウザで開く
open shops_list.html  # macOS
# または
start shops_list.html  # Windows
```

### カテゴリ分析を実行する場合
```bash
python3 category_analysis.py
```

## 重要なデータ属性

- **is_valid**: ショップを含めるには"1"必須
- **delete_flag**: ショップを含めるには"0"必須
- **is_recommend**: おすすめバッジ用のブール値
- **interest_rate + ir_unit**: 支援金額（小数点%または整数点数でフォーマット）
- **ir_text_front**: 率の前のテキスト（"支援金は\n"を削除）
- **order**: カテゴリ内の表示順

## テキスト処理の注意点

- 説明文と支援金テキストから\nと\\nをすべて削除
- パーセンテージは小数点第2位まで表示（0.43%）
- 点数は整数表示（2000点）
- カテゴリ表示順は小学生の保護者（主要ユーザー）向けに最適化

## ファイル構成

```
.
├── Companies Nov 17 2025_fixed.csv  # 最新のCSVデータ
├── Companies Nov 17 2025.csv        # 元データ
├── Companies Oct 9 2025.csv         # 旧データ
├── parse_csv.py                      # CSV→JSON変換スクリプト
├── generate_html.py                  # HTML生成スクリプト
├── category_analysis.py              # カテゴリ分析ツール
├── recategorize_shops.py             # カテゴリ再分類ツール
├── shops_data.json                   # 生成されたJSONデータ
├── shops_data_corrected.json         # 修正版JSONデータ
├── shops_data.js                     # JS形式のデータ
├── shops_list.html                   # 生成されたHTMLファイル（メイン）
├── index.html                        # 別のHTMLファイル
├── script.js                         # JavaScriptファイル
├── styles.css                        # CSSファイル
├── categories.txt                    # カテゴリリスト
├── README.md                         # プロジェクト説明
├── CLAUDE.md                         # 開発者向けドキュメント
├── SESSION_STATUS.md                 # このファイル（セッション状態）
└── カテゴリ分析結果.md               # カテゴリ分析結果

```

## 次回セッション開始時の確認事項

1. 最新のCSVファイルが更新されていないか確認
2. `shops_data.json`が最新か確認（必要に応じて`parse_csv.py`を実行）
3. `shops_list.html`が最新か確認（必要に応じて`generate_html.py`を実行）
4. ブラウザで`shops_list.html`を開いて動作確認

## 参考ドキュメント

- `README.md`: プロジェクトの概要とセットアップ手順
- `CLAUDE.md`: 開発者向けの詳細な技術情報
- `カテゴリ分析結果.md`: カテゴリ分布の分析結果

