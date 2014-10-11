'''
Created on Oct 9, 2014

@author: daviis01
'''
import socket, traceback
from udt import *

host = ''                               # Bind to all interfaces
port = 55000
pktNum = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

while True:
    try:
        pkt,address = udt_recv(s)
        if pkt:
            print("Got data from ", address," mess: ", pkt.mess)
            pkt.ip = address[0]
            pkt.port = address[1]
            if pkt.seqnum == pktNum and not pkt.is_corrupt:
                pkt.seqnum = pktNum
                pkt.mess = "ACK " + str(pktNum)
                pktNum = (pktNum + 1) % 2
            else:
                pkt.mess = "ACK " + str((pktNum + 1) % 2)
                pkt.seqnum = (pktNum + 1) % 2
                print('Either corrupt or seqnum wrong, expected ', pktNum)
            udt_send(pkt)
        
    except (KeyboardInterrupt, SystemExit):
        break
    except:
        traceback.print_exc()
