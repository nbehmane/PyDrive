import socket
import psutil
import json

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
 
SERVER = "129.65.134.233"
PORT = 2457
server = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
host = socket.gethostname()
partitions = psutil.disk_partitions()
client.send(bytes(host, 'UTF-8'))

info = {"Drive": '', "Usage": ''}


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