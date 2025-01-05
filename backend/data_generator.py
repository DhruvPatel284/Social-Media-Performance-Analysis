import random
from datetime import datetime, timedelta
import pandas as pd
from settings import settings

class MockDataGenerator:
    @staticmethod
    def generate_mock_data(num_posts=settings.DEFAULT_NUM_POSTS):
        data = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(num_posts):
            post_type = random.choice(settings.POST_TYPES)
            base_rates = settings.ENGAGEMENT_RATES[post_type]
            
            post = {
                'post_id': f"post_{i}",
                'post_type': post_type,
                'posted_date': (base_date + timedelta(days=random.randint(0, 30))),
                'likes': int(random.gauss(base_rates['likes'], base_rates['likes']*0.2)),
                'views': int(random.gauss(base_rates['views'], base_rates['views']*0.2)),
                'comments': int(random.gauss(base_rates['comments'], base_rates['comments']*0.2)),
                'shares': int(random.gauss(base_rates['comments']/2, base_rates['comments']*0.1))
            }
            
            # Ensure no negative values
            for key in ['likes', 'views', 'comments', 'shares']:
                post[key] = max(0, post[key])
                
            data.append(post)
        
        return pd.DataFrame(data)

    @staticmethod
    def save_to_csv(df, filename='mock_data.csv'):
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")