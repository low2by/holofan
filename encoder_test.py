import time
import RPi.GPIO as GPIO


#class Encoder:


PIN_CLK = 2
PIN_DAT = 3
PIN_CS  = 4
delay = 0.0000005
ns = 1 # number of sensors attached chaned this to one -emmanuel
# totally 10 bits to be extracted from SSI signal
bitcount = 16

# pin setup done here
try:
    GPIO.setup(PIN_CLK,GPIO.OUT)
    GPIO.setup(PIN_DAT,GPIO.IN)
    GPIO.setup(PIN_CS,GPIO.OUT)                                                                                                    
    GPIO.output(PIN_CS,1)
    GPIO.output(PIN_CLK,1)
except:
    print "ERROR. Unable to setup the configuration requested"                                     

#wait some time to start
time.sleep(0.5)

print "GPIO configuration enabled"

def clockup():
    GPIO.output(PIN_CLK,1)
def clockdown():
    GPIO.output(PIN_CLK,0)
def MSB():
    # Most Significant Bit
    clockdown()

def readpos():
    
    GPIO.setmode(GPIO.BCM)
    
    PIN_CLK = 2
    PIN_DAT = 3
    PIN_CS  = 4
    delay = 0.0000005
    ns = 1 # number of sensors attached chaned this to one -emmanuel
    # totally 10 bits to be extracted from SSI signal
    bitcount = 16
    
    GPIO.setup(PIN_CLK,GPIO.OUT)
    GPIO.setup(PIN_DAT,GPIO.IN)
    GPIO.setup(PIN_CS,GPIO.OUT)                                                                                                    
    GPIO.output(PIN_CS,1)
    GPIO.output(PIN_CLK,1)
    
    GPIO.output(PIN_CS,0)
    time.sleep(delay*2)
    #MSB()
    data = 1*ns
    
    for i in range(0,bitcount):
        if i<10:
            #print i
            #clockup()
            GPIO.output(PIN_CLK,1)
            for j in range(0,ns):
                data <<= 1  
                data|= GPIO.input(PIN_DAT)
            #clockdown()
            GPIO.output(PIN_CLK,0)
        else:
            for k in range(0,6):
                #clockup()
                GPIO.output(PIN_CLK,1)
                #clockdown()
                GPIO.output(PIN_CLK,0)
    GPIO.output(PIN_CS,1)
    return data-1024;
try:

    while(1):
        print readpos()
        time.sleep(0.1)
        break
        
finally:
    print "cleaning up GPIO"
    GPIO.cleanup()
