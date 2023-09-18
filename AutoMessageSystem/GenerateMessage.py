from ast import Lambda, Raise
from logging import raiseExceptions
import pandas 
import numpy as np
import time
import re
import os, sys

def GenerateStudentMessage(MessageFilePath, StudentContactFilePath):

    Message_df = pandas.read_excel(MessageFilePath, engine='openpyxl')
    
    StudentContact_df = pandas.read_excel(StudentContactFilePath, engine='openpyxl')


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

        for Index2, Name2 in enumerate(StudentContact_df['姓名(中文)']):
            if (Name1 == Name2):
                Search = re.findall(r'\d+', str(StudentContact_df['首要聯絡人'][Index2]))
                PhoneNum1 = Search[0] if len(Search) > 0 else ''
                Search = re.findall(r'\d+', str(StudentContact_df['次要聯絡人'][Index2]))
                PhoneNum2 = Search[0] if len(Search) > 0 else ''
                Search = re.findall(r'\d+', str(StudentContact_df['其他聯絡人(1)'][Index2]))
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
            message += f'{line}'
            
    MessageSet = []
    for line in ProcessedData: 
        if (not isinstance(line[1], str)):
            continue    #May need better error handling later
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
        MessageSet.append([line[3],message.format( line[0], 
                                                    str(line[2])[:10],
                                                    Detail[0], 
                                                    Detail[1],
                                                    Detail[2], 
                                                    Detail[3],
                                                    Remark1,
                                                    Remark2).split('\n') ])
    print(MessageSet)
    return MessageSet, NotFoundName

def GenerateTutorMessage(MessageFilePath, TutorContactFilePath):

    Message_df = pandas.read_excel(MessageFilePath, engine='openpyxl')
    
    TutorContact_df = pandas.read_excel(TutorContactFilePath, engine='openpyxl')

    MessageSet = []
    NotFoundName = []
    SpamData = {}

    for Index, Detail in enumerate(Message_df['Detail']):
        if (not isinstance(Detail, str)):
            continue    #May need better error handling later
        Line = Detail.split('_')
        if (len(Line) < 4):
            continue    #May need better error handling later
        
        Time, TutorName, CourseName, Room, *_ = Line
        if (not TutorName in SpamData):
            SpamData[TutorName] = {}

        CurrentStudentName = re.findall(r'[\u4e00-\u9fff]+', Message_df['Name'][Index])[0]
        if (not Time in SpamData[TutorName]):
            SpamData[TutorName][Time] = {   'CourseName': [CourseName],
                                            'Room': Room, 
                                            'Date': str(Message_df['Date'][Index])[:10], 
                                            'StudentList':[CurrentStudentName]}
        else:
            SpamData[TutorName][Time]['StudentList'].append(CurrentStudentName)
            if (not CourseName in SpamData[TutorName][Time]['CourseName']):
                SpamData[TutorName][Time]['CourseName'].append(CourseName)
        # Name = Line[1]
        # CourseTitle = '    ' + Line[0] + ' -> ' + Line[2] + '\n'
        # if (not Name in SpamData):
        #     SpamData[Name] = CourseTitle
        # else:
        #     if (not CourseTitle in SpamData[Name]):
        #         SpamData[Name] += CourseTitle

    # print(SpamData)


    Message = ""
    with open("Student_Data\TutorMessage.txt", 'r', encoding="utf-8") as f:
        SpamMessage = f.readlines()
        for line in SpamMessage:
            Message += line

    for TutorName, DataSet in SpamData.items():
        # print(TutorContact_df[TutorContact_df['NickName']=='Ms曾'])
        # print('4',TutorContact_df[TutorContact_df['NickName']=='Ms曾']['PhoneNum'].values[0])
        SearchResult = TutorContact_df[TutorContact_df['NickName'] == TutorName]
        print(DataSet)
        if (len(SearchResult) > 0):
            Data = ''
            for Time, ClassDetail in DataSet.items():
                print(Time, ClassDetail)
                Data += f'    日期:{ClassDetail["Date"]}\n'
                Data += f'    時間:{Time}\n'
                ClassTitle = ''
                for Title in ClassDetail['CourseName']:
                    ClassTitle += Title + ','
                Data += f'    課堂:{ClassTitle}\n'
                Data += f'    課室:{ClassDetail["Room"]}\n'
                Students = ''
                for Student in ClassDetail['StudentList']:
                    Students += Student + ','
                Data += f'    學生列表:{Students}\n'
                Data += '    ========================\n'

            MessageSet.append([SearchResult['PhoneNum'].values[0], Message.format(SearchResult['NickName'].values[0], Data).split('\n')])
        else:
            NotFoundName.append(TutorName)

    return MessageSet, NotFoundName

def GenerateStudentMessageToFile(MessageFilePath= "", ContactFilePath=""):
    Datum, NotFoundData = GenerateStudentMessage(MessageFilePath, ContactFilePath)
    if not os.path.exists('log'):
        os.mkdir('log')
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


def GenerateTutorMessageToFile(MessageFilePath= "", ContactFilePath=""):
    Datum, NotFoundData = GenerateTutorMessage(MessageFilePath, ContactFilePath)
    if not os.path.exists('log'):
        os.mkdir('log')

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