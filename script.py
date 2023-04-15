import os
import pandas as pd
import csv
def test():

    
    UserId = 4
    data = None
    with open("directory.seedin","r",encoding="utf-8") as f:
        data = f.readlines()
    
    data = list(map(lambda x : x.split('\n')[0],data))

    
    target = {12}

    # for i in target:
    #     command = f'cd C:\\Resources_Database && filebrowser rules add {data[5]} -a -i {i}'
    #     print(command)
    #     os.system(command)
    for i in data:
        command = f'cd C:\\Resources_Database && filebrowser rules add {i} -a -i {29}'
        print(command)
        os.system(command)

def addNew():
    data = pd.read_excel("C:\Data_Script\\tutor_filing_code.xlsx")
    data2 = data.to_dict()
    namelist = data2['Name']
    pw = data2['PW']
    
    for key , value in namelist.items():
        name = value.split()
        name = name[1][0] + name[2][0] + name[0]
        namelist[key] = name
    # for i in range(len(namelist)):
    #     command = f'cd C:\\Resources_Database && filebrowser users add {namelist[i]} {pw[i]}'
    #     print(command)
    #     os.system(command)
        
    with open("PW.csv",'a',newline="") as f:
        writer = csv.writer(f)
        for i in range (len(namelist)):
            a = [namelist[i],pw[i]]
            print(a)
            writer.writerow(a)
        
    # for key, value in namelist.items():
    #     print(key, value)
    # for key, value in pw.items():
    #     print(key, value)
    # print(namelist)

if __name__ == '__main__':
    addNew()