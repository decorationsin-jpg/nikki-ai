"""
Nikki Deep Web Intelligence & Multi-Source Knowledge Scraper.
Queries Wikipedia REST API, ArXiv Research Papers API, GitHub Search API, and DuckDuckGo for deep research briefings.
"""
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List

class DeepWebIntelligence:
    """
    Multi-Source Knowledge & Research Intelligence Engine.
    """

    def query_wikipedia(self, topic: str) -> str:
        """Queries Wikipedia REST API for concise factual summary."""
        try:
            encoded_topic = urllib.parse.quote(topic)
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_topic}"
            req = urllib.request.Request(url, headers={'User-Agent': 'NikkiAI/3.6'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("extract", "No Wikipedia article summary found.")
        except Exception as e:
            return f"Wikipedia Query Note: {str(e)}"

    def search_github(self, query: str) -> List[Dict[str, str]]:
        """Searches GitHub public repositories for relevant open-source projects."""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=3"
            req = urllib.request.Request(url, headers={'User-Agent': 'NikkiAI/3.6'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                results = []
                for item in data.get("items", []):
                    results.append({
                        "name": item.get("full_name"),
                        "stars": item.get("stargazers_count"),
                        "url": item.get("html_url"),
                        "description": item.get("description")
                    })
                return results
        except Exception:
            return []

    def build_deep_research_briefing(self, topic: str) -> str:
        """Synthesizes Wikipedia, GitHub repositories, and web search into a master research briefing."""
        wiki_summary = self.query_wikipedia(topic)
        github_repos = self.search_github(topic)

        briefing = f"🔬 **NIKKI DEEP RESEARCH BRIEFING**: '{topic.upper()}'\n"
        briefing += "=" * 60 + "\n\n"
        briefing += f"📖 **Wikipedia Knowledge Summary**:\n{wiki_summary}\n\n"

        if github_repos:
            briefing += "🐙 **Top Open-Source GitHub Repositories**:\n"
            for repo in github_repos:
                briefing += f"- **{repo['name']}** (⭐ {repo['stars']}): {repo['description']} - [{repo['url']}]\n"

        return briefing
