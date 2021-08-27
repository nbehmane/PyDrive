from pymongo import MongoClient
import openpyxl

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
        col.update_one({"Computer": data["Computer"]}, {"$set": data})

    client.close()

def deleteAllEntries():
    client = MongoClient()
    db = client.computers
    col = db["computers"]
    col.remove({})

def importComputerData():
    client = MongoClient()
    db = client.computers
    col = db["computers"]

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = "Computer"
    sheet['B1'] = "MAC"
    sheet['C1'] = "Drive"
    sheet['D1'] = "Total Space"
    sheet['E1'] = "Total Used"
    sheet['F1'] = "Total Free"
    sheet['G1'] = "Time Updated"
    sheet['H1'] = "Date Updated"

    computers = col.find({})
    count = 2
    for comp in computers:
        mac = comp["MAC"]
        sheet[f'A{count}'] = comp["Computer"]
        sheet[f'B{count}'] = f'{mac[0:2]}:{mac[2:4]}:{mac[4:6]}:{mac[6:8]}:{mac[8:10]}:{mac[10:12]}'
        sheet[f'C{count}'] = comp["Drive"]
        sheet[f'D{count}'] = comp["Total Space"]
        sheet[f'E{count}'] = comp["Total Used"]
        sheet[f'F{count}'] = comp["Total Free"]
        sheet[f'G{count}'] = comp["Time"]
        sheet[f'H{count}'] = f'{comp["Month"]}/{comp["Day"]}/{comp["Year"]}'

        count += 1
    wb.save(filename="comps.xlsx")

def main():
    importComputerData()

if __name__ == '__main__':
    main()