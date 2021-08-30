'''
@author: Aditya Verma, Rohit Sharma
Date:29/08/2021

'''
import paho.mqtt.client as mqtt
from cloud import *


# main function
if __name__ == "__main__":
    print("Loaded MQTT configuration information.")
    print("Endpoint URL: " + mqtt_url)
    print("Root Cert: " + root_ca)
    print("Device Cert: " + public_crt)
    print("Private Key: " + private_key)
    
    client = mqtt.Client()

    # methods call
    funInitilise(client)
    subscribeClient(client)
    publishData(client)
