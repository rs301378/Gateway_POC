'''
@author: Aditya Verma, Rohit Sharma
Date:28/08/2021

********************** Script Description *************************
-> In this script, only the callback functions are declared.
-> This script will handle or run from main3.py file.
-> Functions list:-
        * onConnect()
        * funInitilise()
        * publishData()

'''

import ssl, random
import time
import json
import sys
import requests
from datetime import datetime

#aws key & certificate paths
path=(__file__).split('/')
path.pop()
path="/".join(path)
path=path+'/certUploads/'
#print(path)

IoT_protocol_name = "x-amzn-mqtt-ca"
mqtt_url = "a3qvnhplljfvjr-ats.iot.us-west-2.amazonaws.com"
root_ca = path+'root.pem'   #root certificate from aws
public_crt = path+'cert.pem.crt'  #public certificate from aws
private_key = path+'key.pem.key'  #provate key from aws

connflag = False   #connection flag
connbflag = False  #bad connection flag
pubflag = False    #publish flag
awstopic="thing/1100/data"  #aws topic

'''
port = 8883     #set deafult port 8883
server_type = 'aws'  #default server_type 'aws'
custom_url = '3.142.131.2'  #set host
'''

#callback function
def onConnect(client, userdata, flags, response_code):

    #################### Function Description ####################
    #this is connection callback function when the 
    #client receives a CONNACK response from the server

    global connflag
    global connbflag
    if response_code == 0:
        connflag = True
        print("Connected with status: {0}".format(response_code))
    else:
        print("Bad Connection", response_code)
        #connbflag = True

#initialise function 
def funInitilise(client, SERVER_TYPE, HOST, PORT):
    
    #################### Function Description ####################
    #firstly this function checks the server type(custom, aws) 
    #after that it will chooses the port from database 
    #when the connection attempt failed it 
    #show "connection failed message"

    client.on_connect = onConnect
    if SERVER_TYPE == 'custom':
        client.connect(HOST)
    elif SERVER_TYPE == 'aws':
        try:
            if int(PORT) == 8883:
                client.tls_set(root_ca,
                    certfile = public_crt,
                    keyfile = private_key,
                    cert_reqs = ssl.CERT_REQUIRED,
                    tls_version = ssl.PROTOCOL_TLSv1_2,
                    ciphers = None)
                client.connect(HOST, port = int(PORT), keepalive=60)
            elif int(PORT) == 443:
                ssl_context = ssl.create_default_context()
                ssl_context.set_alpn_protocols([IoT_protocol_name])
                ssl_context.load_verify_locations(cafile=root_ca)
                ssl_context.load_cert_chain(certfile=public_crt, keyfile=private_key)
                client.tls_set_context(context = ssl_context)
                client.connect(HOST, port = int(PORT), keepalive=60)
        except:
            print("Connection failed! Please try again...")
            exit(1)

#callback function for publishing data 
def publishData(client, dt, t, pubflag, mainBuffer, SERVER_TYPE):
    
    #################### Function Description ####################
    #this function gets data from mainBuffer and start publishing data on server and also storing data offline(historical data)
    #'dt' is the dataframe which contains ('t_stmp', 't_utc', 'x', 'y', 'z', 'MAC', 'MACTYPE', 'RSSI') values from main3.py file
    #'t' is the topic name which is subscribed
    #'pubflag' is used for publication if it is true then function starts publishing data
    #'SERVER_TYPE' getting from the database file either 'custom' or 'aws' 
    #'client' is the paho mqtt object

    topic = t
    if SERVER_TYPE == 'custom':
        topic = 'Msg'

    name = "BLE Gateway"
    sys_type ="Gateway"
    dev_type ="Beacon"
    sensor = "Accelerometer"

    t_utc = dt.get('t_utc')
    t_stmp = dt.get('t_stmp')
    mac = dt.get('MAC')
    rssi = dt.get('RSSI')
    mactype = dt.get('MACTYPE')
    x = dt.get('x')
    y = dt.get('y')
    z = dt.get('z')

    msg = {
	    "Name": name,
	    "Type":sys_type,
	    "Device":dev_type,
	    "RSSI":str(rssi),
	    "IDtype":mactype,
	    "DeviceID":mac,
	    "TimestampUTC": str(t_utc),
	    "Timestamp": str(t_stmp),
	    "Sensor":sensor,
	    "X-axis":str(x),
	    "Y-axis":str(y),
	    "Z-axis":str(z)
		}

    #print('connflag',connflag,'pubflag',pubflag)
    if connflag == True and pubflag == 'True' and topic!='':
        print("Actually started")
        #Internet connection handling along with publishing data
        try:
            requests.head('http://www.google.com/', timeout=3)     #hit 'google.com' url till the time internet get back
            data = json.dumps(msg)   #converting 'msg' into json
            rt = client.publish(topic, data, qos=1)  #publish data on server
            print("Publishing Data...", rt)
            mainBuffer['dbCmnd'].append({'table':'HistoricalData','operation':'write','value':('1',mac,rssi,'1M','off',str(x),str(y),str(z),t_utc),'source':'cloud'}) 
            return True
        except requests.ConnectionError as ex:
            print("Connection Lost! Please wait for some time...")
            return False
    else:
        print("waiting...")   # it will go on 'waiting' till the connection not established successfully
        mainBuffer['dbCmnd'].append({'table':'OfflineData','operation':'write','value':('1',mac,rssi,'1M','off',str(x),str(y),str(z),t_utc),'source':'cloud'})