"""
Traditional SQLite Database Module
Demonstrates traditional relational database operations with exact text matching
"""
import sqlite3
import time
from typing import List, Dict, Any


class TraditionalDB:
    def __init__(self, db_path: str = "data/traditional.db"):
        self.db_path = db_path
        self.conn = None
        # Ensure data directory exists
        import os
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize the traditional SQLite database with schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster searches
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_name 
            ON products(name)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_category 
            ON products(category)
        """)
        
        self.conn.commit()
    
    def insert_product(self, name: str, description: str, category: str, price: float) -> int:
        """Insert a product into the database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, description, category, price)
            VALUES (?, ?, ?, ?)
        """, (name, description, category, price))
        self.conn.commit()
        return cursor.lastrowid
    
    def search_exact(self, query: str) -> tuple[List[Dict[str, Any]], float]:
        """
        Exact text search using SQL LIKE
        Returns: (results, execution_time)
        """
        start_time = time.time()
        cursor = self.conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT id, name, description, category, price
            FROM products
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY 
                CASE 
                    WHEN name LIKE ? THEN 1
                    WHEN category LIKE ? THEN 2
                    ELSE 3
                END
            LIMIT 20
        """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        
        results = [dict(row) for row in cursor.fetchall()]
        execution_time = time.time() - start_time
        
        return results, execution_time
    
    def get_all_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all products"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, description, category, price
            FROM products
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM products")
        total_products = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(DISTINCT category) as count FROM products")
        total_categories = cursor.fetchone()['count']
        
        cursor.execute("SELECT AVG(price) as avg_price FROM products")
        avg_price = cursor.fetchone()['avg_price'] or 0
        
        return {
            'total_products': total_products,
            'total_categories': total_categories,
            'avg_price': round(avg_price, 2),
            'db_type': 'Traditional SQL'
        }
    
    def clear_all(self):
        """Clear all products"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products")
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Made with Bob
