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
