import timeit
import math
from encoder_test import Encoder

rpm = 600.0;
radius_mm = 200.0;

def main():
    encoder = Encoder()
    count = 0
    total = 0
    for i in range(10000):
        start_time = timeit.default_timer()
        encoder.readpos();
        total += timeit.default_timer() - start_time
        count += 1;
    sample_time = total/count
    print("average time for one sample(average of 100000):" + str(sample_time) + " microseconds")
    rotation_time_sec = ((1/rpm)*60);
    samp_per_revolution =rotation_time_sec/sample_time
    print("samples per revolution: " + str(samp_per_revolution))
    angular_travel = ((rpm*360)/60)*sample_time
    print("degrees turned between samples: " + str(angular_travel) + "degrees")
    dist = radius_mm * angular_travel * math.pi/180
    print("distance traveled at ends between samples: " + str(dist) + "mm")
        

if __name__ == "__main__":
    main()
