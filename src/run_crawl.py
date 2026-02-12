import logging
from .scraper.main import DepartmentScraper
from .processor.converter import HtmlToMarkdown
from .utils.config import TARGET_BASE_URL, PROCESSED_DATA_DIR
from urllib.parse import urljoin, urlparse
from pathlib import Path

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    scraper = DepartmentScraper()
    processor = HtmlToMarkdown()
    
    # 起点となるURL（体系目次から辿るのが効率的）
    start_url = urljoin(TARGET_BASE_URL, "reiki_taikei/taikei_default.html")
    
    logger.info(f"Starting incremental crawl from: {start_url}")
    
    queue = [(start_url, 0)]
    count = 0
    max_docs = 50 # 最初は50件に制限
    
    while queue and count < max_docs:
        url, depth = queue.pop(0)
        
        if url in scraper.visited_urls or depth > 2:
            continue
            
        scraper.visited_urls.add(url)
        html = scraper.fetch_page(url)
        
        if not html:
            continue
            
        # リンクの抽出（深さが2未満の場合）
        if depth < 2:
            new_links = scraper.extract_links(html, url)
            for link in new_links:
                if link not in scraper.visited_urls:
                    queue.append((link, depth + 1))
        
        # 実際の例規本文と思われるページのみを変換・保存（深さ2を優先）
        if depth == 2:
            md_content = f"Source: {url}\n\n" + processor.convert(html)
            
            # 短すぎる、または本文がないページを除外
            if len(md_content) < 500:
                logger.info(f"Skipping short content or menu: {url}")
                continue
                
            # URLから安全なファイル名を生成
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip("/").split("/")
            filename_base = "_".join(path_parts[-2:]) if len(path_parts) >= 2 else path_parts[-1]
            filename_base = filename_base.replace(".html", "")
            
            processor.save_markdown(md_content, f"{filename_base}.md")
            count += 1
            logger.info(f"Progress: {count}/{max_docs} documents saved.")

    logger.info(f"Incremental processing completed. Total documents saved: {count}")
    print(f"\n--- Crawl & Conversion Summary ---")
    print(f"Total Documents saved: {count}")
    print(f"Output directory: {PROCESSED_DATA_DIR}")

if __name__ == "__main__":
    main()
