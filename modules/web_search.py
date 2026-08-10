import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

class FreeWebSearch:
    """
    Direct web search & page reader WITHOUT requiring any API key.
    Uses DuckDuckGo HTML search and direct page scraping.
    """

    @staticmethod
    def search(query: str, max_results: int = 5) -> list:
        """Performs free web search via DuckDuckGo HTML endpoint without API keys."""
        try:
            # First try using duckduckgo_search library if installed
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                return [{"title": r.get('title'), "href": r.get('href'), "snippet": r.get('body')} for r in results]
        except Exception:
            # Fallback to direct HTML search scraping
            encoded_query = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html = resp.read().decode('utf-8')
                    soup = BeautifulSoup(html, 'html.parser')
                    results = []
                    for a in soup.find_all('a', class_='result__a', limit=max_results):
                        results.append({
                            "title": a.get_text(),
                            "href": a.get('href'),
                            "snippet": ""
                        })
                    return results
            except Exception as e:
                return [{"error": f"Search failed: {str(e)}"}]

    @staticmethod
    def fetch_page_text(url: str, max_chars: int = 3000) -> str:
        """Scrapes and extracts readable text from any website URL without API keys."""
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text(separator=' ')
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_text = '\n'.join(chunk for chunk in chunks if chunk)
                return clean_text[:max_chars]
        except Exception as e:
            return f"Failed to fetch content from {url}: {str(e)}"
