import threading
import time
import sqlite3
import paho.mqtt.client as mqtt
import requests
import socket
import queue
import json
import subprocess
import .node
import .cloud
import .database
import paho.mqtt.client as mqtt
from cloud import *
from datetime import datetime




def db_reader(db):
    
    while True:
    
        try:
            data=getdata('Device')
            ID=data[0][1]
            NAME=data[0][2]
            data=getdata('Cloud')
            PROTOCOL=data[0][1]
            HOST=data[0][3]
            PORT=data[0][4]
            data=getdata('Gateway')
            N_STATUS=data[0][1]
            C_STATUS=data[0][2]
            I_STATUS=data[0][3]
        except:
            time.sleep(5)

        
        time.sleep(10)
        db.set()
    
def ledreq(led)
    while True:
        if not req.empty() and SCAN_STATUS=='Active'
            r=req.get()
            node.writeLED(r['MAC'],r['SERVICE'],r['CHAR'],r['CONFIG'])
        
    
def LEDconfig(mac,service,char,config):
    request={'MAC':mac,'SERVICE':service,'CHAR':char,'CONFIG':config}
    req.put(request,block=True,timeout=2)
    

def node(db)
    FLG=db.wait()
    print("NODE STARTED")
    global BT_STATUS
    while True:
        payload=node.app_node
        if not q.full() and C_STATUS=='Active':
            q.put(payload,block=True,timeout=2)
        time.sleep(3)
        
        
def cloud(e_MQTT)
    print("Loaded MQTT configuration information.")
    print("Endpoint URL: " + mqtt_url)
    print("Root Cert: " + root_ca)
    print("Device Cert: " + public_crt)
    print("Private Key: " + private_key)
    
    # creating obejct of MQTT client
    client = mqtt.Client()
    
    # methods call
    funInitilise(client)
    subscribeClient(client)
   
    while True:
        now=datetime.now()  
            print(now)  
            dt = {'t_stmp' : int(datetime.timestamp(now)),
            't_utc' : now.strftime("%d/%m/%Y, %H:%M:%S"),
            'x' : "{:.3f}".format(random.uniform(-5,5)),
            'y' :"{:.3f}".format(random.uniform(-5,5)),
            'z' :"{:.3f}".format(random.uniform(-5,5)) 
        }

        # method call
        publishData(client, dt)
    
       

if __name__=='__main__':
    q=queue.Queue(100)
    req=queue.Queue(100)

    
    #DB VARIABLES
    ID=''
    NAME=''
    PROTOCOL=''
    HOST=''
    PORT=''
    N_STATUS=''
    C_STATUS=''
    BT_STATUS=''
    db = threading.Event()
    led = threading.Event()
    e_MQTT=threading.Event()
    t_db_reader = threading.Thread(name='db_read', target=db_reader,args=(db,))
    t_db_reader.start()
    t_led_thread = threading.Thread(name='led thread', target=ledreq,args=(led,))
    t_led_thread.start()
    t_cloud=threading.Thread(name='cloud', target=cloud,args=(e_MQTT,))
    t_cloud.start()
    t_node=threading.Thread(name='NODE', target=node,args=(db,))
    t_node.start()
    
    
    
    
    
    
    
    
    
    
    
    
def getdata(tableselect):
    try:
        data=conn.execute('select * from ' + tableselect)
        data=data.fetchall()   
        return data
        
    except:
        time.sleep(2)
        return getdata(tableselect)
