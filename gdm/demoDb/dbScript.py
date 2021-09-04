import sqlite3
import time

conn = sqlite3.connect('mydatabasenew.db',check_same_thread=False)

class tables():

    def createTable(self,tablename, val):
        conn.execute('create table if not exists ' + tablename + val)
        conn.commit()
        print("table created")


    def calltable(self):
        val1 = (' (Key  int ,Id varchar(20) , Name varchar(20) , IPv4 varchar(20) , Interface varchar(20) , Status varchar(20)) ')
        val2 = (' ( key int ,ServerType varchar(20) ,Ip varchar(20) , Port varchar(20) , C_Status varchar(20) ) ')
        val3 = (' (key int ,ScaneRate varchar(20)  , N_Status varchar(20) , I_Status varchar(20) ) ')
        val4 = (' (Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , Config varchar(20) , Accerlometer_X varchar(20) , Accerlometer_Y varchar(20) , Accerlometer_Z varchar(20) , date varchar(20) ) ')
        val5 = (' (Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , Config varchar(20) , Accerlometer_X varchar(20) , Accerlometer_Y varchar(20) , Accerlometer_Z varchar(20) , date varchar(20) )')

        self.createTable('Device', val1)
        self.createTable('Cloud', val2)
        self.createTable('Node', val3)
        self.createTable('HistoricalData', val4)
        self.createTable('OfflineData', val5)

    def getdata(self,tableselect):
        data=conn.execute('select * from ' + tableselect)
        data=data.fetchall()   
        return data
        
    def getdatadate(tableselect,s,p):
        d=conn.execute('select * from ' + tableselect + 'where date > = '+ s + 'and date < =' + p)
        d=d.fetchall()
        return d

    def configdataread(self):
        data = self.getdata('Device')
        print(data)
        data = self.getdata('Cloud')
        print(data)
        data = self.getdata('Node')
        print(data)


    def HistoricalDataread(self):
        data = self.getdatadate('HistoricalData')
        print(data)


    def offlinedataread(self):
        data = self.getdata('OfflineData')
        print(data)


    def callgetdata(self):
        self.getdata('Device')
        self.getdata('Cloud')
        self.getdata('Node')
        self.getdata('HistoricalData')
        self.getdata('OfflineData')


    def putdata(self,tablevalue, data):
        query = f'insert into {tablevalue} values {data}'
        conn.execute(query)
        conn.commit()

    def callputdata(self):
        self.putdata('Device', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', 'ACTIVE'))
        self.putdata('Cloud', ('1','Unsecured', 'x.x.x.x', 'xxxx', 'Inactive'))
        self.putdata('Node', ('1' ,'3', 'INACTIVE', 'INACTIVE'))
        # self.putdata('HistoricalData', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', '20' , '20' , '20' ,'2021-09-03'))
        # self.putdata('OfflineData', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', '20' , '20' , '20' '2021-09-03'))


    def deletetable(self,tablename):
        d = 'delete from ' + tablename
        print(d)
        conn.execute(d)


    def updatetable(self,tablename, c, v):
        p = f"update {tablename} set {c} = '{v}' where Key = 1"
        conn.execute(p)
        conn.commit()


p1=tables()

#p1.calltable()
# p1.callgetdata()
# self.configdataread()
# self.HistoricalDataread()
# self.offlinedataread()
#p1.callputdata()
#self.deletetable()
