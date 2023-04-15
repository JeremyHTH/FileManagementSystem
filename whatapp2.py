import pywhatkit
import pandas as pd
import time
import threading

# pywhatkit.sendwhatmsg_instantly("+85251128414",'testing',8,True)
# pywhatkit.sendwhatmsg_instantly("+85267601258",'testing2',8,True)

data = pd.read_excel("C:\Data_Script\sheet1.xlsx")
data = data.to_dict()
keys = list(data.keys())
message = '''
Hi {}

Time: {}
Message: {}

This message is sent by Seed In Education Centre automation system.'''
for i in range(len(data[keys[0]])):
    print(message.format(
    data[keys[3]][i],
    data[keys[5]][i],
    data[keys[6]][i]))
    tel = "+852"+ str(data[keys[4]][i])
    pywhatkit.sendwhatmsg_instantly(tel,             
                                    message.format(data[keys[3]][i], data[keys[5]][i], data[keys[6]][i]),
                                    5,
                                    True)

# print(data.keys())

