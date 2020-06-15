import serial
import time
from urllib.request import urlopen

#write_api = "KFS5CGA822E0W8GY"
#write_api = "S87753IC4AO4FQKK"
write_api = "KFS5CGA822E0W8GY"
base_url="https://api.thingspeak.com/update?api_key={}".format(write_api)

def read_sensor():
    ser = serial.Serial('/dev/ttyS0',9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1.0)
    #print(ser.name)
    ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
    x=ser.read(9)
    if (x):
        #print(x)
        if len(x)>=5 and x[0]==0xff and x[1] == 0x86:
            #print(x[0])
            #print(x[1])
            #print(x[2])
            #print(x[3])
            #print('co2=',x[2]*256+x[3])
            co2=x[2]*256+x[3]
            temp = x[4]-40
            print('co2=',co2)
            print('temp=',temp)
            thingspeakhttp = base_url+"&field1={:.2f}&field2={:.2f}".format(co2,temp)
            #print(thingspeakhttp)
            ser.close()
            return thingspeakhttp
            #if x[4]:
             #   print('temp=',x[4]-40)
              #  temp = x[4]-40


while(True):
    try:
        thingspeakurl = read_sensor()
        #print("in main",thingspeakurl)
        conn = urlopen(thingspeakurl)
        conn.read()
        #print("response: {}".format(conn.read()))
        conn.close()
        time.sleep(2)
    except:
        
        pass
        #print('error reading')   
