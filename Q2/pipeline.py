import datetime
from pymongo import MongoClient

class MongoDBPipeline:
    def open_spider(self,spider):
        db_uri = spider.settings.get('MONGODB_URI','mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'rent591_scrapy')
        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]
    
    def process_item(self, item, spider):
        self.insert_article(item)
        return item

    def insert_article(self, item):
        item = dict(item)
        self.db.article.insert_one(item)
    
    def close_spider(self, spider):
        self.db_client.close()
