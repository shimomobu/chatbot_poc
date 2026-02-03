import requests
import time
import logging
from pathlib import Path
from typing import Optional
from ..utils.config import USER_AGENT, REQUEST_DELAY, RAW_DATA_DIR

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DepartmentScraper:
    """
    自治体ウェブサイトからHTMLを取得するためのスクレイパークラス
    """
    
    def __init__(self):
        self.headers = {
            "User-Agent": USER_AGENT
        }
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        指定されたURLからページを取得します。
        
        Args:
            url (str): 取得対象のURL
            
        Returns:
            Optional[str]: 取得成功時はHTMLテキスト、失敗時はNone
        """
        try:
            time.sleep(REQUEST_DELAY) # サーバー負荷への配慮
            logger.info(f"Fetching URL: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 文字コードの自動推定（必要に応じて 'CP932' や 'EUC-JP' などを指定）
            response.encoding = response.apparent_encoding
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

    def save_raw_html(self, html_content: str, filename: str) -> Path:
        """
        取得したHTMLを保存します。
        
        Args:
            html_content (str): 保存するHTML
            filename (str): ファイル名
            
        Returns:
            Path: 保存されたファイルのパス
        """
        file_path = RAW_DATA_DIR / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"Saved raw HTML to: {file_path}")
            return file_path
        except IOError as e:
            logger.error(f"Error saving file {filename}: {e}")
            raise

if __name__ == "__main__":
    # テスト実行用
    scraper = DepartmentScraper()
    # デモ用のURL (実際にはconfig.pyのTARGET_BASE_URL等を使用)
    # url = "https://example.com"
    # content = scraper.fetch_page(url)
    # if content:
    #     scraper.save_raw_html(content, "test_page.html")
    pass
