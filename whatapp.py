import pywhatkit
import pandas as pd
import time
import threading

timing  = time.localtime()
h = timing.tm_hour
m = timing.tm_min
print(f'{h} : {m}')
if (m != 59):
    m += 1
else:
    m = 0
    h += 1

t1 = threading.Thread(target=pywhatkit.sendwhatmsg_instantly,args=("+85251128414",'testing'))
t2 = threading.Thread(target=pywhatkit.sendwhatmsg_instantly,args=("+85267601258",'testing2',h,m))
# pywhatkit.sendwhatmsg("+85251128414",'testing',h,m)
# pywhatkit.sendwhatmsg("+852",'testing message',h,m)
t1.start()
t2.start()
while t1.is_alive() or t2.is_alive():
    time.sleep(10)

t1.join()