'''
Created on Oct 9, 2014

@author: daviis01
'''
import socket, traceback
from udt import *

global pktNum 
pktNum = 0

def rdt_send(someMsg):
    host = ''                               # Bind to all interfaces
    port = 55000
    needToSend = True 
    global pktNum 
    while needToSend:
        try:
            pkt = make_pkt(someMsg,pktNum,host,port)
            sock = udt_send(pkt) #causes a print
            pkt,addr = udt_recv(sock)
            if pkt:
                if not pkt.is_corrupt or pkt.seqnum != pktNum:
                    if "ACK" in pkt.mess and str(pktNum) in pkt.mess:
                        pktNum = (pktNum + 1) % 2
                        print(pkt.mess)
                        needToSend = False
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

def main():
    message = "wow this is a long message about nothing important, but hi brad"
    
    for word in message.split(sep=" "):
        rdt_send(word)
    
    
if __name__ == '__main__':
    main()