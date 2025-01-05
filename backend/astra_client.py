from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.protocol import InvalidRequest
from settings import settings
import pandas as pd
from collections import defaultdict

class AstraClient:
    def __init__(self):
        self.session = None
        self.cluster = None
        
    def connect(self, create_table=False):
        """Connect to DataStax Astra DB and setup database"""
        try:
            print("Attempting to connect to Astra DB...")
            cloud_config = {
                'secure_connect_bundle': settings.ASTRA_DB_BUNDLE_PATH
            }
            
            auth_provider = PlainTextAuthProvider('token', settings.ASTRA_DB_TOKEN)
            
            self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = self.cluster.connect()
            print("Connected to cluster successfully")
            
            # Set the keyspace
            self.session.set_keyspace(settings.KEYSPACE_NAME)
            print(f"Set keyspace to: {settings.KEYSPACE_NAME}")
            print("now going in analayzer")
            if create_table:
                # Drop existing table if it exists
                self.session.execute(f"DROP TABLE IF EXISTS {settings.TABLE_NAME}")
                print(f"Dropped existing table {settings.TABLE_NAME}")
                
                # Create table with updated schema
                self._create_table()
                print("Table created successfully")
            else : print("not require to create table")
        except Exception as e:
            print(f"Detailed connection error: {str(e)}")
            raise Exception(f"Database connection error: {str(e)}")
        
    def _create_table(self):
        """Create the table with post_type as part of the primary key"""
        try:
            self.session.execute(f"""
                CREATE TABLE IF NOT EXISTS {settings.TABLE_NAME} (
                    post_type text,
                    post_id text,
                    posted_date timestamp,
                    likes int,
                    views int,
                    comments int,
                    shares int,
                    PRIMARY KEY (post_type, post_id)
                )
            """)
            
            # Verify table exists
            verify_query = f"SELECT * FROM {settings.TABLE_NAME} LIMIT 1"
            self.session.execute(verify_query)
            print("Table verified successfully")
        except Exception as e:
            print(f"Detailed table creation error: {str(e)}")
            raise Exception(f"Failed to create table: {str(e)}")
        
    def store_data(self, df):
        """Store DataFrame in Astra DB"""
        try:
            print(f"Attempting to store {len(df)} records")
            insert_statement = self.session.prepare(f"""
                INSERT INTO {settings.TABLE_NAME}
                (post_type, post_id, posted_date, likes, views, comments, shares)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """)
            
            for _, row in df.iterrows():
                print(f"Inserting record for post_id: {row['post_id']}")
                self.session.execute(insert_statement, (
                    row['post_type'],
                    row['post_id'],
                    row['posted_date'],
                    row['likes'],
                    row['views'],
                    row['comments'],
                    row['shares']
                ))
            print("All records stored successfully")
        except Exception as e:
            print(f"Detailed storage error: {str(e)}")
            raise Exception(f"Failed to store data: {str(e)}")
            
    def get_engagement_metrics(self, post_type=None):
            """Get engagement metrics for a specific post type or all post types"""
            try:
                print(f"Querying engagement metrics for post_type: {post_type}")
                if post_type:
                    query = f"""
                        SELECT post_type, likes, views, comments, shares
                        FROM {settings.TABLE_NAME}
                        WHERE post_type = %s
                    """
                    rows = self.session.execute(query, [post_type])
                else:
                    query = f"""
                        SELECT post_type, likes, views, comments, shares
                        FROM {settings.TABLE_NAME}
                    """
                    rows = self.session.execute(query)
                    print(f"Executed query: {query}")
                
                # Calculate averages in Python since we can't use GROUP BY
                metrics = defaultdict(lambda: {'likes': [], 'views': [], 'comments': [], 'shares': []})
                
                # Collect all metrics by post_type
                row_count = 0
                for row in rows:
                    row_count += 1
                    metrics[row.post_type]['likes'].append(row.likes)
                    metrics[row.post_type]['views'].append(row.views)
                    metrics[row.post_type]['comments'].append(row.comments)
                    metrics[row.post_type]['shares'].append(row.shares)
                
                print(f"Retrieved {row_count} rows from database")
                
                # Calculate averages
                result = []
                for post_type, values in metrics.items():
                    result.append({
                        'post_type': post_type,
                        'avg_likes': sum(values['likes']) / len(values['likes']) if values['likes'] else 0,
                        'avg_views': sum(values['views']) / len(values['views']) if values['views'] else 0,
                        'avg_comments': sum(values['comments']) / len(values['comments']) if values['comments'] else 0,
                        'avg_shares': sum(values['shares']) / len(values['shares']) if values['shares'] else 0
                    })
                
                print(f"Calculated metrics for {len(result)} post types")
                return result
                    
            except Exception as e:
                print(f"Error in get_engagement_metrics: {str(e)}")
                raise Exception(f"Failed to get engagement metrics: {str(e)}")
    
    def close(self):
        """Close the database connection"""
        if self.cluster:
            self.cluster.shutdown()