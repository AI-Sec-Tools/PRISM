"""
Database Manager for PRISM
SQLite-based vulnerability storage system.
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="data/prism.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.initialize_schema()
    
    def initialize_schema(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    severity TEXT,
                    cvss_score REAL,
                    published_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            self.logger.info("Database schema initialized")
    
    def store_vulnerability(self, vuln_data):
        """Store vulnerability in database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO vulnerabilities 
                (id, title, severity, cvss_score, published_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                vuln_data.get('id'),
                vuln_data.get('title', ''),
                vuln_data.get('severity', 'medium'),
                vuln_data.get('cvss_score', 0.0),
                vuln_data.get('published_date', datetime.now().isoformat())
            ))
            conn.commit()

# Enhanced Database Operations
    async def get_risk_trends(self, days: int = 30):
        """Get risk score trends over time."""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT date(created_at) as date, 
                       AVG(cvss_score) as avg_score,
                       COUNT(*) as count
                FROM vulnerabilities 
                WHERE created_at >= ?
                GROUP BY date(created_at)
                ORDER BY date
            """, (cutoff_date,))
            
            trends = cursor.fetchall()
            return [{'date': t[0], 'avg_score': t[1], 'count': t[2]} for t in trends]
    
    def get_vulnerability_stats(self):
        """Get comprehensive vulnerability statistics."""
        with sqlite3.connect(self.db_path) as conn:
            # Total vulnerabilities
            total = conn.execute("SELECT COUNT(*) FROM vulnerabilities").fetchone()[0]
            
            # By severity
            severity_stats = {}
            cursor = conn.execute("SELECT severity, COUNT(*) FROM vulnerabilities GROUP BY severity")
            for row in cursor:
                severity_stats[row[0]] = row[1]
            
            return {
                'total': total,
                'by_severity': severity_stats,
                'last_updated': datetime.now().isoformat()
            }
