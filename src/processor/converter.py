import re
from bs4 import BeautifulSoup
import logging
from pathlib import Path
from typing import Optional
import markdownify
from ..utils.config import PROCESSED_DATA_DIR

logger = logging.getLogger(__name__)

class HtmlToMarkdown:
    """
    HTMLをMarkdownへ変換し、構造化データを生成するクラス
    """
    
    def __init__(self):
        pass

    def convert(self, html_content: str) -> str:
        """
        HTMLを受け取り、整形されたMarkdownを返します。
        基本的なHTMLタグ除去に加え、条文構造の保持を試みます。
        
        Args:
            html_content (str): 生のHTMLデータ
            
        Returns:
            str: 変換後のMarkdown
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 不要なタグの除去（スクリプト、スタイル、ナビゲーションなど）
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
            
        # 本文領域の抽出（サイト構造に合わせて調整が必要。ここでは汎用的な'main'や'body'を想定）
        # 実際の実装では、例規集サイト特有の div class="reiki-body" などを指定します
        content_div = soup.find('div', class_='reiki_body') or soup.find('main') or soup.body
        
        if not content_div:
            logger.warning("Could not find main content area. Converting entire body.")
            content_div = soup.body

        # markdownifyを使用して基本変換
        md_text = markdownify.markdownify(str(content_div), heading_style="ATX")
        
        # 不要な空行の削除などのクリーンアップ
        md_text = self._cleanup_markdown(md_text)
        
        return md_text

    def _cleanup_markdown(self, text: str) -> str:
        """
        Markdownテキストの整形を行います。
        """
        # 連続する空行を1つにまとめる
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 行頭・行末の空白除去
        text = text.strip()
        
        return text

    def save_markdown(self, md_content: str, filename: str) -> Path:
        """
        Markdownファイルを保存します。
        
        Args:
            md_content (str): Markdownテキスト
            filename (str): ファイル名 (.md拡張子)
            
        Returns:
            Path: 保存先のパス
        """
        if not filename.endswith('.md'):
            filename += '.md'
            
        file_path = PROCESSED_DATA_DIR / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            logger.info(f"Saved Markdown to: {file_path}")
            return file_path
        except IOError as e:
            logger.error(f"Error saving markdown {filename}: {e}")
            raise

if __name__ == "__main__":
    # テスト実行用
    processor = HtmlToMarkdown()
    # sample_html = "<html><body><h1>第1条</h1><p>この規則は...</p></body></html>"
    # md = processor.convert(sample_html)
    # processor.save_markdown(md, "test_article.md")
    pass
