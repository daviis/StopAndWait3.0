'''
Created on Oct 9, 2014

@author: daviis01
'''
import socket, traceback
from udt import *

host = ''                               # Bind to all interfaces
port = 55000
pktNum = 0
estring = "Hi Brad"


while True:
    try:
        pkt = make_pkt(estring,pktNum,host,port)
        sock = udt_send(pkt) #causes a print
        pkt,addr = udt_recv(sock)
        if pkt:
            if not pkt.is_corrupt or pkt.seqnum != pktNum:
                if "ACK" in pkt.mess and str(pktNum) in pkt.mess:
                    pktNum = (pktNum + 1) % 2
                    print(pkt.mess)
                else:
                    print("got something other than ACK for ", pktNum)
            else:
                print('either corrupt or ack of not ', pktNum)
        else:
            print('got a timeout resend ', pktNum)
    except (KeyboardInterrupt, SystemExit):
        break
    except:
        traceback.print_exc()
