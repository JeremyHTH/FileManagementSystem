from PyQt5.QtWidgets import *
import sys
from subprocess import check_output
class AddSubjectWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 300, 400, 300)
        self.setWindowTitle("Add Subject")
        self.init_UI()
    
    def init_UI(self):
        
        self.Layout = QGridLayout(self)

        self.CheckBoxList = []

        Index = 0
        try: 
            with open("Student_Data/directory.csv","r",encoding="utf-8") as f:
                raw_data = f.readlines()
                
                for name in raw_data:
                    c = QCheckBox(name[1:-1],self)
                    self.Layout.addWidget(c,Index//4,Index%4)
                    self.CheckBoxList.append(c)
                    Index += 1
        except Exception as e:
            print("Exception : \n")
            print(e.args)     

        self._GetServerUserName()
        self.UserNameLabel = QLabel("User :")
        self.Layout.addWidget(self.UserNameLabel, Index//4 + 1, 0, 1, 1)
        self.UserNameCombobox = QComboBox(self)
        self.UserNameCombobox.addItems(self.UserNameDict.keys())
        self.Layout.addWidget(self.UserNameCombobox, Index//4 + 1, 1, 1, 3)


        self.add_button = QPushButton("Add subject", self)
        self.add_button.clicked.connect(self._AddToSystem)
        self.Layout.addWidget(self.add_button, Index//4 + 2, 0, 1, 2)

        self.add_button = QPushButton("Add user", self)
        self.add_button.clicked.connect(self._GetServerUserName)
        self.Layout.addWidget(self.add_button, Index//4 + 2, 2, 1, 2)

        self.setLayout(self.Layout)

    def _AddToSystem(self):
        # print(self.UserNameCombobox.currentText())
        TargetIndex = self.UserNameDict[self.UserNameCombobox.currentText()]
        
        OriginalSubject = []
        command = f'cd C:\\Resources_Database && filebrowser rules ls -i {1}'
        Data = check_output(command.split(), shell= True).decode().split("\n")
        for index, line in enumerate(Data):
            if (index < 2):
                continue
            OriginalSubject.append(line[line.find('\t') + 1:])
        
        print(OriginalSubject)
        for button in self.CheckBoxList:
            if (button.isChecked()):
                # TargetSubject.append(button.text())
                # print(button.text())
                if(not (button.text() in OriginalSubject)):
                    command = f'cd C:\\Resources_Database && filebrowser rules add {button.text()} -a -i {TargetIndex}'   
                    print(command)
    
    def _GetServerUserName(self):
        command = f'cd C:\\Resources_Database && filebrowser users ls'
        data = check_output(command.split(), shell = True)
        data = data.decode().split('\n')
        data = list(map(lambda a : a.split(), data))
        self.UserNameDict = {}
        for index, line in enumerate(data):
            if (index == 0):
                continue
            if (len(line) < 2): 
                break
            self.UserNameDict[line[1]] = line[0]
        # print(self.UserNameDict)

class AddUserWidget(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setGeometry(1000, 300, 400, 300)
        self.setWindowTitle("Add User")
        self.InitUI()
    def InitUI(self):
        self.Layout = QGridLayout()
        
        self.UserNameLabel = QLabel("User Name :", self)
        self.Layout.addWidget(self.UserNameLabel, 0, 0, 1, 1)

        self.UserNameLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.UserNameLineEdit, 0, 1, 1, 3)

        self.PasswordLabel = QLabel("Password :", self)
        self.Layout.addWidget(self.PasswordLabel, 1, 0, 1, 1)

        self.PasswordLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.PasswordLineEdit, 1, 1, 1, 3)

        self.AddUserButton = QPushButton("Add user name", self)
        self.AddUserButton.clicked.connect(self._AddUser)
        self.Layout.addWidget(self.AddUserButton, 2, 0, 1, 4)

        self.setLayout(self.Layout)

    def _AddUser(self):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    container = AddSubjectWidget()
    container.show()
    
    container2 = AddUserWidget()
    container2.show()
    sys.exit(app.exec_())