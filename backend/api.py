from flask import Flask, jsonify
from flask_cors import CORS
from astra_client import AstraClient
from engagement_analyzer import EngagementAnalyzer
from data_generator import MockDataGenerator
from settings import settings
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/initialize', methods=['POST'])
def initialize_data():
    """Initialize the database with mock data"""
    try:
        # Initialize database client
        db_client = AstraClient()
        db_client.connect(create_table=True)  # Only create table during initialization
        
        # Generate and store mock data
        data_generator = MockDataGenerator()
        df = data_generator.generate_mock_data()
        db_client.store_data(df)
        
        return jsonify({'message': 'Data initialized successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_client' in locals():
            db_client.close()

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data"""
    try:
        # Initialize database client
        db_client = AstraClient()
        db_client.connect(create_table=False)  # Don't recreate table
        
        # Get analytics
        analyzer = EngagementAnalyzer(db_client)
        analysis = analyzer.analyze_engagement()
        
        # Debug prints
        print("Debug - Raw metrics from DB:", analysis['metrics'])
        print("Debug - Metrics type:", type(analysis['metrics']))
        print("Debug - Metrics length:", len(analysis['metrics']))
        
        if not analysis['metrics']:
            return jsonify({
                'error': 'No metrics data available',
                'metrics': [],
                'insights': 'No data available for analysis'
            }), 404
            
        return jsonify({
            'metrics': analysis['metrics'],
            'insights': analysis['insights']
        })
    
    except Exception as e:
        print(f"API Error: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db_client' in locals():
            db_client.close()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)