import os
from pathlib import Path

# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# データディレクトリの設定
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# ターゲット設定 (山口県熊毛郡上関町)
# 例規集のトップページや検索システムのURLをここに定義します
TARGET_BASE_URL = "https://www.town.kaminoseki.lg.jp/reiki_int/reiki_menu.html" # 仮のURL

# スクレイピング設定
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
REQUEST_DELAY = 1.0  # サーバー負荷軽減のための待機時間（秒）

# ディレクトリの自動作成
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
