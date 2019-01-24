
import time
import os
import json
import struct
import socket
from pymongo import MongoClient

print ("Server is starting" ) 
#socket using udp
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0',8003))    

print ("Server is listenting port 8003")
#counting
i = 0
count_l=0
count_r=0
#database
conn = MongoClient()
db = conn.finalproject
left_set = db.left
right_set = db.right 
both_set = db.both 
### type list
type_list = ('forefoot','heel','under_pron','over_pron','normalstanding','left_bias','right_bias')

def leftinsert(db_set,type,data):
   # min_data = min(data)
    #data = [i - min_data for i in data]## process the data by minus the minimum

    db_set.insert({"type":type,"data":data})
def rightinsert(db_set,type,data):
    #min_data = min(data)
    #data = [i - min_data for i in data]
    db_set.insert({"type":type,"data":data})

def bothinsert(db_set,type,data_l,data_r):
    #min_l = min(data_l)
    #min_r = min(data_r)
    #data_l = [i-min_l for i in data_l]
    #data_r = [i-min_r for i in data_r]
    data = data_l + data_r
    print(data)
    db_set.insert({"type":type,"data":data})
type_index = input('enter the type number:')
type_index = int(type_index)
type_decided = type_list[type_index]
print(type_decided)
leftdata = None
rightdata = None
while True:
    data, addr = sock.recvfrom(1024)
    received = json.loads(data) 
    if received['sign'] == 'l':
        leftdata = received['data']
        count_l += 1
        print('count left',count_l)
    if received['sign'] == 'r':
        rightdata = received['data']
        count_r += 1
        print('count right:',count_r)
    if leftdata and rightdata:
        print('count:',i)
        bothinsert(both_set,type_decided,leftdata,rightdata)
    i+= 1 
sock.close()

