import time
import board
import adafruit_icm20x
from adafruit_tca9548a import TCA9548A
from tabulate import tabulate

# Initialize I2C bus
i2c = board.I2C()

# Initialize PCA9548A mux
mux = TCA9548A(i2c)

# Initialize ICM20948 sensors
icm1 = adafruit_icm20x.ICM20948(mux[0],address=0x68)
icm2 = adafruit_icm20x.ICM20948(mux[1],address=0x68)
icm3 = adafruit_icm20x.ICM20948(mux[2],address=0x68)  # Assuming ICM20948 is connected to TCA9548A channel 0
icm4 = adafruit_icm20x.ICM20948(mux[3],address=0x68)  # Assuming another ICM20948 is connected to TCA9548A channel 1
icm5 = adafruit_icm20x.ICM20948(mux[4],address=0x68)
icm6 = adafruit_icm20x.ICM20948(mux[5],address=0x68)
icm1.accelerometer_data_rate_divisor = 4095  # minimum
print("Data Rate:", icm1.accelerometer_data_rate)

while True:
    # Read data from the sensors
    start_time=time.time()
    acc=icm1.acceleration
    gyro=icm1.gyro
    end_time=time.time()
    print(end_time-start_time)

# average datareading for acc and gyro is 0.027