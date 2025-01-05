from data_generator import MockDataGenerator
from astra_client import AstraClient
from engagement_analyzer import EngagementAnalyzer

def main():
    try:
        # Initialize database client
        print("Connecting to Astra DB...")
        db_client = AstraClient()
        db_client.connect()
        
        # Generate mock data
        print("Generating mock data...")
        data_generator = MockDataGenerator()
        df = data_generator.generate_mock_data()
        
        # Store data in Astra DB
        print("Storing data in Astra DB...")
        db_client.store_data(df)
        
        # Initialize analyzer
        analyzer = EngagementAnalyzer(db_client)
        
        # Analyze all post types
        print("\nAnalyzing engagement metrics...")
        analysis = analyzer.analyze_engagement()
        
        # Print results
        print("\nEngagement Metrics:")
        for metric in analysis['metrics']:
            print(f"\nPost Type: {metric['post_type']}")
            print(f"Average Likes: {metric['avg_likes']:.2f}")
            print(f"Average Views: {metric['avg_views']:.2f}")
            print(f"Average Comments: {metric['avg_comments']:.2f}")
            print(f"Average Shares: {metric['avg_shares']:.2f}")
        
        print("\nGPT-Generated Insights:")
        print(analysis['insights'])
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        if 'db_client' in locals():
            db_client.close()

if __name__ == "__main__":
    main()