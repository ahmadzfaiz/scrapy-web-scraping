# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re, psycopg2
import settings
from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip whitespaces from item
        field_names = list(adapter.field_names())
        field_names.remove('description')
        field_names.remove('price')
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value[0].strip()

        # Category and Product type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        regex_extract = re.findall('[0-9]+', availability_string)[0]
        if regex_extract == '':
            adapter['availability'] = 0
        else:
            adapter['availability'] = int(regex_extract)

        # Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        # Stars --> convert string to number
        star_string = adapter.get('stars')
        split_stars_array = star_string.split(' ')
        star_text_value = split_stars_array[1].lower()
        if star_text_value == 'zero':
            adapter['stars'] = 0
        elif star_text_value == 'one':
            adapter['stars'] = 1
        elif star_text_value == 'two':
            adapter['stars'] = 2
        elif star_text_value == 'three':
            adapter['stars'] = 3
        elif star_text_value == 'four':
            adapter['stars'] = 4
        elif star_text_value == 'five':
            adapter['stars'] = 5

        return item

class SaveToPostgresPipeline:
    # Define function to configure the connection to the database & connect to it
    def __init__(self):
        self.connection = psycopg2.connect(**settings.DATABASE['default'])
        
        # Create cursor to execute commands
        self.cur = self.connection.cursor()

        # Create books table if not exist
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books(
                id SERIAL PRIMARY KEY,
                url VARCHAR(255),
                title TEXT,
                product_type VARCHAR(255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                price DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                category VARCHAR(255),
                description TEXT
            )
        ''')

    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute('''
            INSERT INTO books(
                url,
                title,
                product_type,
                price_excl_tax,
                price_incl_tax,
                tax,
                price,
                availability,
                num_reviews,
                stars,
                category,
                description
            ) VALUES(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        ''', (
            item['url'],
            item['product_type'],
            item['title'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['tax'],
            item['price'],
            item['availability'],
            item['num_reviews'],
            item['stars'],
            item['category'],
            str(item['description'][0]),
        ))

        # Commit the insert statement
        self.connection.commit()
        return item

    # Define function to disconnect from database
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()