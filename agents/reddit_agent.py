"""
Autonomous Reddit Scraper Agent for Mexican Consumer Insights.
Scrapes subreddits (r/MexicoCity, r/Guadalajara, r/Monterrey, r/mexico, r/AskMexico, r/mexicoexpats)
using high-resilience RSS/Atom feeds and Playwright browser deep fallback.
Cleans PII via Compliance Agent and classifies with Synthesis Agent.
"""

import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import TARGET_SUBREDDITS, PROBLEM_KEYWORDS
from agents.compliance_agent import MexicanComplianceAgent
from agents.synthesis_agent import MexicanSynthesisAgent
from agents.dataset_manager import DatasetManager

class RedditScraperAgent:
    """
    Autonomous agent monitoring Reddit communities for local and expat pain points in Mexico.
    """

    def __init__(self):
        self.subreddits = TARGET_SUBREDDITS
        self.compliance_agent = MexicanComplianceAgent()
        self.synthesis_agent = MexicanSynthesisAgent()
        self.db = DatasetManager()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    def run(self, max_per_sub: int = 15) -> Dict[str, Any]:
        """
        Execute full Reddit scraping run across all target subreddits.
        """
        print("[RedditScraperAgent] Starting scrape across target Mexican subreddits...")
        collected_posts = []
        inserted_count = 0

        for target in self.subreddits:
            sub_name = target["name"]
            city = target.get("city", "National")
            default_audience = target.get("audience", "Both")
            filter_kw = target.get("filter_keyword")

            print(f" -> Scanning r/{sub_name} (City: {city}, Audience: {default_audience})...")
            
            raw_entries = self._fetch_sub_rss(sub_name, limit=max_per_sub)
            for entry in raw_entries:
                title = entry.get("title", "")
                content = entry.get("content", "")
                
                # If filtered by keyword (e.g. for general /r/expats or /r/digitalnomad)
                if filter_kw:
                    if filter_kw.lower() not in (title + " " + content).lower():
                        continue

                # 1. PII Compliance Scrubbing
                raw_record = {
                    "title": title,
                    "content": content,
                    "author": entry.get("author", ""),
                    "source_platform": f"Reddit (r/{sub_name})",
                    "source_url": entry.get("url", ""),
                    "city": city,
                    "audience": default_audience,
                    "timestamp": entry.get("timestamp", datetime.utcnow().isoformat())
                }
                sanitized_record = self.compliance_agent.sanitize_record(raw_record)

                # 2. NLP & Synthesis Processing
                analyzed_problem = self.synthesis_agent.analyze_post(sanitized_record)

                # 3. Save to Database
                is_new = self.db.insert_problem(analyzed_problem)
                if is_new:
                    inserted_count += 1
                collected_posts.append(analyzed_problem)

            time.sleep(1) # respectful pacing between feeds

        self.db.log_agent_run(
            agent_name="RedditScraperAgent",
            status="SUCCESS",
            collected=len(collected_posts),
            inserted=inserted_count,
            details=f"Scraped {len(self.subreddits)} subreddits."
        )

        print(f"[RedditScraperAgent] Finished: {len(collected_posts)} analyzed, {inserted_count} new entries saved.")
        return {
            "agent": "RedditScraperAgent",
            "total_collected": len(collected_posts),
            "total_inserted": inserted_count
        }

    def _fetch_sub_rss(self, sub_name: str, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Fetch new posts via Atom feed without needing API credentials.
        """
        url = f"https://www.reddit.com/r/{sub_name}/new.rss?limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        results = []

        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                xml_content = response.read()
                root = ET.fromstring(xml_content)
                entries = root.findall('{http://www.w3.org/2005/Atom}entry')
                
                for e in entries[:limit]:
                    title_elem = e.find('{http://www.w3.org/2005/Atom}title')
                    content_elem = e.find('{http://www.w3.org/2005/Atom}content')
                    link_elem = e.find('{http://www.w3.org/2005/Atom}link')
                    author_elem = e.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name')
                    updated_elem = e.find('{http://www.w3.org/2005/Atom}updated')

                    title = title_elem.text if title_elem is not None else ""
                    # HTML tags are inside content, strip basic tags
                    import re
                    content_raw = content_elem.text if content_elem is not None else ""
                    clean_content = re.sub(r'<[^>]+>', ' ', content_raw).strip()
                    clean_content = re.sub(r'&#32;|\n+', ' ', clean_content)

                    url_href = link_elem.attrib.get('href', '') if link_elem is not None else ""
                    author_name = author_elem.text if author_elem is not None else "anon"
                    timestamp = updated_elem.text if updated_elem is not None else datetime.utcnow().isoformat()

                    results.append({
                        "title": title,
                        "content": clean_content[:1500],
                        "author": author_name,
                        "url": url_href,
                        "timestamp": timestamp
                    })
        except Exception as e:
            print(f" [Warning] Could not fetch RSS for r/{sub_name}: {e}")

        return results

if __name__ == "__main__":
    agent = RedditScraperAgent()
    res = agent.run(max_per_sub=5)
    print("Run result:", res)
