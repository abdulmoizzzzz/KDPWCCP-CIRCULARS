# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter

class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_empty = False  # Flag to track if collection is emptied

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def empty_collection(self, collection_name):
        self.db[collection_name].delete_many({})
        self.collection_empty = True

    def process_item(self, item, spider):
        
        if spider.name == 'kdpwcc_spider':  
            raw_collection = "rawdataOrganizedMarket"
            refined_collection = "RefineddataOrganizedMarket"
        elif spider.name == 'kdpwcc_spider2':  
            raw_collection = "rawdataOTC"
            refined_collection = "RefineddataOTC"
        else:
            raise ValueError(f"Unknown spider: {spider.name}")

      
        if not self.collection_empty:
            self.empty_collection(raw_collection)
            self.empty_collection(refined_collection)

      
        self.db[raw_collection].insert_one(ItemAdapter(item).asdict())
        self.db[refined_collection].insert_one(ItemAdapter(item).asdict())

        return item

