import sqlite3
import time

#conn = sqlite3.connect('/home/lab/gateway/Gateway_POC/mydatabasenew.db',check_same_thread=False)

class tables():

    def createTable(self,tablename, val):
        #create table is genral function that will create table one by one by passing table name
        self.conn.execute('create table if not exists ' + tablename + val)
        self.conn.commit()
        print("table created")

    def __init__(self):
        self.conn = sqlite3.connect('/home/lab/gateway/Gateway_POC/mydatabasenew.db',check_same_thread=False)

    def calltable(self):
        #calltable function will create all 5 table with dummy parameters that are given
        #below val(i.e parameter of table) is defined for diffrent table '''
        val1 = (' (Key  int ,Id varchar(20) , Name varchar(20) , IPv4 varchar(20) , Interface varchar(20) , Status varchar(20)) ')
        val2 = (' ( key int ,ServerType varchar(20) ,Ip varchar(100) , Port varchar(20) , C_Status varchar(20) , TOPIC varchar(40), PUBFLAG varchar(20)) ')
        val3 = (' (key int ,ScaneRate varchar(20)  , N_Status varchar(20) , I_Status varchar(20) ) ')
        val4 = ('(Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , Config varchar(20) , Accerlometer_X varchar(20) , Accerlometer_Y varchar(20) , Accerlometer_Z varchar(20) , date varchar(20) )')
        val5 = ('(Id int , MacAdd varchar(20) , rssi varchar(20) , PhyConfig varchar(20) , Config varchar(20) , Accerlometer_X varchar(20) , Accerlometer_Y varchar(20) , Accerlometer_Z varchar(20) , date varchar(20))')

        #here we are passing table name and value to the function create table to create all 5 tables that are required
        self.createTable('Device', val1)
        self.createTable('Cloud', val2)
        self.createTable('Node', val3)
        self.createTable('HistoricalData', val4)
        self.createTable('OfflineData', val5)

    def getdata(self,tableselect):
        #getdata will show the data of the tables and display all the dummy data
        try:
            data=self.conn.execute('select * from ' + tableselect)
            data=data.fetchall()
            return data

        except:
            time.sleep(2)
            return self.getdata(tableselect)

    def getdatadate(self,tableselect,s,p):
        #will show the data between two dates that we will pass
        d=self.conn.execute('select * from ' + tableselect + 'where date > = '+ s + 'and date < =' + p)
        d=d.fetchall()
        return d

    def configdataread(self):
        #configdataread will show the data of all 3 tables that are defined in below program
        data = self.getdata('Device')
        print(data)
        data = self.getdata('Cloud')
        print(data)
        data = self.getdata('Node')
        print(data)


    def HistoricalDataread(self):
        #historicaldataread will show the data of only historical data table
        data = self.getdatadate('HistoricalData')
        print(data)


    def offlinedataread(self):
        #offlinedataread will show only the data of offlinedata table
        data = self.getdata('OfflineData')
        print(data)


    def callgetdata(self):
        #callgetdata will pass all the table to getdata function
        self.getdata('Device')
        self.getdata('Cloud')
        self.getdata('Node')
        self.getdata('HistoricalData')
        print(self.getdata('OfflineData'))


    def putdata(self,tablevalue, data):
        #this is the general program for inserting values into table
        try:
            query = f'insert into {tablevalue} values {data}'
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            time.sleep(2)
            print('cannot write to db')
            print(e)
            #elf.putdata(tablevalue,data)


    def callputdata(self):
        #here we are putting all the value of table and inserting into the table all table by one function i.e callputdata
        self.putdata('Device', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', 'Active'))
        self.putdata('Cloud', ('1','Unsecured', '0.0.0.0', '8883', 'Active','Dummy','False'))
        self.putdata('Node', ('1' ,'3', 'Active', 'Active'))
        self.putdata('HistoricalData', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', '20' , '20' , '20' ,'2021-09-03'))
        self.putdata('OfflineData', ('1', '1100110011', 'Test Device', '172.23.0.26', 'ETHERNET', '20' , '20' , '20' ,'2021-09-03'))


    def deletetable(self,tablename):
        #here we will delete all the data of the table that will be called
        d = 'delete from ' + tablename
        print(d)
        self.conn.execute(d)


    def updatetable(self,tablename, c, v):
        #here whenever the updatetable is called t will update the value of table by passing tablename and the parameters and the values to update
        print('hmmmmmmm')
        try:
            p = f"update {tablename} set {c} = '{v}' where Key = 1"
            print('hmmm')
            self.conn.execute(p)
            self.conn.commit()
        except Exception as e:
            print(e)
            #time.sleep(2)
            #self.updatetable(tablename,c,v)

    def putdatabeacon(self,tablevalue, data):
        #putting the values into beacon
        try:
            query = f'insert into {tablevalue} (MacAdd , rssi ,PhyConfig ,Config  , Accerlometer_X , Accerlometer_Y , Accerlometer_Z ,date) values {data}'
            print(query)
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            time.sleep(2)
            print(e)
            #self.putdatabeacon(tablevalue,data)
    def close(self):
        #connection is close
        self.conn.close()

p1=tables()
#print(p1.getdata('Node'))
#p1.calltable()

#p1.callgetdata()
#p1.configdataread()
#p1.HistoricalDataread()
#p1.offlinedataread()
#p1.callputdata()
#p1.configdataread()
#p1.close()
#p1.deletetable()
