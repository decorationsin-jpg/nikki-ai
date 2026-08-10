"""
Nikki Direct Google Search Engine Reader & Scraper.
Allows Nikki to search Google directly, parse featured snippets, knowledge boxes,
and web result links, and deliver verified answers as per Google Search results.
"""
import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from typing import Dict, Any, List

class GoogleSearchEngine:
    """
    Direct Google Search Engine Integration & Scraper.
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def search_google(self, query: str, num_results: int = 4) -> Dict[str, Any]:
        """
        Queries Google Search directly, parses search result snippets, answer boxes, and links.
        """
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}&hl=en"

        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                html_content = response.read().decode('utf-8', errors='ignore')

            soup = BeautifulSoup(html_content, 'html.parser')
            
            snippets = []
            sources = []

            # Extract Google Featured Snippets / Knowledge Cards
            featured_box = soup.select_one('.Z0LcW, .VwiC3b, .wGLgfd, .hgKmu')
            featured_text = featured_box.get_text().strip() if featured_box else ""

            # Extract Top Organic Result Snippets
            for g in soup.select('.g')[:num_results]:
                title_elem = g.select_one('h3')
                snippet_elem = g.select_one('.VwiC3b, .s3tdfe, .st')
                link_elem = g.select_one('a')

                title = title_elem.get_text() if title_elem else "Google Result"
                snippet = snippet_elem.get_text() if snippet_elem else ""
                href = link_elem.get('href') if link_elem else ""

                if snippet:
                    snippets.append(f"• **{title}**: {snippet}")
                if href and href.startswith('http'):
                    sources.append(href)

            # Combine search result facts
            primary_answer = featured_text if featured_text else ("\n".join(snippets[:3]) if snippets else "No direct Google answer box found.")

            return {
                "query": query,
                "featured_snippet": featured_text,
                "snippets": snippets,
                "sources": list(set(sources))[:3],
                "summary": primary_answer
            }
        except Exception as e:
            return {
                "query": query,
                "error": f"Google Search connection error: {str(e)}",
                "summary": f"Could not retrieve Google Search results directly due to connection limit. Error: {str(e)}"
            }

    def get_google_answer(self, query: str) -> str:
        """
        Fetches Google Search results and formats a clear response 'As per Google Search Results'.
        """
        print(f"🔍 [Nikki Google Search Engine]: Reading Google Search for '{query}'...")
        res = self.search_google(query)

        if "error" in res and not res.get("snippets"):
            return f"As per search result attempt: {res['error']}"

        answer = f"🌐 **As per Google Search Results for '{query}'**:\n\n"
        answer += f"{res['summary']}\n\n"

        if res.get("sources"):
            answer += "📌 **Google Web Sources**:\n"
            for src in res["sources"]:
                answer += f"- [{src}]\n"

        return answer
