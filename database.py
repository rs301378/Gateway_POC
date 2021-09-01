import sqlite3
conn = sqlite3.connect('mydatabase.db')

def createTable(tablename,val):
    
    conn.execute('create table if not exists ' + tablename + val)
    conn.commit()
    print("table created")

def calltable():
        
    val1=(' (Key varchar(20) ,Id int , Name varchar(20) , IPv4 varchar(20) , Interface varchar(20) , Status varchar(20)) ')
    val2=('(Key int , Protocol varchar(20) , ConType varchar(20) , Host varchar(20) , Port varchar(20)) ')
    val3=('(Key int , N_Status varchar(20) , C_Status varchar(20)) ')
    val4=('(Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , LedConfig varchar(20) , ManufactureData varchar(20)) ')
    val5=('(Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , LedConfig varchar(20) , ManufactureData varchar(20)) ')
    val6=('(PacketId int , TopicName varchar(20) , Qos int , RetainFlag varchar(20) , Payload varchar(20) , Dupflag varchar(20) ) ')
    val7=('(PacketId varchar(20) , Qos1 varchar(20) , Topic1 varchar(20) , Qos2 varchar(20) , Topic2 varchar(20)) ')
    val8=('(PacketId varchar(20) , Returncode1 varchar(20) , Returncode2 varchar(20) )')
    createTable('Device',val1)
    createTable('Cloud',val2 )
    createTable('Gateway',val3)
    createTable('Historicaldata',val4)
    createTable('Offlinedata',val5)
    createTable('Cloudpublish',val6)
    createTable('Cloudsubscribe',val7)
    createTable('Cloudsuback',val8)
def getdata(tableselect):
  
    data=conn.execute('select * from ' + tableselect)
    data=data.fetchall()   
    return data

def callgetdata():
    getdata('Device')
    getdata('Cloud')
    getdata('Gateway')
    getdata('Historicaldata')
    getdata('Offlinedata')
    getdata('Cloudpublish')
    getdata('Cloudsubscribe')
    getdata('Cloudsuback')

def putdata(tablevalue,data):
    query=f'insert into {tablevalue} values {data }' 
    conn.execute(query)
    conn.commit()

def callputdata():
    putdata('Device',('1','1100110011','Test Device','172.23.0.26','ETHERNET','ACTIVE'))    
    putdata('Cloud',('1','HTTP','Unsecured','x.x.x.x','xxxx')) 
    putdata('Gateway',('1','INACTIVE','INACTIVE'))
    putdata('Historicaldata',('1','1100110011','Test Device','172.23.0.26','ETHERNET','ACTIVE'))
    putdata('Offlinedata',('1','1100110011','Test Device','172.23.0.26','ETHERNET','ACTIVE'))
    putdata('Cloudpublish',('1','1100110011','Test Device','172.23.0.26','ETHERNET','ACTIVE'))
    putdata('Cloudsubscribe',('1','HTTP','Unsecured','x.x.x.x','xxxx'))
    putdata('Cloudsuback',('1','INACTIVE','INACTIVE'))

def updatetable(tablename,c,v):
    u='update ' + tablename + ' set ' + c + '=' + v +' where Key = 1'
    print(u)
    conn.execute(u)

def deletetable(tablename):
    d='delete from ' + tablename
    print(d)
    conn.execute(d)

#"UPDATE Cloud SET PROTOCOL=?,CONTYPE=?,HOST=?,PORT=?  WHERE KEY = 1",('MQTT','Unsec','3.142.131.2','5555')
#calltable()
#callgetdata()
#callputdata()
#deletetable('Device')
