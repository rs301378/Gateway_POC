import json
from bluepy.btle import Scanner

def hextodec(value):
    return -(value & 0x8000) | (value & 0x7fff)

def app_node(db):

    FLG=db.wait()
    print("NODE STARTED")
    global BT_STATUS
    while True:
        if N_STATUS=='Active':
            bt=subprocess.check_output(['hciconfig'])
            if b'UP' in bt:
                BT_STATUS='Active'
            else:
                BT_STATUS='Inactive'
            if BT_STATUS=='Active' and C_STATUS=='Active':
                lescan=Scanner(0)
                devices=lescan.scan(3)
                for dev in devices:
                    man=dev.getValueText(255)
                    z=man[14:16] + man[12:14]
                    y=man[10:12] + man[8:10]
                    x=man[6:8] + man[4:6]
                    x=hextodec(int(x, 16))*0.00245
				    y=hextodec(int(y, 16))*0.00245
				    z=hextodec(int(z, 16))*0.00245
                    payload={'TYPE':'Beacon'}
                    payload.update({'MAC':dev.addr,'MAC TYPE':dev.addrType,'RSSI':dev.rssi,'Accelerometer(x)':x,'Accelerometer(y)':y,'Accelerometer(z)':z})
                    for (adtype,desc,value) in dev.getScanData():
                        payload.update({desc:value})
                    if not q.full() and C_STATUS=='Active':
                        q.put(payload,block=True,timeout=2)

        time.sleep(3)
