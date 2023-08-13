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

    for Index1, Name1 in enumerate(Message_df['Name']):
        found = False
        try:
            Name1 = re.findall(r'[\u4e00-\u9fff]+', Name1)[0]
        except:
            pass

        for Index2, Name2 in enumerate(Contact_df['姓名(中文)']):
            if (Name1 == Name2):
                Search = re.findall(r'\d+', str(Contact_df['首要聯絡人'][Index2]))
                PhoneNum1 = Search[0] if len(Search) > 0 else ''
                Search = re.findall(r'\d+', str(Contact_df['次要聯絡人'][Index2]))
                PhoneNum2 = Search[0] if len(Search) > 0 else ''
                Search = re.findall(r'\d+', str(Contact_df['其他聯絡人(1)'][Index2]))
                PhoneNum3 = Search[0] if len(Search) > 0 else ''
                if (PhoneNum1 != '' or PhoneNum2 != '' or PhoneNum3 != ''):
                    ProcessedData.append([ Name2, 
                                            Message_df['Detail'][Index1], 
                                            Message_df['Date'][Index1],
                                            PhoneNum1,
                                            PhoneNum2,
                                            PhoneNum3])
                    found = True
                    break
        if (not found):
            NotFoundName.append(Name1)

    # print(ProcessedData)
    # print("===============")
    # print(NotFoundName)

    message = ""
    with open("Student_Data\StudentMessage.txt", 'r', encoding="utf-8") as f:
        SpanMessage = f.readlines()
        for line in SpanMessage:
            message += f'{line}\n'
            
    Message_Set = []
    for line in ProcessedData: 
        Detail = line[1].split("_")

        # if (len(Detail) > 4 and Detail[4] == '(XXX)'):
        #     continue
        skip = False
        for i in range(4,len(Detail)):
            Search = re.findall(r'\([x|X]{3}\)', Detail[i])
            if (len(Search) > 0):
                skip = True
                break
        if (skip):
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
