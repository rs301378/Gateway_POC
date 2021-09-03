import sqlite3
import time

conn = sqlite3.connect('mydatabasenew.db')

class tables():

    def createTable(self,tablename, val):
        conn.execute('create table if not exists ' + tablename + val)
        conn.commit()
        print("table created")


    def calltable(self):
        val1 = (' (Key  int ,Id varchar(20) , Name varchar(20) , IPv4 varchar(20) , Interface varchar(20) , Status varchar(20)) ')
        val2 = (' ( key int ,ServerType varchar(20) ,Ip varchar(20) , Port varchar(20) , C_Status varchar(20) ) ')
        val3 = (' (key int ,ScaneRate varchar(20)  , N_Status varchar(20) , I_Status varchar(20) ) ')
        val4 = ('(Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , Config varchar(20) , Accerlometer_X varchar(20) , Accerlometer_Y varchar(20) , Accerlometer_Z varchar(20)) , date varchar(20) ')
        val5 = ('(Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , Config varchar(20) , Accerlometer_X varchar(20) , Accerlometer_Y varchar(20) , Accerlometer_Z varchar(20)) , date varchar(20)')

        p1.createTable('Device', val1)
        p1.createTable('Cloud', val2)
        p1.createTable('Node', val3)
        p1.createTable('HistoricalData', val4)
        p1.createTable('OfflineData', val5)

    def getdata(self,tableselect):

        try:
            data=conn.execute('select * from ' + tableselect)
            data=data.fetchall()   
            return data

        except:
            time.sleep(2)
            return p1.getdata(tableselect)
        
    def getdatadate(tableselect,s,p):
        d=conn.execute('select * from ' + tableselect + 'where date > = '+ s + 'and date < =' + p)
        d=d.fetchall()
        return d

    def configdataread(self):
        data = p1.getdata('Device')
        print(data)
        data = p1.getdata('Cloud')
        print(data)
        data = p1.getdata('Node')
        print(data)


    def HistoricalDataread(self):
        data = p1.getdatadate('HistoricalData')
        print(data)


    def offlinedataread(self):
        data = p1.getdata('OfflineData')
        print(data)


    def callgetdata(self):
        p1.getdata('Device')
        p1.getdata('Cloud')
        p1.getdata('Node')
        p1.getdata('HistoricalData')
        p1.getdata('OfflineData')


    def putdata(self,tablevalue, data):
        try:
            query = f'insert into {tablevalue} values {data}'
            conn.execute(query)
            conn.commit()
        except:
            time.sleep(2)
            p1.putdata(tablevalue,data)


    def callputdata(self):
        p1.putdata('Device', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', 'ACTIVE'))
        p1.putdata('Cloud', ('1','Unsecured', 'x.x.x.x', 'xxxx', 'Inactive'))
        p1.putdata('Node', ('1' ,'3', 'INACTIVE', 'INACTIVE'))
        p1.putdata('HistoricalData', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', '20' , '20' , '20' ,'2021-09-03'))
        p1.putdata('OfflineData', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', '20' , '20' , '20' '2021-09-03'))


    def deletetable(self,tablename):
        d = 'delete from ' + tablename
        print(d)
        conn.execute(d)


    def updatetable(self,tablename, c, v):
        try:
            p = f"update {tablename} set {c} = '{v}' where Key = 1"
            conn.execute(p)
            conn.commit()
        except:
            time.sleep(2)
            p1.updatetable(tablename,c,v)


p1=tables()

#p1.calltable()
p1.callgetdata()
p1.configdataread()
p1.HistoricalDataread()
p1.offlinedataread()
p1.callputdata()
#p1.deletetable()