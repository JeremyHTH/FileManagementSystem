import pandas 
import numpy as np
import time
import re

def Generate_Message(MessageFilePath, ContactFilePath):

    Message_df = pandas.read_excel(MessageFilePath, engine='openpyxl')
    
    Contact_df = pandas.read_excel(ContactFilePath, engine='openpyxl')


    # Merge_List = Merge_df.values.tolist()

    # print(Merge_List)

    ProcessedData = []
    NotFoundName = []
    # for line in Merge_List:
    #     temp = []
    #     for item in lin, end=" ")
    #         if (not (ie:
    #         print(itemtem.isnull())):
    #             temp.append(item)
    #     print("")
    #     Processed_Data.append(temp)

    for index1, name1 in enumerate(Message_df['Name']):
        found = False
        try:
            name1 = re.findall(r'[\u4e00-\u9fff]+', name1)[0]
        except:
            pass

        for index2, name2 in enumerate(Contact_df['姓名(中文)']):
            if (name1 == name2):
                ProcessedData.append([ name2, 
                                        Message_df['Detail'][index1], 
                                        Message_df['Date'][index1],
                                        Contact_df['首要聯絡人'][index2],
                                        Contact_df['次要聯絡人'][index2],
                                        Contact_df['其他聯絡人(1)'][index2]])
                found = True
        if (not found):
            NotFoundName.append(name1)

    print(ProcessedData)
    print("===============")
    print(NotFoundName)

    message = r'''《閣下明天的補習通知》
致{}同學及家長,
    日期: {}
    時間: {}
    導師: {}
    課堂: {}
    課室: {}
    {}{}
此訊息為思研教育中心系統自動發出。
如不想再接收有關訊息，請於辦公時間與我們聯繫。
'''
    Message_Set = []
    for line in ProcessedData: 
        Detail = line[1].split("_")

        if (len(Detail) > 4 and Detail[4] == '(XXX)'):
            continue
        Remark1 = ""
        Remark2 = ""

        if (len(Detail) > 4):
            Remark1 = f"備註 1 : {Detail[4]}\n"
        
        if (len(Detail) > 5):
            Remark2 = f"備註 2 : {Detail[5]}\n"

        # print(message.format( line[0], Detail[0], Detail[1] + Detail[2], Detail[3]))
        Message_Set.append([line[3],message.format( line[0], 
                                                    str(line[2])[:10],
                                                    Detail[0], 
                                                    Detail[1],
                                                    Detail[2], 
                                                    Detail[3],
                                                    Remark1,
                                                    Remark2).split('\n') ])
    
    return Message_Set, NotFoundName

def GenerateMessageToFile(MessageFilePath= "", ContactFilePath=""):
    Datum, NotFoundData = Generate_Message(MessageFilePath, ContactFilePath)

    with open(f'log\\Generate_Message_{time.ctime()[3:].replace(" ","_").replace(":","_")}.txt', 'a', encoding='utf-8') as f:
        for Data in Datum:
            f.write(f"{Data[0]}\n")
            for line in Data[1]:
                f.write(f"{line}\n")
            f.write("\n")
        f.write("=======================================================\n")
        f.write("Not Found: \n")
        for name in NotFoundData:
            f.write(f'{name}\n')
