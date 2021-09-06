import threading
import time
import sqlite3
import paho.mqtt.client as mqtt
import requests
import socket
import queue
import json
import subprocess
from collections import deque
from cloud import *
from node import *
from database import p1 as db
from datetime import datetime

awstopic=""
pubflag=False
conFlag=True


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




def monitor(monEvent,conEvent):
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
    global conFlag
    global SERVER_TYPE
    while True:

        if len(mainBuffer['monitor'])!=0:
            dataa=mainBuffer['monitor'].popleft()
            ID=dataa['ID']
            NAME=dataa['NAME']
            HOST=dataa['HOST']
            PORT=dataa['PORT']
            C_STATUS=dataa['C_STATUS']
            N_STATUS=dataa['N_STATUS']
            I_STATUS=dataa['I_STATUS']
            SCAN_TIME=dataa['SCAN_TIME']
            SERVER_TYPE=dataa['SERVER_TYPE']
            if conFlag==True:
                conEvent.set()
                conFlag=False
            monEvent.set()
        mainBuffer['dbCmnd'].append({'table':'','operation':'read','value':'','source':'monitor'})
        print("Cloud-",C_STATUS)
        print("Node-",N_STATUS)
        print("Scan-",SCAN_TIME)
        print("Host-",HOST)
        print("Prev_host-",prev_HOST)
        time.sleep(5)





def preq(led):
    while True:
        if not req.empty() and SCAN_STATUS=='Active':
            r=req.get()
            node.writep(r['MAC'],r['SERVICE'],r['CHAR'],r['CONFIG'])


def pconfig(mac,service,char,config):
    request={'MAC':mac,'SERVICE':service,'CHAR':char,'CONFIG':config}
    req.put(request,block=True,timeout=2)


def node(monEvent):
    FLG=monEvent.wait()
    print("NODE STARTED")
    global BT_STATUS
    while True:
        if C_STATUS=='Active' and N_STATUS=='Active':
            payload=app_node(int(SCAN_TIME))
            if payload!=None:
                q.append(payload)
        time.sleep(3)


def cloud():
    global client
    global pubflag

    while True:
        chgEvent.wait()
        print("cloud publish")
        if len(q)!=0 and C_STATUS=='Active' and N_STATUS=='Active':#and I_STATUS=='Active':
            d = q.popleft()
            #print(d)
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
                #print('dt',dt)
                if SERVER_TYPE == 'custom':
                    pubflag=True
                publishData(client,dt,awstopic,pubflag,mainBuffer,SERVER_TYPE)
        time.sleep(3)

def dbMaster():
    while True:

        if len(mainBuffer['dbCmnd'])!=0:

            job=mainBuffer['dbCmnd'].popleft()
            source=job['source']
            table=job['table']
            value=job['value']

            if job['operation']=='read':

                if source=='monitor':

                    dataa=db.getdata('Device')
                    ID_=dataa[0][1]
                    NAME_=dataa[0][2]

                    dataa=db.getdata('Cloud')
                    SERVER_TYPE_=dataa[0][1]
                    HOST_=dataa[0][2]
                    PORT_=dataa[0][3]
                    C_STATUS_=dataa[0][4]


                    dataa=db.getdata('Node')
                    N_STATUS_=dataa[0][2]
                    I_STATUS_=dataa[0][3]
                    SCAN_TIME_=dataa[0][1]
                    payl={'ID':ID_,'NAME':NAME_,'SERVER_TYPE':SERVER_TYPE_,'HOST':HOST_,'PORT':PORT_,'C_STATUS':C_STATUS_,'N_STATUS':N_STATUS_,'I_STATUS':I_STATUS_,'SCAN_TIME':SCAN_TIME_}
                    mainBuffer[source].append(payl)

                #if source=='cloud':
                    #dataa=db.getdata('HistoricalData')



            if job['operation']=='write':
                if table=='HistoricalData':
                    db.putdata(table,value)
                if table=='OfflineData':
                    db.putdata(table,value)



        time.sleep(1)



if __name__=='__main__':

    mainBuffer={
            'cloud':deque([]),
            'monitor':deque([]),
            'dbCmnd':deque([])
               }

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
    prev_HOST=''
    prev_PORT=''
    SERVER_TYPE=''
    #creating obejct of MQTT client
    q=deque([])



    conEvent=threading.Event()
    monEvent=threading.Event()
    chgEvent=threading.Event()
    t_dbMaster=threading.Thread(name='dbMaster', target=dbMaster)
    t_dbMaster.start()
    t_monitor = threading.Thread(name='monitor', target=monitor,args=(monEvent,conEvent,))
    t_monitor.start()
    t_node=threading.Thread(name='NODE', target=node,args=(monEvent,))
    t_node.start()

    #conEvent.wait()
    #connflag=False
    #client = mqtt.Client()

    #client.message_callback_add("$aws/things/Test_gateway/jobs/notify-next",job)
    #print("Connecting first time to cloud.")
    t_cloud=threading.Thread(name='cloud', target=cloud)
    t_cloud.start()
    while True:
        if prev_HOST!=HOST or prev_PORT!=PORT:
            print("-"*20)
            print("Server setting")
            #print(HOST)
            #print(PORT)
            if chgEvent.isSet():
                chgEvent.clear()
            if connflag==True:
                client.loop_stop()
                client.disconnect()
            client = mqtt.Client()
            #client.message_callback_add("$aws/things/Test_gateway/jobs/notify-next",job)
            print("Connecting to cloud...")
            #pubflag=False
            funInitilise(client,SERVER_TYPE,HOST,PORT)
            prev_HOST=HOST
            prev_PORT=PORT
            #print("Current",prev_HOST)
            if SERVER_TYPE == 'aws':
                pubflag=False
                client.subscribe("$aws/things/Test_gateway/jobs/notify-next",1)
            client.loop_start()
            chgEvent.set()
            print("-"*20)
        #print("main running")
        time.sleep(5)
