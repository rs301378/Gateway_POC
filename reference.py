import threading
import time
import sqlite3
import paho.mqtt.client as mqtt
import requests
import socket
import queue
import json
from bluepy.btle import Scanner
import subprocess


def db_reader(db):
    print('DB STARTED')
    conn = sqlite3.connect('/usr/share/apache2/default-site/htdocs/Gateway_Manager/Gateway_Manager/test.db')
    cur=conn.cursor()
    global ID
    global NAME
    global PROTOCOL
    global HOST
    global PORT
    global N_STATUS
    global C_STATUS
    global BT_STATUS
    while True:
        try:
            cur.execute("SELECT * FROM Device")
            dev_row=cur.fetchall()
            ID=dev_row[0][1]
            NAME=dev_row[0][2]
            cur.execute("SELECT * FROM Cloud")
            cld_row=cur.fetchall()
            PROTOCOL=cld_row[0][1]
            HOST=cld_row[0][3]
            PORT=cld_row[0][4]
            cur.execute("SELECT * FROM Gateway")
            gwy_row=cur.fetchall()
            N_STATUS=gwy_row[0][1]
            C_STATUS=gwy_row[0][2]
        except:
            time.sleep(5)
            conn.close()
            conn = sqlite3.connect('/usr/share/apache2/default-site/htdocs/Gateway_Manager/Gateway_Manager/test.db')
            cur=conn.cursor()
        
        time.sleep(10)
        db.set()
    conn.close()

def app_control(db):
    FLG=db.wait()
    print('APP STARTED')
    while FLG:
        if C_STATUS=='Active':
            if PROTOCOL=='MQTT':
                if e_HTTP.isSet() or e_SOCK.isSet():
                    e_HTTP.clear()
                    e_SOCK.clear()
                    e_CLOSE.wait()
                if not e_MQTT.isSet():
                    e_MQTT.set()
            elif PROTOCOL=='HTTP':
                if e_MQTT.isSet() or e_SOCK.isSet():
                    e_MQTT.clear()
                    e_SOCK.clear()
                    e_CLOSE.wait()
                if not e_HTTP.isSet():
                    e_HTTP.set()
            elif PROTOCOL=='WS':
                if e_MQTT.isSet() or e_MQTT.isSet():
                    e_MQTT.clear()
                    e_HTTP.clear()
                    e_CLOSE.wait()
                if not e_SOCK.isSet():
                    e_SOCK.set()
        elif C_STATUS=='Inactive':
            if e_HTTP.isSet() or e_SOCK.isSet()or e_MQTT.isSet():
                    e_HTTP.clear()
                    e_SOCK.clear()
                    e_MQTT.clear()
                    e_CLOSE.wait()         
        time.sleep(5)


def c_MQTT(e_MQTT):
    while True:
        flg_mqtt=e_MQTT.wait()
        print('MQTT STARTED')
        client = mqtt.Client("P1") 
        client.connect(HOST)
        data='IOT Gateway|ID:'+ID+'|NAME:'+NAME
        client.publish("Msg",data)
        data='NODE|DEVICE:Accelerometer|STATUS:'+N_STATUS
        client.publish("Msg",data)
        data='CLOUD|SERVER:MQTT Broker|STATUS:'+C_STATUS
        client.publish("Msg",data)
        data=''
        while e_MQTT.isSet():
            if not q.empty() and N_STATUS=='Active':
                #data='VAL:'+q.get()
                data=json.dumps(q.get())
                client.publish("Msg",data)
            elif N_STATUS=='Inactive':
                data='NODE|DEVICE:Accelerometer|STATUS:'+N_STATUS
                client.publish("Msg",data)
            time.sleep(5)
        data='CLOUD|SERVER:MQTT Broker|STATUS:'+C_STATUS
        client.publish("Msg",data)
        print('MQTT disconnecting')
        client.disconnect()
        e_CLOSE.set()

