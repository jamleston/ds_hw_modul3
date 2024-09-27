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
    if result:
        return result
    else:
        answer = 'No cat with this id, check it twice'
        return answer

# res = showCatById('66f4022d81b181920b27d926')
# print(res)

# 
# update
# 

def updateAge(name, age):
    new_name = name.lower()
    cat = db.cats.find_one({"name": new_name})
    if cat:
        db.cats.update_one({"name": new_name}, {"$set": {"age": age}})
        result = db.cats.find_one({"name": new_name})
        return result
    else:
        answer = f'We dont have cat named {name}, try another'
        return answer

# res = updateAge('Barsik', 10000000)
# print(res)

def addNewFeature(name, feature):
    new_name = name.lower()
    cat = db.cats.find_one({"name": new_name})
    if cat:
        db.cats.update_one({'name': new_name}, {'$addToSet': {'features': feature}})
        result = db.cats.find_one({"name": new_name})
        return result
    else:
        answer = f'We dont have cat named {name}, try another'
        return answer

# res = addNewFeature('arsik', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
# print(res)

# 
# delete
# 

def deleteByName(name):
    new_name = name.lower()
    cat = db.cats.find_one({"name": new_name})
    if cat:
        db.cats.delete_one({"name": new_name})
        result = db.cats.find_one({"name": new_name})
        return result
    else:
        answer = f'We dont have cat named {name}, try another'
        return answer

# res = deleteByName('Barsik')
# print(res)

def deleteAll():
    db.cats.deleteMany({})
    result = db.cats.find({})
    return result

# res = deleteAll()
# print(res)