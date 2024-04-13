import torch
import numpy as np
import torch.nn as nn
import board
import adafruit_icm20x
from adafruit_tca9548a import TCA9548A
from quarternion import Quaternion
from PIL import Image
import matplotlib.pyplot as plt 


class MLP(nn.Module):
    def __init__(self) :
        super().__init__()
        self.net=nn.Sequential(
            nn.Linear(24,24),nn.ReLU(),
            nn.Linear(24,14),nn.ReLU(),
            nn.Linear(14,8)
        )
        # 初始化模型的权重和偏置为 Float 类型
        for layer in self.net:
            if isinstance(layer, nn.Linear):
                layer.weight.data = layer.weight.data.double()
                layer.bias.data = layer.bias.data.double()
                
    def forward (self,x):
        return self.net(x)


model_path = './MLP_model .ckpt'


model=MLP()
model=model.to('cpu')
model.load_state_dict(torch.load(model_path))

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

# {0: 'call', 1: 'five', 2: 'love', 3: 'ok', 4: 'one', 5: 'rock', 6: 'yes', 7: 'zero'}

gesture_images = {
    0: './gesture/call.png',
    1: './gesture/five.png',
    2: './gesture/love.png',
    3: './gesture/ok.png',
    4: './gesture/one.png',
    5: './gesture/rock.png',
    6: './gesture/yes.png',
    7: './gesture/zero.png'
}

while True:
    #return a dict
    dic=qua.datareader()
    sensor_data = [
        dic["muzhi"].tolist()+dic["shizhi"].tolist()+dic["zhongzhi"].tolist()+
        dic["wumingzhi"].tolist()+dic["xiaomuzhi"].tolist()+dic["shoubei"].tolist()
    ]
    sensor_data=torch.tensor(sensor_data,dtype=torch.double)
    output=model(sensor_data)

    # {0: 'call', 1: 'five', 2: 'love', 3: 'ok', 4: 'one', 5: 'rock', 6: 'yes', 7: 'zero'}
    label=output.argmax(dim=-1)
    
    print("Predicted Gesture:", label.item())
    image_path = gesture_images.get(label.item(),'./gesture/zero.png')  # 如果手势标签对应的图片不存在，显示默认图片
    image = Image.open(image_path)

    plt.figure("Image")
    plt.imshow(image)
    plt.axis('on')
    plt.show(block=False)
    plt.pause(2.5)
    plt.close()


