#!/usr/bin/env python3
"""
CSVファイル内のフィールドに含まれる改行文字を修正するスクリプト

問題: フィールド内の \n が実際の改行として扱われ、レコードが複数行に分割される
解決: フィールド内の改行を削除し、正しいCSV形式に修正する
"""

def fix_csv(input_file, output_file):
    """
    CSVファイルのフィールド内改行を修正

    戦略:
    1. ファイル全体を読み込む
    2. 各論理レコードを再構築（company_idで始まる行を検出）
    3. フィールド内の改行を削除
    4. 正しい形式で出力
    """

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # ヘッダー行を保存
    header = lines[0].strip()
    expected_columns = header.count(',') + 1  # 24列

    print(f"ヘッダー: {expected_columns}列")

    # レコードを再構築
    records = []
    current_record = []

    for i, line in enumerate(lines[1:], start=2):
        line = line.strip()

        # 空行はスキップ
        if not line:
            continue

        # 数字で始まる行は新しいレコードの開始
        if line[0].isdigit() and ',' in line:
            # 前のレコードを保存
            if current_record:
                merged = ''.join(current_record)
                records.append(merged)

            # 新しいレコードを開始
            current_record = [line]
        else:
            # 前のレコードの続き
            if current_record:
                current_record.append(line)

    # 最後のレコードを保存
    if current_record:
        merged = ''.join(current_record)
        records.append(merged)

    print(f"抽出したレコード数: {len(records)}")

    # 出力ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        f.write(header + '\n')
        for record in records:
            f.write(record + '\n')

    print(f"修正完了: {output_file}")

    # 検証
    print("\n検証中...")
    import csv
    valid_count = 0
    total_count = 0

    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_count += 1
            if row['is_valid'] == '1' and row['delete_flag'] == '0':
                valid_count += 1

    print(f"総レコード数: {total_count}")
    print(f"有効レコード数 (is_valid=1 & delete_flag=0): {valid_count}")

if __name__ == "__main__":
    input_file = '20251210_companies.csv'
    output_file = '20251210_companies_fixed.csv'

    fix_csv(input_file, output_file)
