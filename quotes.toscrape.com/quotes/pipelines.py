# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from itemadapter import ItemAdapter
from quotes.settings import PG_DATABASE

class QuotesPipeline:
    def process_item(self, item, spider):
        return item

class SaveToPostgresPipeline:
    # Define function to configure the connection to the database & connect to it
    def __init__(self):
        self.connection = psycopg2.connect(**PG_DATABASE['default'])

        # Create cursor to execute commands
        self.cur = self.connection.cursor()

        # Create books table if not exist
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS quotes(
                id SERIAL PRIMARY KEY,
                text TEXT,
                author VARCHAR(100),
                tags TEXT[]
            )
        ''')

    def process_item(self, item, spider):
        # Change python list into postgresql array in tags
        tags = item['tags']
        tags = str(map(str, tags))
        tags = tags.replace('[', '{').replace(']', '}').replace('\'', '\"')
        print(tags)

        # Define insert statement
        self.cur.execute('''
            INSERT INTO books(
                text,
                author,
                tags
            ) VALUES(
                %s,
                %s,
                %s
            )
        ''', (
            item['text'],
            item['author'],
            item['tags']
        ))

        # Commit the insert statement
        self.connection.commit()
        return item
        
    
    # Define function to disconnect from database
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()