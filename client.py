
from local import LOCAL_CREDENTIALS
from funcs import getSize
from uuid import getnode as get_mac
import socket
import psutil
import json
import time

def tryConnect(server, count):
    try:
        client.connect(server)
        count += 1
    except ConnectionRefusedError:
        if count == 5:
            print("TIME OUT...")
            quit()
        print("CONNECTION REFUSED OR BUSY")
        print("Waiting 5 seconds...")
        time.sleep(5)
        tryConnect(server, count)
 
server = (LOCAL_CREDENTIALS["SERVER"], LOCAL_CREDENTIALS["PORT"])
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

count = 0
tryConnect(server, count)
print("CONNECTION ESTABLISHED")

host = socket.gethostname()
partitions = psutil.disk_partitions()
client.send(bytes(host, 'UTF-8'))

info = {
    "Computer": '',
    "Drive": '', 
    "Total Space": '',
    "Total Used": '',
    "Total Free": '', 
    "Year": '',
    "Month": '',
    "Day": '',
    "Time": '',
    "MAC": '' 
    }

info["Computer"] = host
updateTime = time.localtime()
info["Month"] = updateTime[1]
info["Day"] = updateTime[2]
info["Time"] = f'{updateTime[3]}:{updateTime[4]}:{updateTime[5]}'
info["Year"] = updateTime[0]

macTest = hex(get_mac()) if hex(get_mac()) == hex(get_mac()) else 0xDEADDEADBEEF
info["MAC"] = macTest.replace('0x', '')

for p in partitions:
    if (p.device != 'C:\\'):
        continue
    else:
        info["Drive"] = p.device
    try:
        usage = psutil.disk_usage(p.mountpoint)
        info["Total Space"] = getSize(usage.total)
        info["Total Used"] = getSize(usage.used)
        info["Total Free"] = getSize(usage.free)
    except PermissionError:
        continue
serial = json.dumps(info)

inData =  client.recv(2048)
print("From Server : ", inData.decode())

while True:
    outData = serial
    client.send(bytes(outData,'UTF-8'))

    inData =  client.recv(2048)
    print("From Server : ", inData.decode())
    
    outData = 'DONE'
    client.send(bytes(outData,'UTF-8'))

    inData =  client.recv(2048)
    print("From Server : ", inData.decode())
    break
client.close()