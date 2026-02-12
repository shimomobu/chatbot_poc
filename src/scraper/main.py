import requests
import time
import logging
from pathlib import Path
from typing import Optional, List, Set, Dict
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from ..utils.config import USER_AGENT, REQUEST_DELAY, RAW_DATA_DIR

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DepartmentScraper:
    """
    自治体ウェブサイトからHTMLを取得し、巡回（クローリング）するためのクラス
    """
    
    def __init__(self):
        self.headers = {
            "User-Agent": USER_AGENT
        }
        self.visited_urls: Set[str] = set()
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        指定されたURLからページを取得します。
        """
        try:
            time.sleep(REQUEST_DELAY) # サーバー負荷への配慮
            logger.info(f"Fetching URL: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 文字コードの自動推定
            response.encoding = response.apparent_encoding
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

    def extract_links(self, html_content: str, base_url: str) -> List[str]:
        """
        HTML内からリンクを抽出し、絶対URLのリストを返します。
        同一ドメインのリンクのみに制限します。
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        domain = urlparse(base_url).netloc
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # 相対パスを絶対URLに変換
            absolute_url = urljoin(base_url, href)
            
            # フラグメント（#...）を除去
            absolute_url = absolute_url.split('#')[0]
            
            # ドメイン制限と重複チェック
            if urlparse(absolute_url).netloc == domain:
                if absolute_url not in self.visited_urls:
                    links.append(absolute_url)
        
        return list(set(links))

    def crawl(self, start_url: str, max_depth: int = 2) -> Dict[str, str]:
        """
        指定されたURLを起点に、最大深度までクローリングを行います。
        URLとHTML内容の辞書を返します。
        """
        pages_content = {}
        queue = [(start_url, 0)] # (url, current_depth)
        
        while queue:
            url, depth = queue.pop(0)
            
            if url in self.visited_urls or depth > max_depth:
                continue
            
            self.visited_urls.add(url)
            html = self.fetch_page(url)
            
            if html:
                pages_content[url] = html
                logger.info(f"Successfully crawled: {url} (Depth: {depth})")
                
                if depth < max_depth:
                    new_links = self.extract_links(html, url)
                    for link in new_links:
                        if link not in self.visited_urls:
                            queue.append((link, depth + 1))
        
        return pages_content

    def save_raw_html(self, html_content: str, filename: str) -> Path:
        """
        取得したHTMLを保存します。
        """
        file_path = RAW_DATA_DIR / filename
        try:
            # ファイル名に使用できない文字を置換
            safe_filename = "".join([c if c.isalnum() or c in "._-" else "_" for c in filename])
            target_path = RAW_DATA_DIR / safe_filename
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"Saved raw HTML to: {target_path}")
            return target_path
        except IOError as e:
            logger.error(f"Error saving file {filename}: {e}")
            raise

if __name__ == "__main__":
    pass
