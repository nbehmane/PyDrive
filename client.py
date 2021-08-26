import socket
import psutil
import json
import time
from local import LOCAL_CREDENTIALS
from funcs import get_size

count = 0
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
 
SERVER = LOCAL_CREDENTIALS["SERVER"]
PORT = LOCAL_CREDENTIALS["PORT"]
server = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tryConnect(server)
print("CONNECTION ESTABLISHED")

host = socket.gethostname()
partitions = psutil.disk_partitions()
client.send(bytes(host, 'UTF-8'))

info = {
    "Computer": '',
    "Drive": '', 
    "Usage": '', 
    "Month": '',
    "Day": '',
    "Time": '',
    "Year": ''
    }

info["Computer"] = host
updateTime = time.ctime().split(' ')
info["Month"] = updateTime[1]
info["Day"] = updateTime[3]
info["Time"] = updateTime[4]
info["Year"] = updateTime[5]

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