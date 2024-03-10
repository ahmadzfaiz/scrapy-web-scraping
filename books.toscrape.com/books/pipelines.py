# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from itemadapter import ItemAdapter
from books.items import BooksItem
from books.settings import PG_DATABASE

class CleanBooksPipeline:
    def process_item(self, item, spider):
        # Clean data if the item is BooksItem
        if isinstance(item, BooksItem):
            adapter = ItemAdapter(item)
            
            # Price --> convert to float
            value = adapter.get('price')
            value = value.replace('£', '')
            adapter['price'] = float(value)

            # Rating --> convert to integer
            value = adapter.get('rating')
            if 'One' in value:
                adapter['rating'] = 1
            elif 'Two' in value:
                adapter['rating'] = 2
            elif 'Three' in value:
                adapter['rating'] = 3
            elif 'Four' in value:
                adapter['rating'] = 4
            elif 'Five' in value:
                adapter['rating'] = 5
            else:
                adapter['rating'] = 0

            return item
        
        # If it doesn't meet the conditions above, then run this 
        else:
            return item

class SaveToPostgresPipeline:
    # Define function to configure the connection to the database & connect to it
    def __init__(self):
        self.connection = psycopg2.connect(**PG_DATABASE['default'])

        # Create cursor to execute commands
        self.cur = self.connection.cursor()

        # Create books table if not exist
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books(
                id SERIAL PRIMARY KEY,
                title TEXT,
                price DECIMAL,
                rating INTEGER
            )
        ''')

    def process_item(self, item, spider):
        # # Clean data if the item is BooksItem
        if isinstance(item, BooksItem):
            # Define insert statement
            self.cur.execute('''
                INSERT INTO books(
                    title,
                    price,
                    rating
                ) VALUES(
                    %s,
                    %s,
                    %s
                )
            ''', (
                item['title'],
                item['price'],
                item['rating']
            ))

            # Commit the insert statement
            self.connection.commit()
            return item
        
        # If it doesn't meet the conditions above, then run this 
        else:
            return item
    
    # Define function to disconnect from database
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()