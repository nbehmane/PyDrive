from pymongo import MongoClient

def sendToDataBase(data):
    client = MongoClient()
    db = client.computers
    col = db["computers"]

    query = {"Computer": data["Computer"]}
    found = col.find(query)
    if found.count() == 0:
        print("Computer Added")
        col.insert_one(data)
    else:
        print("Computer Updated")
        col.update_one(data)

    client.close()