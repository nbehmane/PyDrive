from pymongo import MongoClient

def sendToDataBase(data):
    client = MongoClient()
    db = client.computers
    col = db["computers"]

    query = {"Computer": data["Computer"]}
    found = col.find(query)
    if found.count() == 0:
        col.insert_one(data)
    else:
        print("OBJECT EXISTS")

    client.close()


