'''
@author: Aditya Verma, Rohit Sharma
Date:28/08/2021

'''
#import paho.mqtt.client as mqtt
import ssl, random
import time
from datetime import datetime
import json
import sys

mqtt_url = "a3qvnhplljfvjr-ats.iot.us-west-2.amazonaws.com"
root_ca = 'C:/Users/ROHIT/Desktop/scratch_N/certs/AmazonRootCA1.pem'
public_crt = 'C:/Users/ROHIT/Desktop/scratch_N/certs/gateway-certificate.pem.crt'
private_key = 'C:/Users/ROHIT/Desktop/scratch_N/certs/gateway-private.pem.key'

connflag = False
pubflag= False

def onConnect(client, userdata, flags, response_code):
    global connflag
    
    if response_code == 0:
        client.connflag = True #set falg 
        print("Connection Ok..., connected with status: {0}".format(response_code))
    else:
        print("Bad connection!", response_code)

def onPublish(client, userdata, mid):
    print(userdata + " -- " + mid)
    #client.disconnect()

def onLedControl(client, obj, msg):
    print("LED Control"+msg.topic+"::"+str(msg.payload)+str(type(msg.payload)))
    cmd=json.loads(msg.payload)
    print("MAC:",cmd["MAC"])
    print("CMD:",cmd["CMD"])

def updateJobStatus(client, jobId,status):
    client.publish(getUrl(jobId), getStatusJSON(status),0)

def getStatusJSON(status):
    return json.dumps({
        "status" : status
    })

def getUrl(jobId):
    return "$aws/things/Test_gateway/jobs/"+jobId+"/update"

def onJob(client, obj, msg):
    try:
        global pubflag
        print(str(msg.payload))
        jobconfig = json.loads(msg.payload.decode('utf-8'))
       
        if 'execution' in jobconfig:
            jobid = jobconfig['execution']['jobId']
            operation = jobconfig['execution']['jobDocument']['operation']
            cmd=jobconfig['execution']['jobDocument']['command']
           
            #jobstatustopic = "$aws/things/Test_gateway/jobs/"+ jobid + "/update"
       
            if operation=="publish" and cmd=="start":
                pubflag=True
            elif operation=="publish" and cmd=="stop":
                pubflag=False
            
            client.publish(getUrl, getStatusJSON,0)
    except:
        print("Exception occured")
        updateJobStatus(jobid,'Failed')

def onGeneral(client,obj,msg):
    print("GENERAL"+msg.topic+"::"+str(msg.payload))

# method for publishing data
def publishData(client):
    
    topic="thing/1100/data"
    name="BLE Gateway"
    sys_type="Gateway"
    dev_type="Beacon"
    dev_id="FF:00:00:FF:AA:BB"
    sensor="Accelerometer"
    
    while True:
        time.sleep(5)
        #print(connflag) 
        if connflag == True and pubflag == True :
            now=datetime.now()
            t_stmp=int(datetime.timestamp(now))
            t_utc=now.strftime("%d/%m/%Y, %H:%M:%S")
            x="{:.3f}".format(random.uniform(-5,5))
            y="{:.3f}".format(random.uniform(-5,5))
            z="{:.3f}".format(random.uniform(-5,5))
            
            msg = {
		        "Name": name,
                "Type":sys_type,
                "Device":dev_type,
                "DeviceID":dev_id,
		        "TimestampUTC": t_utc,
		        "Timestamp": t_stmp,
		        "Sensor":sensor,
                "X-axis":x,
                "Y-axis":y,
                "Z-axis":z 
	         }
            data=json.dumps(msg)
            client.publish(topic,data,qos=1)
            #print("Published: " + "%.2f" % ap_measurement )
        else:
            print("waiting...")

# method for subscription
def subscribeClient(client):
    client.message_callback_add("iot/led", onLedControl)
    client.message_callback_add("iot/general", onGeneral)
    client.message_callback_add("$aws/things/Test_gateway/jobs/notify-next", onJob)

    #client.subscribe("iot/#",0)
    client.subscribe("$aws/things/Test_gateway/jobs/notify-next",1)
    client.loop_start()


def funInitilise(client):
    client.tls_set(root_ca,
                   certfile = public_crt,
                   keyfile = private_key,
                   cert_reqs = ssl.CERT_REQUIRED,
                   tls_version = ssl.PROTOCOL_TLSv1_2,
                   ciphers = None)

    client.on_connect = onConnect
    #client.on_publish = on_publish
    
    #Internet connection handling
    print("Connecting to AWS IoT Broker...")
    try:
        client.connect(mqtt_url, port = 8883, keepalive=60)
    except:
        print("Cannot connect to AWS IoT Broker!")
        sys.exit(1)
    
