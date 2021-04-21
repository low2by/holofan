import pi3d
from multiprocessing import Process
import time
import RPi.GPIO as GPIO
from encoder import Encoder
from scanline import get_pixels
from PIL import Image

class ObjectSpace:
    def __init__(self):
#         GPIO.setmode(GPIO.BCM)
        self.prevValue = 0
        self.rotation = 0
        self.rotateVert = False

        self.DISPLAY = pi3d.Display.create(0,0,1920,1080, window_title='Holofan', near=0.1)
        self.LOGGER = pi3d.Log(level='DEBUG', file='error.log')
        self.DISPLAY.set_background(0,0,0,1)
        
#         e1 = Encoder(17, 27, callback=valueChanged)
# 
#         GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.add_event_detect(22, GPIO.RISING, callback=button_callback)
        
        self.mykeys = pi3d.Keyboard()

    def load_obj(self, objPath, name):
        self.mymodel = pi3d.Model(file_string=objPath, name=name, z=1.0)
        self.mymodel.translateY(-0.2)
        self.mymodel.set_material((1.0, 1.0, 1.0))
        #mymodel.translate(0,1,0)
        
    def update(self):
        if self.DISPLAY.loop_running():
            k = self.mykeys.read()
            if k > -1:
                if k == 112:  #key p picture6
#                     p = Process(target=generate_lines)
#                     p.start()
                    img = Image.fromarray(line, 'RGB')
                    self.LOGGER.info(img)
                    img.save('slices/'+str(deg)+'.jpg')
                    
                elif k == 27:  #Escape key
                    self.mykeys.close()
                    self.DISPLAY.destroy()
#                   GPIO.cleanup()
            self.mymodel.draw()

    def rotateModel(self, deg, axis='y'):
        if axis.lower() == 'x':
            self.mymodel.rotateIncX(deg)
        if axis.lower() == 'y':
            self.mymodel.rotateIncY(deg)
        if axis.lower() == 'z':
            self.mymodel.rotateIncZ(deg)

    def valueChanged(value):
        if self.rotateVert:
            self.mymodel.rotateIncX(18 if value > self.prevValue else -18)
        else:
            self.mymodel.rotateIncY(18 if value > self.prevValue else -18)
        self.prevValue = value

    def button_callback(channel):
        time.sleep(.01)
        self.rotateVert = not self.rotateVert

    def generate_lines():
        arr = pi3d.screenshot()
        for deg in range(180):
            line = get_pixels(deg, arr, 128)



if __name__=="__main__":
    space = ObjectSpace()
    space.load_obj("banana.obj", "banana")
    while True:
        space.rotateModel(6)
        space.update()