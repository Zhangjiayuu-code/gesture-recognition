import time
import csv
import board
import adafruit_icm20x
from adafruit_tca9548a import TCA9548A
from tabulate import tabulate
from quarternion import Quaternion

# Initialize I2C bus
i2c = board.I2C()

# Initialize PCA9548A mux
mux = TCA9548A(i2c)

# Initialize ICM20948 sensors
muzhi = adafruit_icm20x.ICM20948(mux[0], address=0x68)
shizhi = adafruit_icm20x.ICM20948(mux[1], address=0x68)
zhongzhi = adafruit_icm20x.ICM20948(mux[2], address=0x68)
wumingzhi = adafruit_icm20x.ICM20948(mux[3], address=0x68)
xiaomuzhi = adafruit_icm20x.ICM20948(mux[4], address=0x68)
shoubei = adafruit_icm20x.ICM20948(mux[5], address=0x68)

# return dict like "shizhi":(si yuan shu)
qua=Quaternion(muzhi,shizhi,zhongzhi,wumingzhi,xiaomuzhi,shoubei)

# Open CSV file for writing
with open('./csv/one.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    csv_headers = ["1w", "1x", "1y", "1z", "2w", "2x", "2y", "2z", "3w", "3x", "3y", "3z",
                   "4w", "4x", "4y", "4z", "5w", "5x", "5y", "5z", "6w", "6x", "6y", "6z",
                   "gesture"
                   ]
    writer.writerow(csv_headers)
    
    # Read data from the sensors
    for i in range(2000):
        # Read data from each sensor

        dic=qua.datareader()
        sensor_data = [
            dic["muzhi"].tolist()+dic["shizhi"].tolist()+dic["zhongzhi"].tolist()+
            dic["wumingzhi"].tolist()+dic["xiaomuzhi"].tolist()+dic["shoubei"].tolist()+
            ["OK"]
        ]
        writer.writerows(sensor_data)
        print("{} collected".format(i))
