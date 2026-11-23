import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def cv_to_json_convert(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop =True,inplace =True)
            data_json = list(json.loads((data.T.to_json())).values())
            return data_json
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    
    def push_data_mongo(self,records,database,collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection

            self.mongoclient = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongoclient[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    file_path = "Network_Data\phisingData.csv" 
    database= "gsaran76"
    collection="NetworkSecurityData"
    networkobj = NetworkDataExtract()

    data_json = networkobj.cv_to_json_convert(file_path= file_path)
    print(data_json)
    no_of_records = networkobj.push_data_mongo(records = data_json,database =database,collection =collection)
    print(no_of_records)

