from openai import OpenAI
from settings import settings
import json

class EngagementAnalyzer:
    def __init__(self, astra_client):
        self.astra_client = astra_client
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
    def analyze_engagement(self, post_type=None):
        """Analyze engagement metrics and generate insights"""
        try:
            # Get metrics from database
            metrics = self.astra_client.get_engagement_metrics(post_type)
            print("Debug - Raw metrics from DB:", metrics)  # Debug print
            
            if not metrics:
                print("Warning: No metrics returned from database")
                return {'metrics': [], 'insights': "No data available for analysis"}
            
            # Generate insights using GPT
            insights = self._generate_insights(metrics)
            
            return {
                'metrics': metrics,
                'insights': insights
            }
        except Exception as e:
            print(f"Error in analyze_engagement: {str(e)}")
            raise
    
    def _generate_insights(self, metrics):
        """Generate insights using GPT"""
        try:
            if not metrics:
                return "No data available for analysis"
                
            prompt = f"""
            Analyze the following social media engagement metrics and provide key insights:
            {json.dumps(metrics, indent=2)}
            
            Focus on:
            1. Comparative performance between post types
            2. Engagement patterns
            3. Recommendations for content strategy
            
            Format the response as bullet points with specific percentages and metrics.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",  
                messages=[
                    {"role": "system", "content": "You are a social media analytics expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return "Error generating insights"
            
    def calculate_comparative_metrics(self, metrics):
        """Calculate comparative metrics between post types"""
        try:
            results = {}
            
            # Convert metrics list to dictionary for easier comparison
            metrics_dict = {m['post_type']: m for m in metrics}
            
            for post_type1 in metrics_dict:
                for post_type2 in metrics_dict:
                    if post_type1 != post_type2:
                        comparison_key = f"{post_type1}_vs_{post_type2}"
                        results[comparison_key] = {
                            'likes_difference': (
                                (metrics_dict[post_type1]['avg_likes'] / metrics_dict[post_type2]['avg_likes'] - 1) * 100
                            ),
                            'engagement_ratio': (
                                (metrics_dict[post_type1]['avg_comments'] + metrics_dict[post_type1]['avg_shares']) /
                                (metrics_dict[post_type2]['avg_comments'] + metrics_dict[post_type2]['avg_shares'])
                            )
                        }
            
            return results
        except Exception as e:
            print(f"Error calculating comparative metrics: {str(e)}")
            return {}