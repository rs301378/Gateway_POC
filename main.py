import threading
import time
import sqlite3
import paho.mqtt.client as mqtt
import requests
import socket
import queue
import json
import subprocess
import node.py

if __name__=='__main__':
    q=queue.Queue(18)
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
