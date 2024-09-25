from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# connecting to compass

client = MongoClient(
    "mongodb+srv://user:12345@cluster0.mxpz2.mongodb.net/",
    server_api=ServerApi('1')
)

# creating database

db = client.book

# adding items

result_one = db.cats.insert_one(
    {
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"],
    }
)

result_many = db.cats.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]
)

# 
# read
# 

def showAll():
    obj = db.cats.find({})
    result = []
    for el in obj:
        result.append(el)
    return result

# res = showAll()
# print(res)

def showCatById(id):
    result = db.cats.find_one({"_id": ObjectId(id)})
    return result

# res = showCatById('66f4022d81b181920b27d926')
# print(res)

# 
# update
# 

def updateAge(name, age):
    db.cats.update_one({"name": name}, {"$set": {"age": age}})
    result = db.cats.find_one({"name": name})
    return result

# res = updateAge('barsik', 10000000)
# print(res)

def addNewFeature(name, feature):
    db.cats.update_one({'name': name}, {'$addToSet': {'features': feature}})
    result = db.cats.find_one({"name": name})
    return result

# res = addNewFeature('barsik', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
# print(res)

# 
# delete
# 

def deleteByName(name):
    db.cats.delete_one({"name": name})
    result = db.cats.find_one({"name": name})
    return result

# res = deleteByName('barsik')
# print(res)

def deleteAll():
    db.cats.deleteMany({})
    result = db.cats.find({})
    return result

# res = deleteAll()
# print(res)