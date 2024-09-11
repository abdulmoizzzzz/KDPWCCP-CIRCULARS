from flask import Flask, Response
from pymongo import MongoClient
import json  

app = Flask(__name__)


client = MongoClient("mongodb+srv://moiz121:test123456@cluster0.lq8grwq.mongodb.net/")
db = client.KDPWCCP
collection = db.RefineddataOrganizedMarket

@app.route('/')
def get_all_data():
    
    projection = {"_id": False}
    
    
    data = list(collection.find({}, projection))
   
    
    result = {
        "RefineddataOrganizedMarket": data
    }
    
    pretty_json = json.dumps(result, indent=2)
    
    return Response(pretty_json, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)  
