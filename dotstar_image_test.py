from scanline import get_pixels
from numpy import asarray
from PIL import Image
import numpy as np
import math
import pigpio
import RPi.GPIO as GPIO
import pigpio

GPIO.setmode(GPIO.BCM)

from encoder_test import readpos


REFRESHES = 512
POINTS = 128
apa102_cmd=[0]*4 + [0xE1,0, 0, 0]*POINTS + [255]*4

POINTS = 128
start_frame = [2, 192, 128]

def main():
    pi = pigpio.pi()
    h = pi.spi_open(0, int(32e6), 0xEF)
    
    image = Image.open('/home/pi/Desktop/holofan/images/uofu_logo_web.jpg')
    arr = asarray(image)
    
    #dots = dotstar.DotStar(board.SCK, board.MOSI, 128, brightness=0.05, auto_write=False, baudrate=8000000)
    
    lines = np.zeros((0, len(apa102_cmd)), int)
    
    for i in range(REFRESHES):
        #print(i*180/1024)
        pixels = get_pixels(i*(360/float(REFRESHES)), arr, POINTS)
        for j in range(len(pixels)):
            set_LED_RGB(j, pixels[j][0],pixels[j][1],pixels[j][2])
        #print(pixels.shape)
        #print(lines.shape)
        lines= np.append(lines, np.array(apa102_cmd)[np.newaxis,:], axis=0)
        
    for i in range(1024):
        pi.spi_xfer(h, lines[readpos(),:].tolist())
        
def set_LED_RGB(led, r, g, b):
    offset = (led*4) +4
    apa102_cmd[offset+1] = b
    apa102_cmd[offset+2] = g
    apa102_cmd[offset+3] = r
    
if __name__ == "__main__":
    main()
