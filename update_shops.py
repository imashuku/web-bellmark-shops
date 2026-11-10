#!/usr/bin/env python3
"""
掲載ショップ一覧の月次更新を1本で通す。

毎月やること:
  1. Box から `YYYYMMDD_companies.csv` をこのディレクトリに置く
  2. `python3 update_shops.py` を実行する

以上。ファイル名も日付も、CSV のファイル名から自動で決まる。
手で書き換える場所は無くなった（従来は fix_csv.py・parse_csv.py のファイル名と
generate_html.py の日付を、毎月4か所書き換えていた）。

  python3 update_shops.py                    # 最新CSVを自動で拾って生成
  python3 update_shops.py 20260910_companies.csv
  python3 update_shops.py --deploy           # 生成後に vercel --prod まで
  python3 update_shops.py --check            # 生成せず、直近の状態だけ点検

安全弁:
  - 店舗数が想定レンジ（既定 180〜280）を外れたら止める。
    CSV が壊れていたり列がずれていたときに、空の一覧を本番へ出さないため。
  - 前回の店舗数と比べて増減が大きいときは警告する（止めはしない）。
  - --deploy は生成が全部通ったときだけ走る。
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_RE = re.compile(r"^(\d{8})_companies\.csv$")

MIN_SHOPS = 180
MAX_SHOPS = 280
# 前回比でこれ以上動いたら警告（率）
DELTA_WARN = 0.15


def die(msg: str) -> None:
    print(f"\n🔴 中止: {msg}", file=sys.stderr)
    sys.exit(1)


def find_latest_csv() -> Path:
    """`YYYYMMDD_companies.csv` のうち日付が最も新しいものを返す。"""
    candidates = []
    for p in HERE.iterdir():
        m = CSV_RE.match(p.name)
        if m:
            candidates.append((m.group(1), p))
    if not candidates:
        die("`YYYYMMDD_companies.csv` が見つかりません。Box から落としてこのディレクトリに置いてください。")
    candidates.sort()
    return candidates[-1][1]


def date_label(stamp: str) -> str:
    """`20260810` → `2026年8月現在`"""
    return f"{int(stamp[0:4])}年{int(stamp[4:6])}月現在"


def previous_total() -> int | None:
    """前回生成した shops_data.json の店舗数。無ければ None。"""
    f = HERE / "shops_data.json"
    if not f.exists():
        return None
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return sum(len(v) for v in data.values())
    except Exception:
        return None


def source_label(src: Path, override: str | None = None) -> str:
    """Reuse an explicitly supplied label only for the same unchanged source."""
    if override:
        return override
    meta_path = HERE / "shops_source.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if meta.get("source") == src.name and meta.get("sha256") == digest:
            return meta["label"]
    return date_label(CSV_RE.match(src.name).group(1))


def run_check(label: str | None = None) -> int:
    """生成せずに、いま本番へ出ている中身の整合だけ見る。"""
    idx = HERE / "index.html"
    data = HERE / "shops_data.json"
    if not idx.exists() or not data.exists():
        die("index.html か shops_data.json がありません。まず生成してください。")
    total = previous_total()
    html = idx.read_text(encoding="utf-8")
    m = re.search(r'class="date-note">([^<]+)<', html)
    print(f"shops_data.json: {total}店舗")
    print(f"index.html の日付表記: {m.group(1) if m else '（見つかりません）'}")
    print(f"index.html のサイズ: {idx.stat().st_size:,} bytes")
    latest = find_latest_csv()
    stamp = CSV_RE.match(latest.name).group(1)
    want = source_label(latest, label)
    if m and m.group(1) != want:
        print(f"\n🟠 最新CSV {latest.name} は「{want}」ですが、index.html は「{m.group(1)}」のままです。")
        return 1
    print("\n✅ 最新CSVと index.html の日付が一致しています。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("csv", nargs="?", help="取り込むCSV（省略時は最新の YYYYMMDD_companies.csv）")
    ap.add_argument("--deploy", action="store_true", help="生成が通ったら vercel --prod --yes まで実行")
    ap.add_argument("--check", action="store_true", help="生成せず、いまの状態だけ点検して終わる")
    ap.add_argument("--label", help="表示する対象月・提供日（CSV日付と対象月が異なる場合）")
    args = ap.parse_args()

    os.chdir(HERE)

    if args.check:
        return run_check(args.label)

    src = Path(args.csv) if args.csv else find_latest_csv()
    if not src.is_absolute():
        src = HERE / src
    if not src.exists():
        die(f"{src.name} が見つかりません。")

    m = CSV_RE.match(src.name)
    if not m:
        die(f"CSVのファイル名が `YYYYMMDD_companies.csv` の形式ではありません: {src.name}")
    stamp = m.group(1)
    label = source_label(src, args.label)
    fixed = HERE / f"{stamp}_companies_fixed.csv"

    print(f"■ 取り込むCSV : {src.name}")
    print(f"■ 日付表記     : {label}")
    print()

    # ---- 1. 改行混入の修正 ----
    print("── 1/3 CSVの整形 ──")
    sys.path.insert(0, str(HERE))
    from fix_csv import fix_csv  # noqa: E402
    fix_csv(str(src), str(fixed))

    # ---- 2. JSON化 ----
    print("\n── 2/3 shops_data.json の生成 ──")
    from parse_csv import parse_shops  # noqa: E402
    shops = parse_shops(str(fixed))
    total = sum(len(v) for v in shops.values())

    if not (MIN_SHOPS <= total <= MAX_SHOPS):
        die(
            f"店舗数が {total} 件で想定レンジ {MIN_SHOPS}〜{MAX_SHOPS} を外れています。\n"
            f"      CSVの列ずれ・文字コード・ダウンロード途中切れを疑ってください。\n"
            f"      （index.html は書き換えていません。本番は無傷です）"
        )

    prev = previous_total()
    (HERE / "shops_data.json").write_text(
        json.dumps(shops, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for cat, lst in sorted(shops.items(), key=lambda kv: -len(kv[1])):
        print(f"  {cat}: {len(lst)}件")
    print(f"  ── 合計 {total}件")

    if prev is not None and prev > 0:
        delta = total - prev
        rate = abs(delta) / prev
        mark = "🟠" if rate > DELTA_WARN else "  "
        print(f"{mark} 前回 {prev}件 → 今回 {total}件（{delta:+d}件）")
        if rate > DELTA_WARN:
            print(f"   増減が {rate:.0%} あります。CSVが正しいか一度目で確認してください。")

    # ---- 3. HTML生成 ----
    print("\n── 3/3 index.html の生成 ──")
    env = {**os.environ, "SHOPS_DATE": label}
    r = subprocess.run([sys.executable, "generate_html.py"], cwd=HERE, env=env)
    if r.returncode != 0:
        die("generate_html.py が失敗しました。")

    # 生成物の検算（日付が本当に入ったか・空でないか）
    html = (HERE / "index.html").read_text(encoding="utf-8")
    if label not in html:
        die(f"index.html に「{label}」が入っていません。generate_html.py の差し込み先を確認してください。")
    print(f"  index.html: {len(html.encode('utf-8')):,} bytes ／ 日付「{label}」を確認")

    (HERE / "shops_source.json").write_text(json.dumps({
        "source": src.name,
        "sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "label": label,
        "total": total,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n✅ 生成完了")
    print(f"   {src.name} → {fixed.name} → shops_data.json → index.html")

    if args.deploy:
        print("\n── デプロイ ──")
        r = subprocess.run(["vercel", "--prod", "--yes"], cwd=HERE)
        if r.returncode != 0:
            die("vercel のデプロイが失敗しました。生成物はできているので、手で `vercel --prod --yes` を試してください。")
        print("\n✅ 本番へ反映しました")
    else:
        print("\n次: 目で index.html を確認 →  python3 update_shops.py --deploy  か  vercel --prod --yes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
