import threading
import time
import sqlite3
import paho.mqtt.client as mqtt
import requests
import socket
import queue
import json
import subprocess
from cloud import *
from node import *
from database import p1 as db
from datetime import datetime

awstopic=""
pubflag=False

    
def parse(jobconfig,client):
    global pubflag
    global awstopic
       
    if 'execution' in jobconfig:
       
        jobid = jobconfig['execution']['jobId']
        cat = jobconfig['execution']['jobDocument']['category']
        operation = jobconfig['execution']['jobDocument']['operation']
        cmd=jobconfig['execution']['jobDocument'][cat]
        if cat=='cloud':

            value=cmd['value']
            task=cmd['task']
        #led_config=jobconfig['execution']['jobDocument']['led']
        
            if task=='publish_status' and value=='start':
                pubflag=True
                print("Publish Started")
            #db.updatetable('Cloud','C_Status','Active')
            elif task=='publish_status' and value=='stop':
                pubflag=False
                print("Publish Stopped")
            #db.updatetable('Cloud','C_Status','Inactive')
            
            if task=='publish_topic':
                awstopic=value
                print("Topic set",awstopic)
        
        #if cat=='node':
        #if op=='read':
         #   rr=node.readp(j['MAC'],j['SERVICE'],j['CHAR'],j['CONFIG'])
        #publish rr
    #if op=='write':
     #   node.writep(j['MAC'],j['SERVICE'],j['CHAR'],j['CONFIG'])  
        jobstatustopic = "$aws/things/Test_gateway/jobs/"+ jobid + "/update"
       
        #if operation=="publish" and cmd=="start":
        #    pubflag=True
        #elif operation=="publish" and cmd=="stop":
        #    pubflag=False
        #led config
        client.publish(jobstatustopic, json.dumps({ "status" : "SUCCEEDED"}),0) 
        
    
    
    
#if cat=='db':
    #table
    #start time and stop time
    #publish data

#if cat=='gateway':
    #variable scantime
        
    

def job(client,obj,msg):

    # This callback will only be called for messages with topics that match
    # $aws/things/Test_gateway/jobs/notify-next

    jobconfig = json.loads(msg.payload.decode('utf-8'))
    t_job = threading.Thread(name='parse', target=parse,args=(jobconfig,client,))
    t_job.start()
    
    
     

def db_reader(dbEvent):
    print('db thread started')
    global ID
    global NAME
    global PROTOCOL
    global HOST
    global PORT
    global N_STATUS
    global C_STATUS
    global BT_STATUS
    global SCAN_TIME
    while True:
    
        try:
        
            dataa=db.getdata('Device')
            #print(dataa)
            ID=dataa[0][1]
            NAME=dataa[0][2]
            dataa=db.getdata('Cloud')
            #print(dataa)
            PROTOCOL=dataa[0][1]
            HOST=dataa[0][3]
            PORT=dataa[0][4]
            C_STATUS=dataa[0][4]
            dataa=db.getdata('Node')
            #print(dataa)
            N_STATUS=dataa[0][2]
            I_STATUS=dataa[0][3]
            SCAN_TIME=dataa[0][1]
            #print(I_STATUS)
        except:
            time.sleep(5)
            
        dbEvent.set()
        #time.sleep(10)
        
    
def preq(led):
    while True:
        if not req.empty() and SCAN_STATUS=='Active':
            r=req.get()
            node.writep(r['MAC'],r['SERVICE'],r['CHAR'],r['CONFIG'])
        
    
def pconfig(mac,service,char,config):
    request={'MAC':mac,'SERVICE':service,'CHAR':char,'CONFIG':config}
    req.put(request,block=True,timeout=2)
    

def node(dbEvent):
    FLG=dbEvent.wait()
    print("NODE STARTED")
    global BT_STATUS
    while True:
    
        payload=app_node(int(SCAN_TIME),N_STATUS)
        if not q.full() and C_STATUS=='Active':
            q.put(payload,block=True,timeout=2)
        time.sleep(3)
        
        
def cloud(client):
    while True:
        if not q.empty() and C_STATUS=='Active' and N_STATUS=='Active':#and I_STATUS=='Active':
            d = q.get()
            print(d)
            #print(q)
            for dev in d:
                dt={}
                now=datetime.now()  
                #print(now)  
                dt = {'t_stmp' : int(datetime.timestamp(now)),
                    't_utc' : now.strftime("%d/%m/%Y, %H:%M:%S"),
                    'x' : dev['Accelerometer(x)'],
                    'y' : dev['Accelerometer(y)'],
                    'z' : dev['Accelerometer(z)'],
                    'MAC' : dev['MAC'],
                    'MACTYPE' : dev['MACTYPE'],
                    'RSSI' : dev['RSSI']
                    }

                # method call
                #print('pubflag',pubflag)
                print('dt',dt)
                publishData(client, dt,awstopic,pubflag)
    
            
          

if __name__=='__main__':
    q=queue.Queue(100)
    #req=queue.Queue(100)
    
    #DB VARIABLES
    ID=''
    NAME=''
    PROTOCOL=''
    HOST=''
    PORT=''
    N_STATUS=''
    C_STATUS=''
    I_STATUS=''
    BT_STATUS=''
    SCAN_TIME=''
    #creating obejct of MQTT client
    client = mqtt.Client()

    client.message_callback_add("$aws/things/Test_gateway/jobs/notify-next",job)
    print("Connecting to AWS IoT Broker...")

    #client.subscribe("iot/#",0)
    
    #<----- cloud main ---------->
   
    # methods call
    funInitilise(client)
    client.subscribe("$aws/things/Test_gateway/jobs/notify-next",1)
    client.loop_start()
    
    dbEvent = threading.Event()
    #led = threading.Event()
    t_db_reader = threading.Thread(name='db_read', target=db_reader,args=(dbEvent,))
    t_db_reader.start()
    #t_pconfig_thread = threading.Thread(name='led thread', target=preq,args=(led,))
    #t_pconfig_thread.start()
    t_cloud=threading.Thread(name='cloud', target=cloud,args=(client,))
    t_cloud.start()
    t_node=threading.Thread(name='NODE', target=node,args=(dbEvent,))
    t_node.start()



#from database
#port = 443
#server_type = 'aws'
#custom_url = '3.142.131.2' 
    
