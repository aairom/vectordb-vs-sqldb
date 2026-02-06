"""
Flask Backend API for Vector DB vs SQL DB Comparison
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from traditional_db import TraditionalDB
from vector_db import VectorDB
from sample_data import SAMPLE_PRODUCTS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Initialize databases
traditional_db = TraditionalDB()
vector_db = VectorDB()


@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})


@app.route('/api/initialize', methods=['POST'])
def initialize_databases():
    """Initialize both databases with sample data"""
    try:
        # Clear existing data
        traditional_db.clear_all()
        vector_db.clear_all()
        
        # Insert sample products
        for product in SAMPLE_PRODUCTS:
            traditional_db.insert_product(
                product['name'],
                product['description'],
                product['category'],
                product['price']
            )
            vector_db.insert_product(
                product['name'],
                product['description'],
                product['category'],
                product['price']
            )
        
        return jsonify({
            'success': True,
            'message': f'Initialized databases with {len(SAMPLE_PRODUCTS)} products'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search/traditional', methods=['POST'])
def search_traditional():
    """Search using traditional SQL database"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results, execution_time = traditional_db.search_exact(query)
        
        return jsonify({
            'results': results,
            'execution_time': round(execution_time * 1000, 2),  # Convert to ms
            'count': len(results),
            'db_type': 'traditional'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/vector', methods=['POST'])
def search_vector():
    """Search using vector database"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results, execution_time = vector_db.search_semantic(query)
        
        return jsonify({
            'results': results,
            'execution_time': round(execution_time * 1000, 2),  # Convert to ms
            'count': len(results),
            'db_type': 'vector'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/compare', methods=['POST'])
def search_compare():
    """Compare search results from both databases"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Search in both databases
        trad_results, trad_time = traditional_db.search_exact(query)
        vec_results, vec_time = vector_db.search_semantic(query)
        
        return jsonify({
            'traditional': {
                'results': trad_results,
                'execution_time': round(trad_time * 1000, 2),
                'count': len(trad_results)
            },
            'vector': {
                'results': vec_results,
                'execution_time': round(vec_time * 1000, 2),
                'count': len(vec_results)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics from both databases"""
    try:
        trad_stats = traditional_db.get_stats()
        vec_stats = vector_db.get_stats()
        
        return jsonify({
            'traditional': trad_stats,
            'vector': vec_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products from traditional database"""
    try:
        products = traditional_db.get_all_products(limit=100)
        return jsonify({'products': products, 'count': len(products)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_databases():
    """Clear all data from both databases"""
    try:
        traditional_db.clear_all()
        vector_db.clear_all()
        return jsonify({'success': True, 'message': 'Databases cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Display URLs prominently
    print("\n" + "="*70)
    print("🚀 VECTOR DB vs SQL DB COMPARISON APPLICATION")
    print("="*70)
    print()
    print("🌐 OPEN THIS URL IN YOUR BROWSER:")
    print("   ┌─────────────────────────────────────┐")
    print("   │  http://localhost:8080              │")
    print("   └─────────────────────────────────────┘")
    print()
    print("📡 API Endpoints:")
    print("   • http://localhost:8080/api/health")
    print("   • http://localhost:8080/api/initialize")
    print("   • http://localhost:8080/api/search/compare")
    print()
    print("📝 Instructions:")
    print("   1. Open http://localhost:8080 in your browser")
    print("   2. Click 'Initialize Databases' button")
    print("   3. Try example searches")
    print()
    print("🛑 Press CTRL+C to stop the server")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=True)

# Made with Bob
