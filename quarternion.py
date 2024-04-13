import time
import csv
import board
import adafruit_icm20x
from adafruit_tca9548a import TCA9548A
import ahrs
import numpy as np

class Quaternion():

    def __init__(self,T,I,M,R,P,back) -> None:
        self.T=T
        self.I=I
        self.M=M
        self.R=R
        self.P=P
        self.back=back

    def datareader(self):
        begin_time=time.time()
        acc_loader=np.ndarray((6,4,3))
        gyro_loader=np.ndarray((6,4,3))
        for i in range(4):
            acc_loader[0][i]=self.T.acceleration
            gyro_loader[0][i]=self.T.gyro
            acc_loader[1][i]=self.I.acceleration
            gyro_loader[1][i]=self.I.gyro
            acc_loader[2][i]=self.M.acceleration
            gyro_loader[2][i]=self.M.gyro
            acc_loader[3][i]=self.R.acceleration
            gyro_loader[3][i]=self.R.gyro
            acc_loader[4][i]=self.P.acceleration
            gyro_loader[4][i]=self.P.gyro
            acc_loader[5][i]=self.back.acceleration
            gyro_loader[5][i]=self.back.gyro    
        
        muzhi_attitude = ahrs.filters.Madgwick(acc=acc_loader[0], gyr=gyro_loader[0])
        shizhi_attitude = ahrs.filters.Madgwick(acc=acc_loader[1], gyr=gyro_loader[1])
        zhongzhi_attitude = ahrs.filters.Madgwick(acc=acc_loader[2], gyr=gyro_loader[2])
        wumingzhi_attitude = ahrs.filters.Madgwick(acc=acc_loader[3], gyr=gyro_loader[3])
        xiaomuzhi_attitude = ahrs.filters.Madgwick(acc=acc_loader[4], gyr=gyro_loader[4])
        shoubei_attitude = ahrs.filters.Madgwick(acc=acc_loader[5], gyr=gyro_loader[5])
        finger_quaternions = {
            'muzhi': muzhi_attitude.Q[-1],
            'shizhi': shizhi_attitude.Q[-1],
            'zhongzhi': zhongzhi_attitude.Q[-1],
            'wumingzhi': wumingzhi_attitude.Q[-1],
            'xiaomuzhi': xiaomuzhi_attitude.Q[-1],
            'shoubei':shoubei_attitude.Q[-1],
            'time': time.time()-begin_time
        }

        return finger_quaternions
"""  """


if __name__ == '__main__':

    # Initialize I2C bus
    i2c = board.I2C()
    # Initialize PCA9548A mux
    mux = TCA9548A(i2c)

    muzhi = adafruit_icm20x.ICM20948(mux[0], address=0x68)
    shizhi = adafruit_icm20x.ICM20948(mux[1], address=0x68)
    zhongzhi = adafruit_icm20x.ICM20948(mux[2], address=0x68)
    wumingzhi = adafruit_icm20x.ICM20948(mux[3], address=0x68)
    xiaomuzhi = adafruit_icm20x.ICM20948(mux[4], address=0x68)
    shoubei = adafruit_icm20x.ICM20948(mux[5], address=0x68)
    qua=Quaternion(muzhi,shizhi,zhongzhi,wumingzhi,xiaomuzhi,shoubei)
    while True:
        finger_quaternion = qua.datareader()
        for finger, quaternion in finger_quaternion.items():
            print(finger, quaternion, sep='\n')
        print()  # 打印空行以分隔不同的键值对
    # average reading time 0.34

