# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## プロジェクト概要

ウェブベルマークの掲載ショップ一覧を表示するWebアプリケーションです。ユーザーが買い物をすることで学校を支援できる仕組みで、CSVデータから店舗情報を処理してカテゴリ別に閲覧できるWebインターフェースを生成します。

## 主要コマンド

### データ処理
```bash
# CSVからJSONデータを生成（最初に実行）
python3 parse_csv.py

# 全機能を含む静的HTMLページを生成
python3 generate_html.py

# ショップカテゴリを分析
python3 category_analysis.py

# ショップ内容に基づく代替カテゴリ分類
python3 recategorize_shops.py
```

### データフロー
```
Companies Oct 9 2025.csv → parse_csv.py → shops_data.json → generate_html.py → shops_list.html
```

## アーキテクチャ

### データ処理スクリプト
- **parse_csv.py**: CSVを読み込み、有効なショップ（is_valid=1、delete_flag=0）をフィルタリング、category_idでグループ化してJSON出力
- **generate_html.py**: shops_data.jsonを読み込み、CSS/JS埋め込みの完全な静的HTMLを生成
- **category_analysis.py**: データ検証のためのカテゴリ分布分析

### カテゴリシステム
カテゴリID 1-21（欠番あり）を日本語名にマッピング：
- 1: インテリア・生活雑貨・ペット用品
- 9: 家電・PC・カメラ（33店舗 - 最多）
- 11: 総合通販・百貨店（28店舗 - アスクル含む）
- 14: 旅行・宿泊予約（26店舗）

### HTML機能
- ショップ名検索
- おすすめショップフィルター
- SNS共有（LINE、Twitter、Facebook、URLコピー）
- A4サイズ最適化の印刷/PDF出力
- レスポンシブデザイン
- 支援率表示（%または点数）

### 重要なデータ属性
- **is_valid**: ショップを含めるには"1"必須
- **delete_flag**: ショップを含めるには"0"必須
- **is_recommend**: おすすめバッジ用のブール値
- **interest_rate + ir_unit**: 支援金額（小数点%または整数点数でフォーマット）
- **ir_text_front**: 率の前のテキスト（"支援金は\n"を削除）
- **order**: カテゴリ内の表示順

### テキスト処理の注意点
- 説明文と支援金テキストから\nと\\nをすべて削除
- パーセンテージは小数点第2位まで表示（0.43%）
- 点数は整数表示（2000点）
- カテゴリ表示順は小学生の保護者（主要ユーザー）向けに最適化

## 現在の出力

メイン成果物は `shops_list.html` - Webサーバーなしでブラウザで直接開ける完全なスタンドアロンWebページです。