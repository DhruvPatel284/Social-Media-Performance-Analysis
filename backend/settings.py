import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # DataStax Astra DB Settings
    ASTRA_DB_BUNDLE_PATH = os.getenv('ASTRA_DB_BUNDLE_PATH')
    ASTRA_DB_TOKEN = os.getenv('ASTRA_DB_TOKEN')  # New token setting
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Database Settings
    KEYSPACE_NAME = "social_analytics"
    TABLE_NAME = "engagement_data"
    
    # Data Generation Settings
    DEFAULT_NUM_POSTS = 100
    POST_TYPES = ['carousel', 'reel', 'static']
    
    # Base Engagement Rates for Different Post Types
    ENGAGEMENT_RATES = {
        'carousel': {'likes': 50, 'views': 200, 'comments': 15},
        'reel': {'likes': 80, 'views': 500, 'comments': 25},
        'static': {'likes': 30, 'views': 100, 'comments': 10}
    }

settings = Settings()