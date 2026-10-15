"""
Dataset & Persistence Manager for MexConsumerPulse.
Manages SQLite storage, deduplication, schema migrations, and CSV/JSON automated exports.
"""

import sqlite3
import json
import csv
from datetime import datetime
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DB_PATH, EXPORTS_DIR

class DatasetManager:
    """
    Manages the persistent database for raw posts, classified consumer problems,
    daily reports, and analytical metrics.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Consumer Problems Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consumer_problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_hash TEXT UNIQUE,
                    title TEXT NOT NULL,
                    content TEXT,
                    source_platform TEXT NOT NULL,
                    source_url TEXT,
                    city TEXT NOT NULL,
                    colonia TEXT,
                    category TEXT NOT NULL,
                    confidence REAL,
                    audience TEXT NOT NULL,
                    urgency INTEGER NOT NULL,
                    sentiment TEXT,
                    matched_slang TEXT,
                    problem_summary TEXT,
                    solution_found TEXT,
                    venture_concept TEXT,
                    solution_summary TEXT,
                    timestamp TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 2. Daily Intelligence Reports Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_date TEXT UNIQUE,
                    report_title TEXT,
                    executive_summary TEXT,
                    markdown_content TEXT,
                    metrics_json TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 3. Agent Execution Run Logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    records_collected INTEGER,
                    records_inserted INTEGER,
                    details TEXT,
                    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def insert_problem(self, problem: Dict[str, Any]) -> bool:
        """
        Insert a analyzed consumer problem, preventing duplicate entries.
        """
        import hashlib
        raw_sig = f"{problem.get('source_url', '')}_{problem.get('title', '')[:50]}"
        content_hash = hashlib.sha256(raw_sig.encode('utf-8')).hexdigest()

        market_opp = problem.get("market_opportunity", {})
        venture_concept = market_opp.get("venture_concept", "")
        solution_summary = market_opp.get("solution_summary", "")

        matched_slang_json = json.dumps(problem.get("matched_slang", []), ensure_ascii=False)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO consumer_problems (
                        content_hash, title, content, source_platform, source_url,
                        city, colonia, category, confidence, audience, urgency,
                        sentiment, matched_slang, problem_summary, solution_found,
                        venture_concept, solution_summary, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    content_hash,
                    problem.get("title", ""),
                    problem.get("content", ""),
                    problem.get("source_platform", "Unknown"),
                    problem.get("source_url", ""),
                    problem.get("city", "National"),
                    problem.get("colonia", "General"),
                    problem.get("category", "General"),
                    problem.get("confidence", 0.5),
                    problem.get("audience", "Both"),
                    problem.get("urgency", 3),
                    problem.get("sentiment", "Neutral"),
                    matched_slang_json,
                    problem.get("problem_summary", ""),
                    problem.get("solution_found", ""),
                    venture_concept,
                    solution_summary,
                    problem.get("timestamp") or datetime.utcnow().isoformat()
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Already exists
                return False

    def get_all_problems(self, limit: int = 500, city: Optional[str] = None, 
                         category: Optional[str] = None, audience: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM consumer_problems WHERE 1=1"
        params = []
        if city and city != "All":
            query += " AND city LIKE ?"
            params.append(f"%{city}%")
        if category and category != "All":
            query += " AND category = ?"
            params.append(category)
        if audience and audience != "All":
            query += " AND audience = ?"
            params.append(audience)
        
        query += " ORDER BY urgency DESC, created_at DESC LIMIT ?"
        params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_metrics(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM consumer_problems")
            total_count = cursor.fetchone()[0]

            cursor.execute("SELECT category, COUNT(*) as count FROM consumer_problems GROUP BY category ORDER BY count DESC")
            cat_rows = cursor.fetchall()
            by_category = {r["category"]: r["count"] for r in cat_rows}

            cursor.execute("SELECT city, COUNT(*) as count FROM consumer_problems GROUP BY city ORDER BY count DESC")
            city_rows = cursor.fetchall()
            by_city = {r["city"]: r["count"] for r in city_rows}

            cursor.execute("SELECT audience, COUNT(*) as count FROM consumer_problems GROUP BY audience")
            aud_rows = cursor.fetchall()
            by_audience = {r["audience"]: r["count"] for r in aud_rows}

            cursor.execute("SELECT AVG(urgency) FROM consumer_problems")
            avg_urgency = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT COUNT(*) FROM consumer_problems WHERE urgency >= 4")
            urgent_count = cursor.fetchone()[0]

            return {
                "total_problems": total_count,
                "urgent_problems_count": urgent_count,
                "average_urgency": round(avg_urgency, 2),
                "by_category": by_category,
                "by_city": by_city,
                "by_audience": by_audience
            }

    def save_daily_report(self, report_date: str, title: str, summary: str, markdown: str, metrics: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO daily_reports (report_date, report_title, executive_summary, markdown_content, metrics_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(report_date) DO UPDATE SET
                    report_title=excluded.report_title,
                    executive_summary=excluded.executive_summary,
                    markdown_content=excluded.markdown_content,
                    metrics_json=excluded.metrics_json
            ''', (report_date, title, summary, markdown, json.dumps(metrics, ensure_ascii=False)))
            conn.commit()

    def get_latest_report(self) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_reports ORDER BY report_date DESC LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None

    def log_agent_run(self, agent_name: str, status: str, collected: int, inserted: int, details: str = ""):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO agent_runs (agent_name, status, records_collected, records_inserted, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (agent_name, status, collected, inserted, details))
            conn.commit()

    def export_dataset(self) -> Dict[str, str]:
        """
        Exports all current records to CSV and JSON in data/exports/
        """
        problems = self.get_all_problems(limit=5000)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        csv_filename = EXPORTS_DIR / f"mexico_consumer_problems_{timestamp}.csv"
        latest_csv = EXPORTS_DIR / "mexico_consumer_problems_latest.csv"
        json_filename = EXPORTS_DIR / f"mexico_consumer_problems_{timestamp}.json"
        latest_json = EXPORTS_DIR / "mexico_consumer_problems_latest.json"

        if problems:
            keys = problems[0].keys()
            for out_csv in [csv_filename, latest_csv]:
                with open(out_csv, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(problems)

        for out_json in [json_filename, latest_json]:
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(problems, f, ensure_ascii=False, indent=2)

        return {
            "csv_path": str(latest_csv),
            "json_path": str(latest_json),
            "total_exported": len(problems)
        }
