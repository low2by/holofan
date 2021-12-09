import time
import RPi.GPIO as GPIO


class Encoder:
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    
        #Pin1(Digital Input): nothing
        #Pin2: Clock - GPIO2
        #Pin3: GND - GND
        #Pin4: Digital Output - GPIO3
        #Pin5: VCC - 3.3v
        #Pin6: CS - GPIO4
        
        self.PIN_CLK = 17
        self.PIN_DAT = 27
        self.PIN_CS  = 4
        self.delay = 0.0000005
        self.ns = 1 # number of sensors attached chaned this to one -emmanuel
        # totally 10 bits to be extracted from SSI signal
        self.bitcount = 16

        # pin setup done here
        try:
            GPIO.setup(self.PIN_CLK,GPIO.OUT)
            GPIO.setup(self.PIN_DAT,GPIO.IN)
            GPIO.setup(self.PIN_CS,GPIO.OUT)                                                                                                    
            GPIO.output(self.PIN_CS,1)
            GPIO.output(self.PIN_CLK,1)
        except:
            print ("ERROR. Unable to setup the configuration requested")                                     

        #wait some time to start
        time.sleep(0.5)
    


    def clockup(self):
        GPIO.output(self.PIN_CLK,1)
        
    def clockdown(self):
        GPIO.output(self.PIN_CLK,0)
        
    def MSB(self):
        # Most Significant Bit
        self.clockdown()

    def readpos(self):
        
#         GPIO.setup(self.PIN_CLK,GPIO.OUT)
#         GPIO.setup(self.PIN_DAT,GPIO.IN)
#         GPIO.setup(self.PIN_CS,GPIO.OUT)                                                                                                    
#         GPIO.output(self.PIN_CS,1)
#         GPIO.output(self.PIN_CLK,1)
        
        GPIO.output(self.PIN_CS,0)
        time.sleep(self.delay*2)
        self.MSB()
        data = 0
        
        full_data = 0
        
        for i in range(0,self.bitcount):
            if i<16:
                #print i
                self.clockup()
                GPIO.output(self.PIN_CLK,1)
                for j in range(0,self.ns):
                    data <<= 1  
                    data|= GPIO.input(self.PIN_DAT)
                self.clockdown()
                GPIO.output(self.PIN_CLK,0)
#             else:
#                 for k in range(0,6):
#                     self.clockup()
#                     self.clockdown()
        GPIO.output(self.PIN_CS,1)
        return data;

if __name__ == "__main__":
        
    try:
        encoder = Encoder();
        while(1):
            
            #print("{:016b}".format(encoder.readpos()))
            print(encoder.readpos())
            time.sleep(0.1)
            #break
            
    finally:
        print ("cleaning up GPIO")
        GPIO.cleanup()
