import json
from bluepy.btle import Scanner, DefaultDelegate , UUID, Peripheral
from time import sleep
import struct
import sys
from datetime import datetime
import subprocess


def hextodec(value):
    return -(value & 0x8000) | (value & 0x7fff)
 

def writeLED(mac,service,char,config):
    led_service_uuid = UUID(service) #in string format
    led_char_uuid = UUID(char)
    
    if SCAN_STATUS=='Inactive':
        p = Peripheral(mac, "random")
        led_srv=p.getServiceByUUID(led_service_uuid) # Service object for dev
        led_ch=led_srv.getCharacteristics(led_char_uuid)[0] # Charateristic object for dev
        if config=='Active':
            led_ch.write(struct.pack('B', 0x01))
        if config=='Inactive':
            led_ch.write(struct.pack('B', 0x00))
        p.disconnect()
        
    if SCAN_STATUS=='Active':
        time.sleep(3)
        writeLED(mac,service,char,config)

def app_node(SCAN_TIME,N_STATUS):

    if N_STATUS=='Active':
        #Accelerometer Section
        #with open("/sys/devices/virtual/misc/FreescaleAccelerometer/data","r") as VAL:
        #   r=str(VAL.readline())
        #BLE Section
        bt=subprocess.check_output(['hciconfig'])
        if b'UP' in bt:
            BT_STATUS='Active'
        else:
            BT_STATUS='Inactive'
        if BT_STATUS=='Active':
            #SCAN_STATUS='Active'
            lescan=Scanner(0)
            devices=lescan.scan(SCAN_TIME)
            payload=[]
            for dev in devices:
                #man=dev.getValueText(255)
                #print(man)
                #print(len(man))
                #z=man[14:16] + man[12:14]
                #y=man[10:12] + man[8:10]
                #x=man[6:8] + man[4:6]
                #print(x,y,z)
                #print(hextodec(int(x, 16))*0.00245,hextodec(int(y, 16))*0.00245,hextodec(int(z, 16))*0.00245)
                #x=hextodec(int(x, 16))*0.00245
                #y=hextodec(int(y, 16))*0.00245
                #z=hextodec(int(z, 16))*0.00245
                x=1
                y=2
                z=3
                now=datetime.now()
            
                payload.append({'TYPE':'Beacon','MAC':dev.addr,'MACTYPE':dev.addrType,'RSSI':dev.rssi,'Accelerometer(x)':x,'Accelerometer(y)':y,'Accelerometer(z)':z,'Timestamp':int(datetime.timestamp(now))})
                
                '''for (adtype,desc,value) in dev.getScanData():
                    payload.update({desc:value})
                if not q.full() and C_STATUS=='Active':
                    q.put(payload,block=True,timeout=2)'''
            SCAN_STATUS='Inactive'
        #elif not q.full() and C_STATUS=='Active' and BT_STATUS=='Inactive':
        #    q.put(r,block=True,timeout=2)
    #print(payload)
    return payload

