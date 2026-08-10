"""
NIKKI Master SQLite Local Database Initializer.
Stores 4-tier memories, indexed knowledge document embeddings, and audit logs locally on disk.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
import sqlite3
from pathlib import Path

class NikkiDatabase:
    def __init__(self, db_path: str = "data/nikki.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Memories Table (Short-term, Long-term, Episodic, Semantic)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    tier TEXT NOT NULL,
                    key TEXT,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Knowledge Documents Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    content_hash TEXT,
                    chunks_count INTEGER DEFAULT 0,
                    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Vector Embeddings Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vector_embeddings (
                    id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    chunk_text TEXT NOT NULL,
                    vector_json TEXT,
                    FOREIGN KEY (doc_id) REFERENCES knowledge_documents(id)
                )
            """)

            # Security Audit Logs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_audit_logs (
                    id TEXT PRIMARY KEY,
                    action TEXT NOT NULL,
                    permission_level INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

if __name__ == "__main__":
    db = NikkiDatabase()
    print("✅ Nikki Master SQLite Database Initialized at data/nikki.db!")
