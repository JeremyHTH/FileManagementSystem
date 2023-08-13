import sys,time,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtGui
import subprocess
import platform

# Send Message 
# from SendMessage import SendMessage
# from GenerateMessage import GenerateMessageToFile
from AutoMessageSystem import *

from FileBrowserSystem import *

class ServerControlWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()
        self.Handler = None 
        if (not os.path.exists("log")):
            os.mkdir("log")
    
        self.OutFile = open(f'log/Outfile{time.ctime()[3:].replace(" ","_").replace(":","_")}.log','a')
        self.OutFile.write("Start")
    
    def InitUI(self):
        
        self.Layout = QGridLayout(self)
        self.UIName_Label = QLabel("Start UI", self)
        self.Layout.addWidget(self.UIName_Label,0,0,1,1)

        self.UIStart_Button = QPushButton("Start",self)
        self.UIStart_Button.clicked.connect(self.StartServer)
        self.Layout.addWidget(self.UIStart_Button,0,1,1,1)
        
        self.UITerminate_Button = QPushButton("Terminate",self)
        self.UITerminate_Button.clicked.connect(self.TerminateServer)
        self.UITerminate_Button.setEnabled(False)
        self.Layout.addWidget(self.UITerminate_Button,0,2,1,1)

        self.ServerStatus = QLineEdit("OFF",self)
        self.ServerStatus.setEnabled(False)
        self.ServerStatus.setProperty("class","status")
        self.ServerStatus.setProperty("state", "OFF")
        # sizePolicy = QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred)   
        # self.ServerStatus.setSizePolicy(sizePolicy)
        self.ServerStatus.setMaximumWidth(150)
        self.Layout.addWidget(self.ServerStatus,0,3,1,1)


        self.addSubject_button = QPushButton("add Subject", self)
        self.addSubject_button.clicked.connect(self._AddSubject)
        self.Layout.addWidget(self.addSubject_button,1,0,1,2)

        self.addUser_button = QPushButton('add User', self)
        self.addUser_button.clicked.connect(self._AddUser)
        self.Layout.addWidget(self.addUser_button, 1,2,1,2)

        self.setLayout(self.Layout)

    def StartServer(self):
        if (self.Handler):
            self.Handler.terminate()
            self.OutFile.close()
            self.OutFile = None
        if (self.OutFile == None):
            self.OutFile = open(f'log/Outfile{time.ctime()[3:].replace(" ","_").replace(":","_")}.log','a')
        if (platform.system() == 'Windows'):
            ProcessName = "StartServer.bat"
        else:
            ProcessName += './StartServer.bash'
        print(ProcessName)
        try:
            self.Handler = subprocess.Popen(ProcessName, stdout = self.OutFile)
        except Exception as e:
            print(e)
        else:
            
            self.ServerStatus.setText("ON")
            self.ServerStatus.setProperty("state","ON")
            self.ServerStatus.style().polish(self.ServerStatus)
            self.UIStart_Button.setEnabled(False)
            self.UITerminate_Button.setEnabled(True)

    def TerminateServer(self):
        if (self.Handler):
            self.Handler.kill()
            self.Handler = None
            self.ServerStatus.setText("OFF")
            self.ServerStatus.setProperty("state","OFF")
            self.ServerStatus.style().polish(self.ServerStatus)
            self.UIStart_Button.setEnabled(True)
            self.UITerminate_Button.setEnabled(False)
            self.OutFile.close()
            self.OutFile = None
            os.system(f'taskkill /IM "filebrowser.exe" /F')

    def close(self) -> bool:
        self.TerminateServer()
        self.OutFile.close()
        return super().close()
    

    def _AddSubject(self):
        self.SubWindow = AddSubjectWidget()
        self.SubWindow.show()

    def _AddUser(self):
        self.SubWindow = AddUserWidget()
        self.SubWindow.show()

# class UserControlWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.init_UI()
    
#     def init_UI(self):
        
#         self.Layout = QGridLayout(self)

#         self.add_button = QPushButton("add Subject", self)
#         self.add_button.clicked.connect(self._AddSubject)
#         self.Layout.addWidget(self.add_button,0,0,1,2)
#         self.setLayout(self.Layout)

#     def _AddSubject(self):
#         for button in self.CheckBoxList:
#             if (button.isChecked()):
#                 print(button.text())
            

class AutoNotificationSystemWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()
    
    def InitUI(self):
        
        self.Layout = QGridLayout(self)

        self.MessageFilePathLabel = QLabel("Message File Path: ",self)
        self.Layout.addWidget(self.MessageFilePathLabel,0,0,1,1)

        self.MessageFilePathLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.MessageFilePathLineEdit,0,1,1,5)

        self.SelectMessageFilePath = QPushButton("Select Path", self)
        self.SelectMessageFilePath.clicked.connect(self._UpdatePathLineEdit)
        self.Layout.addWidget(self.SelectMessageFilePath,0,6,1,1)

        self.ContactFilePathLabel = QLabel("Contact File Path: ",self)
        self.Layout.addWidget(self.ContactFilePathLabel,1,0,1,1)

        self.ContactFilePathLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.ContactFilePathLineEdit,1,1,1,5)

        self.SelectContactFilePath = QPushButton("Select Path", self)
        self.SelectContactFilePath.clicked.connect(self._UpdatePathLineEdit)
        self.Layout.addWidget(self.SelectContactFilePath,1,6,1,1)

        self.GenerateMessageToFile_Button = QPushButton("Generate message to file", self)
        self.GenerateMessageToFile_Button.clicked.connect(self._GenerateMessageToFile)
        self.Layout.addWidget(self.GenerateMessageToFile_Button,2,0,1,2)

        self.SendMessageButton = QPushButton("Send Message", self)
        self.SendMessageButton.clicked.connect(self._SendWhatsappMessage)
        self.Layout.addWidget(self.SendMessageButton,2,2,1,2)


        self.setLayout(self.Layout)

    def _SendWhatsappMessage(self):
        try:
            SendMessage(self.MessageFilePathLineEdit.text(), self.ContactFilePathLineEdit.text())
        except Exception as e:
            QMessageBox.warning(self,"Send message fail",str(e),QMessageBox.Ok)

    def _GenerateMessageToFile(self):
        try:
            GenerateMessageToFile(self.MessageFilePathLineEdit.text(), self.ContactFilePathLineEdit.text())
        except Exception as e:
            QMessageBox.warning(self,"Generate message fail",str(e),QMessageBox.Ok)
        else:
            QMessageBox.information(None,"Generate message","Generate message to txt done",QMessageBox.Ok)


    def _UpdatePathLineEdit(self):
        FilePath, _ = QFileDialog.getOpenFileName(None, 'Open File', 'Student_Data', 'Excel Files (*.xlsx)')
        
        if (FilePath):
            Sender = self.sender()
            
            if (Sender == self.SelectMessageFilePath):
                self.MessageFilePathLineEdit.setText(FilePath)

            elif (Sender == self.SelectContactFilePath):
                self.ContactFilePathLineEdit.setText(FilePath)

class CenterWidget(QWidget):
    def __init__(self):
        super().__init__()

        if (not os.path.exists("log")):
            os.mkdir("log")

        if (not os.path.exists("Student_Data")):
                    os.mkdir("Student_Data")

        self.InitUI()
        

    def InitUI(self):
        self.Layout = QGridLayout(self)

        #First Row (Server)
        self.FirstRow = ServerControlWidget()
        self.FirstRow.setProperty("class","OddLine")
        self.Layout.addWidget(self.FirstRow,0,0,1,1)

        # self.SecondRow = UserControlWidget()
        # self.layout.addWidget(self.SecondRow,1,0,1,1)

        self.ThirdRow = AutoNotificationSystemWidget()
        self.ThirdRow.setProperty("class","OddLine")
        self.Layout.addWidget(self.ThirdRow,3,0,2,1)

        self.setLayout(self.Layout)
    
    def close(self) -> bool:
        self.FirstRow.close()
        return super().close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.CenterWid = CenterWidget()
        self.setGeometry(1000,300,800,600)
        self.setWindowTitle("Control Center")
        self.setCentralWidget(self.CenterWid)
        self.status = QStatusBar(self)
        self.status.showMessage("Welcome")
        self.setStatusBar(self.status)

        self.setWindowIcon(QtGui.QIcon("Image\logo.png"))
        self.setStyle(QStyleFactory.create('fusion'))
        self.setStyleSheet(self.LoadStyle())

    def LoadStyle(self):
        Data = ""
        try:
            with open('Sytle.css','r') as f: 
                Data = f.read()
        except Exception as e:
            print(e.args)
            # QMessageBox.question(self,'Error',str(e))
        return Data
    
    def close(self) -> bool:
        self.CenterWid.close()
        return super().close()

if __name__ == '__main__':
    import ctypes
    myappid = 'EducationCentre.ControlApp.Ver1.5' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    container = MainWindow()

    container.show()
    sys.exit(app.exec_())