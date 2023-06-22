import pandas 
import numpy as np
def Generate_Message():
    Message_df = pandas.read_excel(r"C:\Users\jerem\Desktop\Seedin\FileManagementSystem\Student_Data\Sample_Time_Table_Privite.xlsx", engine='openpyxl')

    Contact_df = pandas.read_excel(r"C:\Users\jerem\Desktop\Seedin\FileManagementSystem\Student_Data\WTS_Contact_Privite.xlsx", engine='openpyxl')

    print(Message_df)
    print(Contact_df)


    # Merge_List = Merge_df.values.tolist()

    # print(Merge_List)

    Processed_Data = []

    # for line in Merge_List:
    #     temp = []
    #     for item in line:
    #         print(item, end=" ")
    #         if (not (item.isnull())):
    #             temp.append(item)
    #     print("")
    #     Processed_Data.append(temp)

    for index1, name1 in enumerate(Message_df['Name']):
        for index2, name2 in enumerate(Contact_df['姓名(中文)']):

            if (name1 == name2):
                Processed_Data.append([ name1, 
                                        Message_df['Detail'][index1], 
                                        Contact_df['手提電話'][index2],
                                        Contact_df['手提電話(母親)'][index2],
                                        Contact_df['手提電話(父親)'][index2]])

    print(Processed_Data)

    message = '''Hi {}

    Time: {}
    Message: {}
    Table: {}

    This message is sent by Seed In Education Centre automation system.'''

    Message_Set = []
    for line in Processed_Data: 
        Detail = line[1].split(" ")

        # print(message.format( line[0], Detail[0], Detail[1] + Detail[2], Detail[3]))
        Message_Set.append([line[2],message.format( line[0], Detail[0], Detail[1] + Detail[2], Detail[3]).split('\n') ])
    
    return Message_Set
if __name__ == '__main__':  
    print(Generate_Message()) 