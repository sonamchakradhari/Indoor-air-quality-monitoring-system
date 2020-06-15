import RPi.GPIO as GPIO
import time
from urllib.request import urlopen

#write_api = "KFS5CGA822E0W8GY"
#write_api = "S87753IC4AO4FQKK"
#write_api="I0VHGAIKI98ZFGSO"
#base_url="https://api.thingspeak.com/update?api_key={}".format(write_api)
#base_url="https://api.thingspeak.com/update?api_key={}".format(write_api)
#base_url="https://api.thingspeak.com/update?api_key={}".format(write_api)

write_api = "KFS5CGA822E0W8GY"
base_url="https://api.thingspeak.com/update?api_key={}".format(write_api)



p1_falling_time=0
p1_rising_time=0
p1_pulse_width = 0
p1_avg=0
no_sample = 8 #no of samples to calculate avg
p1_sample_n=0  

p2_falling_time=0
p2_rising_time=0
p2_pulse_width = 0
p2_avg=0
p2_sample_n=0  
#get the milli seconds
def millisectime ():
    return int(round(time.time()*1000))

#pin configuration of dust sensor
p1_small_PIN = 12
p2_large_PIN = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(p1_small_PIN, GPIO.IN)
GPIO.setup(p2_large_PIN, GPIO.IN)

#GPIO.add_event_detect(p1_small_PIN, GPIO.RISING)
#GPIO.add_event_detect(16, GPIO.RISING)

GPIO.add_event_detect(p1_small_PIN, GPIO.BOTH)
GPIO.add_event_detect(p2_large_PIN, GPIO.BOTH)

#GPIO.add_event_detect(p1_small_PIN, GPIO.FALLING)
#GPIO.add_event_detect(16, GPIO.FALLING)


try :
    run_time = millisectime()
    run_end_time = run_time + 120000
#    while (millisectime()<run_end_time):
    while(1):
        count_p1=0 #count no p1 of times
        count_p2=0 #count of p2 particles
        total=0
        start_time = millisectime()
        end_time = start_time+15000  # 15 sec time for the samples
        #while(1):
        while (millisectime()<end_time):
            #total=total+1
            if GPIO.event_detected(p1_small_PIN):
                if GPIO.input(p1_small_PIN) == 0:
                    p1_falling_time = millisectime() #time.time()
                    p1_rising_time=0
                    #print("p1:falling:",GPIO.input(12),p1_falling_time)
                    
                if GPIO.input(p1_small_PIN) == 1:
                    if p1_falling_time != 0:
                        p1_rising_time = millisectime() #time.time()
                        p1_pulse_width = p1_rising_time - p1_falling_time
                        #print("p1-small particle: pulse width:",p1_pulse_width)
                        
                        
                        #thingspeakhttp = base_url+"&field5={:.2f}".format(p1_pulse_width)
                        #conn = urlopen(thingspeakhttp)
                        #conn.read()
                        #conn.close()
                        
                        p1_sample_n = p1_sample_n+1
                        p1_avg = p1_avg + p1_pulse_width
                        #if p1_sample_n <= no_sample:
                         #   p1_sample_n=p1_sample_n+1
                          #  p1_avg = p1_avg+p1_pulse_width
                        #if p1_sample_n > no_sample:
                         #   p1_avg = (p1_avg/(30000*3))*100
                          #  print("p1_avg:",p1_avg)
                           # p1_sample_n=0
                    p1_pulse_width = 0
                    p1_falling_time = 0
                    p1_rising_time = 0
                    #print("p1:rising:",GPIO.input(12),p1_rising_time)
                
                count_p1=count_p1 +1
            
            if GPIO.event_detected(p2_large_PIN):
                #print("p2:",GPIO.input(16),time.time())
                if GPIO.input(p2_large_PIN) == 0:
                    p2_falling_time = millisectime() #time.time()
                    p2_rising_time=0
                    #print("p2:falling:",GPIO.input(16),p2_falling_time)
                
                if GPIO.input(p2_large_PIN) == 1:
                    if p2_falling_time != 0:
                        p2_rising_time = millisectime() #time.time()
                        p2_pulse_width = p2_rising_time - p2_falling_time
                        #print("p2-large particle:pulse width:",p2_pulse_width)
                        
                        #thingspeakhttp = base_url+"&field6={:.2f}".format(p2_pulse_width)
                        #conn = urlopen(thingspeakhttp)
                        #conn.read()
                        #conn.close()
                        
        
                        p2_sample_n = p2_sample_n+1
                        p2_avg=p2_avg+p2_pulse_width
                        #if p2_sample_n <= no_sample:
                         #   p2_sample_n=p2_sample_n+1
                          #  p2_avg = p2_avg+p2_pulse_width
                        #if p2_sample_n > no_sample:
                         #   p2_avg = (p2_avg/30000)
                          #  print("p2_avg:",p2_avg)
                           # p2_sample_n=0
                       
                    p2_pulse_width = 0
                    p2_falling_time = 0
                    p2_rising_time = 0
                    #print("p2:rising:",GPIO.input(p2_large_PIN),p2_rising_time)
                
                count_p2=count_p2 +1
        
        
        p1_avg = (p1_avg/(15000*3))*100
        p1_concentration = round(p1_avg/0.0072,3)
        print("small particle dust concentration:",p1_concentration)

        #print("dust concentration:",p1_concentration)
        
        
        print("p1_lpo:",round(p1_avg,2))
        
        
        p2_avg = (p2_avg/15000) * 100
        p2_concentration = round(p2_avg/0.0072,3)
        print("large particle dust concentration:",p2_concentration)
        #print("dust concentration:",p2_concentration)
        print("p2_lpo:",round(p2_avg,2))
    
        thingspeakhttp = base_url+"&field3={:.2f}&field4={:.2f}&field5={:.2f}&field6={:.2f}".format(p1_avg,p2_avg,p1_concentration,p2_concentration)
        conn = urlopen(thingspeakhttp)
        conn.read()
        conn.close()
        
        
        
    print("total-p1:",count_p1)
    print("total-p2:",count_p2)
    #print("total:",total)
    
    GPIO.cleanup()
except:
    pass
    
    
    
    #print(" error")
    #print("total-p1:",count_p1)
    #print("total-p2:",count_p2)
    #GPIO.cleanup()
    #p1_avg = (p1_avg/(30000*3))*100
    #print("p1_avg:",p1_avg)
    
    #p2_avg = (p2_avg/30000) * 100
    #print("p2_avg:",p2_avg)
    
    
    #print("total:",total)
    

