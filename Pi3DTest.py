import pi3d
from multiprocessing import Process
import time
import RPi.GPIO as GPIO
from encoder import Encoder
from scanline import get_pixels
from PIL import Image

class ObjectSpace:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        prevValue = 0
        rotation = 0
        rotateVert = False

        DISPLAY = pi3d.Display.create(0,0,1920,1080, window_title='Holofan', near=0.1, use_glx=True, use_pygame=True)
        LOGGER = pi3d.Log(level='DEBUG', file='error.log')
        DISPLAY.set_background(0,0,0,1)
        mykeys = pi3d.Keyboard()

    def load_obj(self, objPath, name):
        mymodel = pi3d.Model(file_string=objPath, name=name, z=1.0)
        mymodel.translateY(-0.2)
        mymodel.set_material((1.0, 1.0, 1.0))
        #mymodel.translate(0,1,0)
        
    def run(self):
        while DISPLAY.loop_running():
            k = mykeys.read()
            if k > -1:
                if k == 112:  #key p picture6
                    p = Process(target=generate_lines)
                    p.start()
            #                img = Image.fromarray(line, 'RGB')
            #                LOGGER.info(img)
                        #img.save('slices/'+str(deg)+'.jpg')
                    
                elif k == 27:  #Escape key
                    mykeys.close()
                    DISPLAY.destroy()
                    GPIO.cleanup()
                    break
            mymodel.draw()

    def valueChanged(value):
        global rotateVert
        global prevValue
        
        if rotateVert:
            mymodel.rotateIncX(18 if value > prevValue else -18)
        else:
            mymodel.rotateIncY(18 if value > prevValue else -18)
        prevValue = value

    def button_callback(channel):
        global rotateVert
        time.sleep(.01)
        rotateVert = not rotateVert

    e1 = Encoder(17, 27, callback=valueChanged)

    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(22, GPIO.RISING, callback=button_callback)

    def generate_lines():
        arr = pi3d.screenshot()
        for deg in range(180):
            line = get_pixels(deg, arr, 128)



if __name__=="__main__":
    space = ObjectSpace()
    space.loadObj("banana.obj", "banana")
    space.run()