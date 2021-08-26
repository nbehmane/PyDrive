import socket
import psutil
import json
import time
from local import LOCAL_CREDENTIALS
from funcs import get_size
from uuid import getnode as get_mac

info = {
    "Computer": '',
    "Drive": '', 
    "Usage": '', 
    "Year": '',
    "Month": '',
    "Day": '',
    "Time": '',
    "MAC": ''
    }

count = 0
SERVER = LOCAL_CREDENTIALS["SERVER"]
PORT = LOCAL_CREDENTIALS["PORT"]
server = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
 

tryConnect(server, count)
print("CONNECTION ESTABLISHED")

host = socket.gethostname()
partitions = psutil.disk_partitions()
client.send(bytes(host, 'UTF-8'))


info["Computer"] = host
updateTime = time.localtime()
info["Month"] = updateTime[1]
info["Day"] = updateTime[2]
info["Time"] = f'{updateTime[3]}:{updateTime[4]}:{updateTime[5]}'
info["Year"] = updateTime[0]

mac_test = hex(get_mac()) if hex(get_mac()) == hex(get_mac()) else 0xDEADDEAD
info["MAC"] = mac_test

for p in partitions:
    if (p.device != 'C:\\'):
        continue
    else:
        info["Drive"] = p.device
    try:
        usage = psutil.disk_usage(p.mountpoint)
        mes = get_size(usage.total)
        info["Usage"] = mes
    except PermissionError:
        continue
serial = json.dumps(info)

in_data =  client.recv(1024)
print("From Server : ", in_data.decode())

while True:
    out_data = serial
    client.send(bytes(out_data,'UTF-8'))

    in_data =  client.recv(1024)
    print("From Server : ", in_data.decode())
    
    out_data = 'DONE'
    client.send(bytes(out_data,'UTF-8'))

    in_data =  client.recv(1024)
    print("From Server : ", in_data.decode())
    break
client.close()