def c_HTTP(e_HTTP):
    while True:
        flg_HTTP=e_HTTP.wait()
        print('HTTP STARTED')
        url='http://'+HOST
        data='IOT Gateway|ID:'+ID+'|NAME:'+NAME
        payload = {'data':data}
        r = requests.post(url,data = payload)
        data='NODE|DEVICE:Accelerometer|STATUS:'+N_STATUS
        payload = {'data':data}
        r = requests.post(url,data = payload)
        data='CLOUD|SERVER:HTTP Server|STATUS:'+C_STATUS
        payload = {'data':data}
        r = requests.post(url,data = payload)
        data=''
        while e_HTTP.isSet():
            if not q.empty() and N_STATUS=='Active':
                data='VAL:'+q.get()
                payload = {'data':data}
                r = requests.post(url,data = payload)
            elif N_STATUS=='Inactive':
                data='NODE|DEVICE:Accelerometer|STATUS:'+N_STATUS
                payload = {'data':data}
                r = requests.post(url,data = payload)
            time.sleep(5)
        data='CLOUD|SERVER:HTTP Server|STATUS:'+C_STATUS
        payload = {'data':data}
        r = requests.post(url,data = payload)
        print('HTTP disconnecting')
        e_CLOSE.set()


def c_SOCK(e_SOCK):
    while True:
        flg_sock=e_SOCK.wait()
        print('SOCKET STARTED')
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, int(PORT)))
        data='IOT Gateway|ID:'+ID+'|NAME:'+NAME
        s.sendall(bytes(data,'utf-8'))
        time.sleep(0.25)
        data='NODE|DEVICE:Accelerometer|STATUS:'+N_STATUS
        s.sendall(bytes(data,'utf-8'))
        time.sleep(0.25)
        data='CLOUD|SERVER:Socket Server|STATUS:'+C_STATUS
        s.sendall(bytes(data,'utf-8'))
        data=''
        time.sleep(0.25)
        while e_SOCK.isSet():
            if not q.empty() and N_STATUS=='Active':
                data='VAL:'+q.get()
                s.sendall(bytes(data,'utf-8'))
            elif N_STATUS=='Inactive':
                data='NODE|DEVICE:Accelerometer|STATUS:'+N_STATUS
                s.sendall(bytes(data,'utf-8'))
            time.sleep(5)
        data='CLOUD|SERVER:Socket Server|STATUS:'+C_STATUS
        s.sendall(bytes(data,'utf-8'))
        print('SOCKET disconnecting')
        s.close()
        e_CLOSE.set()

def app_node(db):
    i=1000
    FLG=db.wait()
    print("NODE STARTED")
    global BT_STATUS
    while True:
        if N_STATUS=='Active':
            #Accelerometer Section
            with open("/sys/devices/virtual/misc/FreescaleAccelerometer/data","r") as VAL:
                r=str(VAL.readline())
            #BLE Section
            bt=subprocess.check_output(['hciconfig'])
            if b'UP' in bt:
                BT_STATUS='Active'
            else:
                BT_STATUS='Inactive'
            if BT_STATUS=='Active' and C_STATUS=='Active':
                lescan=Scanner(0)
                devices=lescan.scan(3)
                for dev in devices:
                    payload={'TYPE':'Beacon'}
                    payload.update({'MAC':dev.addr,'MAC TYPE':dev.addrType,'RSSI':dev.rssi})
                    for (adtype,desc,value) in dev.getScanData():
                        payload.update({desc:value})
                    if not q.full() and C_STATUS=='Active':
                        q.put(payload,block=True,timeout=2)
            elif not q.full() and C_STATUS=='Active' and BT_STATUS=='Inactive':
                q.put(r,block=True,timeout=2)
                #i=i+1
                #if i>9999:
                 #   i=1000
        time.sleep(3)


            

            
if __name__=='__main__':
    q=queue.Queue(18)
    #ACCELEROMETER ENABLED
    ENB=open("/sys/devices/virtual/misc/FreescaleAccelerometer/enable","w")
    ENB.write('1')
    ENB.close()
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
    e_MQTT=threading.Event()
    e_HTTP=threading.Event()
    e_SOCK=threading.Event()
    e_CLOSE=threading.Event()
    t_db_reader = threading.Thread(name='db_read', target=db_reader,args=(db,))
    t_db_reader.start()
    t_app_control = threading.Thread(name='app_ctrl', target=app_control,args=(db,))
    t_app_control.start()
    t_MQTT=threading.Thread(name='MQTT', target=c_MQTT,args=(e_MQTT,))
    t_MQTT.start()
    t_HTTP=threading.Thread(name='HTTP', target=c_HTTP,args=(e_HTTP,))
    t_HTTP.start()
    t_SOCK=threading.Thread(name='SOCKET', target=c_SOCK,args=(e_SOCK,))
    t_SOCK.start()
    t_node=threading.Thread(name='NODE', target=app_node,args=(db,))
    t_node.start()
