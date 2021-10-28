import time
import RPi.GPIO as GPIO


class Encoder:
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    
        self.PIN_CLK = 2
        self.PIN_DAT = 3
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
            print "ERROR. Unable to setup the configuration requested"                                     

        #wait some time to start
        time.sleep(0.5)

        print "GPIO configuration enabled"
    


    def clockup(self):
        GPIO.output(self.PIN_CLK,1)
    def clockdown(sef):
        GPIO.output(self.PIN_CLK,0)
    def MSB(self):
        # Most Significant Bit
        clockdown()

    def readpos(self):
        
        GPIO.setup(self.PIN_CLK,GPIO.OUT)
        GPIO.setup(self.PIN_DAT,GPIO.IN)
        GPIO.setup(self.PIN_CS,GPIO.OUT)                                                                                                    
        GPIO.output(self.PIN_CS,1)
        GPIO.output(self.PIN_CLK,1)
        
        GPIO.output(self.PIN_CS,0)
        time.sleep(self.delay*2)
        #MSB()
        data = 0
        
        full_data = 0
        
        for i in range(0,self.bitcount):
            if i<10:
                #print i
                #clockup()
                GPIO.output(self.PIN_CLK,1)
                for j in range(0,self.ns):
                    data <<= 1  
                    data|= GPIO.input(self.PIN_DAT)
                    
                    full_data <<= 1  
                    full_data |= GPIO.input(self.PIN_DAT)
                #clockdown()
                GPIO.output(self.PIN_CLK,0)
            else:
                for k in range(0,6):
                    #clockup()
                    GPIO.output(self.PIN_CLK,1)
                    full_data <<= 1  
                    full_data |= GPIO.input(self.PIN_DAT)
                    #clockdown()
                    GPIO.output(self.PIN_CLK,0)
        GPIO.output(self.PIN_CS,1)
        #print("{:010b}".format(full_data))
        return data-512;

if __name__ == "__main__":
        
    try:
        
        while(1):
            
            #Print readpos()
            time.sleep(0.1)
            #break
            
    finally:
        print "cleaning up GPIO"
        GPIO.cleanup()
