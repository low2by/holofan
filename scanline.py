from numpy import asarray
from PIL import Image
import numpy as np
import math
from Profiler import profile


def get_pixels(deg, arr, POINTS):
    h, w, channels = arr.shape
    midw = w/2
    midh = h/2
    mindim = min(w, h)
    midmindim = mindim/2
    
    rad = deg*math.pi/180
    m = math.tan(rad)
    b = midh-m*midw
    # print("y="+str(m)+"x+"+str(b))
    pixels = np.zeros((POINTS, 3), dtype=np.uint8)
    
    a = midmindim * math.cos(rad)
    o = midmindim * math.sin(rad)
    
    #rounding
#    wpoints = enumerate(np.rint(np.linspace(midw-a, midw+a-1, POINTS)).astype(int))
#    hpoints = enumerate(np.rint(np.linspace(midh-o, midh+o-1, POINTS)).astype(int))

    #truncating
    wpoints = enumerate(np.linspace(midw-a, midw+a-1, POINTS).astype(int))
    hpoints = enumerate(np.linspace(midh-o, midh+o-1, POINTS).astype(int))

    if abs(m) < 1:
        for idx, _x in wpoints:
            x = _x
            y = int(m*x + b) #truncating
#            y = round(m*x + b) #rounding
            pixels[idx] = arr[min(y, arr.shape[0]-1)][min(x, arr.shape[1]-1)]
    else:
        for idx, _y in hpoints:
            y = _y
            x = int((y-b)/m) #truncating
#            x = round((y-b)/m) #rounding
            pixels[idx] = arr[min(y, arr.shape[0]-1)][min(x, arr.shape[1]-1)]
    return pixels

@profile
def main():
    from encoder_test import Encoder
    encoder = Encoder();
    image = Image.open('/home/pi/Desktop/test.jpeg')
    arr = asarray(image)
    POINTS = 128
    while(1):
        
        #line = get_pixels(encoder.readpos()*0.3516, arr, POINTS).reshape((1, POINTS, 3))
        line = get_pixels(encoder.readpos()*0.3516, arr, POINTS).reshape((1, POINTS, 3))
        #thickline = np.tile(line, (30,1,1))
#        img = Image.fromarray(line, 'RGB')
#        img.save('/home/pi/Pictures/slice'+str(deg)+'.jpg')
    
if __name__ == "__main__":
    main()
    
