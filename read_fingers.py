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
while True:
    # Read data from the sensors
    data = [
        ["Sensor 1", *icm1.acceleration, *icm1.gyro, *icm1.magnetic],
        ["Sensor 2", *icm2.acceleration, *icm2.gyro, *icm2.magnetic],
        ["Sensor 3", *icm3.acceleration, *icm3.gyro, *icm3.magnetic],
        ["Sensor 4", *icm4.acceleration, *icm4.gyro, *icm4.magnetic],
        ["Sensor 5", *icm5.acceleration, *icm5.gyro, *icm5.magnetic],
        ["Sensor 6", *icm6.acceleration, *icm6.gyro, *icm6.magnetic]

    ]

    headers = ["Sensor", "Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", "Mag X", "Mag Y", "Mag Z"]
    
    # Print data as a table
    print(tabulate(data, headers=headers, tablefmt="grid"))

    time.sleep(0.5)
