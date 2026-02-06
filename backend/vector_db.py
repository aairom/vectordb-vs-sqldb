"""
Vector Database Module using sqlite-vec
Demonstrates semantic search capabilities using vector embeddings
"""
import sqlite_vec
import time
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

import sqlite3


class VectorDB:
    def __init__(self, db_path: str = "data/vector.db"):
        self.db_path = db_path
        self.conn = None
        # Ensure data directory exists
        import os
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional embeddings
        self.embedding_dim = 384
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize the vector database with schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # Try to load sqlite-vec extension (optional)
        # If it fails, we'll use numpy-based similarity which works fine
        try:
            if hasattr(self.conn, 'enable_load_extension'):
                self.conn.enable_load_extension(True)
                sqlite_vec.load(self.conn)
                self.conn.enable_load_extension(False)
                print("[INFO] sqlite-vec extension loaded successfully")
            else:
                print("[INFO] Using numpy-based similarity search (extension loading not available)")
        except Exception as e:
            print(f"[INFO] Using numpy-based similarity search: {e}")
        
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
        
        # Create embeddings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                product_id INTEGER PRIMARY KEY,
                embedding BLOB NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        
        self.conn.commit()
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding vector for text"""
        return self.model.encode(text, convert_to_numpy=True)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return float(dot_product / (norm1 * norm2))
    
    def insert_product(self, name: str, description: str, category: str, price: float) -> int:
        """Insert a product and its embedding into the database"""
        cursor = self.conn.cursor()
        
        # Insert product
        cursor.execute("""
            INSERT INTO products (name, description, category, price)
            VALUES (?, ?, ?, ?)
        """, (name, description, category, price))
        product_id = cursor.lastrowid
        
        # Generate and store embedding
        combined_text = f"{name} {description} {category}"
        embedding = self._generate_embedding(combined_text)
        embedding_blob = embedding.tobytes()
        
        cursor.execute("""
            INSERT INTO embeddings (product_id, embedding)
            VALUES (?, ?)
        """, (product_id, embedding_blob))
        
        self.conn.commit()
        return product_id
    
    def search_semantic(self, query: str, limit: int = 20) -> tuple[List[Dict[str, Any]], float]:
        """
        Semantic search using vector similarity
        Returns: (results, execution_time)
        """
        start_time = time.time()
        
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        cursor = self.conn.cursor()
        
        # Get all products with embeddings
        cursor.execute("""
            SELECT p.id, p.name, p.description, p.category, p.price, e.embedding
            FROM products p
            JOIN embeddings e ON p.id = e.product_id
        """)
        
        results = []
        for row in cursor.fetchall():
            # Convert blob back to numpy array
            stored_embedding = np.frombuffer(row['embedding'], dtype=np.float32)
            
            # Calculate similarity
            similarity = self._cosine_similarity(query_embedding, stored_embedding)
            
            results.append({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'category': row['category'],
                'price': row['price'],
                'similarity': round(similarity, 4)
            })
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        results = results[:limit]
        
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
        
        cursor.execute("SELECT COUNT(*) as count FROM embeddings")
        total_embeddings = cursor.fetchone()['count']
        
        return {
            'total_products': total_products,
            'total_categories': total_categories,
            'avg_price': round(avg_price, 2),
            'total_embeddings': total_embeddings,
            'embedding_dimension': self.embedding_dim,
            'db_type': 'Vector Database'
        }
    
    def clear_all(self):
        """Clear all products and embeddings"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM embeddings")
        cursor.execute("DELETE FROM products")
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Made with Bob
