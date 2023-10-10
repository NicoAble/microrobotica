import Alphabot

import threading
import socket 
import time

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server_address=config1.server_address
s.bind(('0.0.0.0', 3450))       #bind del server tcp
s.listen()
c, a=s.accept()
print("connesso")


class Ostacoli(threading.Thread):
    def __init__(self, alpha):
        threading.Thread.__init__(self)
        self.alpha=alpha
        self.connessione=c
        self.DR=alpha.GetDR_status()
        self.DL=alpha.GetDL_status()
    
    def run(self):
        while True:
            self.DR=self.alpha.GetDR_status()
            self.DL=self.alpha.GetDL_status()
            #if self.DR==0 or self.DL==0: self.alpha.stop()
            stri=f"{self.DL}:{self.DR}"
            self.connessione.sendall(stri.encode())
            #print(stri)
            time.sleep(1)


def main():
    Ab=Alphabot.AlphaBot() 
    obstacles=Ostacoli(Ab)
    obstacles.start()
    while True:
        text_received = c.recv(4096)
        #print(text_received.decode())
        t=text_received.decode()
        l=t.split(',')
        t=l[0]
        pwm=l[1]
        pwm=float(pwm)
        if pwm < 27: pwm=27
        elif pwm > 100: pwm=100

        i=float(t[2:])
        if(t[1]==";"):
            if((t[:1]=='F') or t[:1]=='f'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    c.sendall(b"ok")
                    Ab.forward()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: c.sendall(b"error") #questo address è quello del client che ha mandato dati al server
            elif((t[:1]=='B') or t[:1]=='b'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    c.sendall(b"ok")
                    Ab.backward()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: c.sendall(b"error")
            elif((t[:1]=='L') or t[:1]=='l'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    c.sendall(b"ok")
                    Ab.left()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: c.sendall(b"error")
            elif((t[:1]=='R') or t[:1]=='r'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    c.sendall(b"ok")
                    Ab.right()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: c.sendall(b"error")
            elif((t[:1]=='E') or t[:1]=='e'):
                c.sendall(b"exit") 
                print("esecuzione terminata forzatamente")
                break
            else: c.sendall(b"error")
        else: c.sendall(b"error")
    s.close()


if __name__ == "__main__":
    main()