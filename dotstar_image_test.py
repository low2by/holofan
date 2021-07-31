from scanline import get_pixels
import adafruit_dotstar as dotstar
from numpy import asarray
from PIL import Image
import numpy as np
import math
import board

import pigpio

from encoder_test.py import data

POINTS = 128
start_frame = [2, 192, 128]

def main():
    
    #print data
    
    pi = pigpio.pi()
    
    spi = pi.spi_open(0, 125000000, 0)
    pi.spi_write(spi, )
    
    image = Image.open('/home/pi/Downloads/bunny.jpeg')
    arr = asarray(image)
    
    dots = dotstar.DotStar(board.SCK, board.MOSI, 128, brightness=0.05, auto_write=False, baudrate=8000000)
    
    lines = np.zeros((0, 128, 3), int)
    
    for i in range(1024):
        #print(i*180/1024)
        pixels = get_pixels(i*359/1024, arr, POINTS)
        #print(pixels.shape)
        #print(lines.shape)
        lines= np.append(lines, pixels[np.newaxis,:,:], axis=0)
        
    for i in range(1024):
        for j in range(128):
            dots[j] = lines[i,j,:]
        dots.show()
        
        
    
if __name__ == "__main__":
    main()
