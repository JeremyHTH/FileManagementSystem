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
        if (not os.path.exists("log")):
            os.mkdir("log")
    
        self.LogFile = open(f'log/AutoNotificationSystem.log','a')
        self.LogFile.write(f'{time.ctime()[4:]}\tStart App\n')
    
    def InitUI(self):
        
        self.Layout = QGridLayout(self)

        self.MessageFilePathLabel = QLabel("Message File Path: ",self)
        self.Layout.addWidget(self.MessageFilePathLabel,0,0,1,1)

        self.MessageFilePathLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.MessageFilePathLineEdit,0,1,1,6)

        self.SelectMessageFilePath = QPushButton("Select Path", self)
        self.SelectMessageFilePath.clicked.connect(self._UpdatePathLineEdit)
        self.Layout.addWidget(self.SelectMessageFilePath,0,7,1,1)

        self.StudentContactFilePathLabel = QLabel("Student Contact File Path: ",self)
        self.Layout.addWidget(self.StudentContactFilePathLabel,1,0,1,1)

        self.StudentContactFilePathLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.StudentContactFilePathLineEdit,1,1,1,6)

        self.SelectStudentContactFilePath = QPushButton("Select Path", self)
        self.SelectStudentContactFilePath.clicked.connect(self._UpdatePathLineEdit)
        self.Layout.addWidget(self.SelectStudentContactFilePath,1,7,1,1)

        self.TutorContactFilePathLabel = QLabel("Tutor Contact File Path: ",self)
        self.Layout.addWidget(self.TutorContactFilePathLabel,2,0,1,1)

        self.TutorContactFilePathLineEdit = QLineEdit(self)
        self.Layout.addWidget(self.TutorContactFilePathLineEdit,2,1,1,6)

        self.SelectTutorContactFilePath = QPushButton("Select Path", self)
        self.SelectTutorContactFilePath.clicked.connect(self._UpdatePathLineEdit)
        self.Layout.addWidget(self.SelectTutorContactFilePath,2,7,1,1)

        self.GenerateStudentMessageToFileButton = QPushButton("Generate student message to file", self)
        self.GenerateStudentMessageToFileButton.clicked.connect(self.GenerateStudentWhatsappMessageToFile)
        self.Layout.addWidget(self.GenerateStudentMessageToFileButton,3,0,1,2)

        self.SendStudentMessageMessageButton = QPushButton("Send Student Message", self)
        self.SendStudentMessageMessageButton.clicked.connect(self._SendStudentWhatsappMessage)
        self.Layout.addWidget(self.SendStudentMessageMessageButton,3,2,1,2)

        self.GenerateTutorMessageToFileButton = QPushButton("Generate Tutor message to file", self)
        self.GenerateTutorMessageToFileButton.clicked.connect(self.GenerateTutorWhatsappMessageToFile)
        self.Layout.addWidget(self.GenerateTutorMessageToFileButton,3,4,1,2)

        self.SendTutorMessageMessageButton = QPushButton("Send Tutor Message", self)
        self.SendTutorMessageMessageButton.clicked.connect(self._SendTutorWhatsappMessage)
        self.Layout.addWidget(self.SendTutorMessageMessageButton,3,6,1,2)

        self.setLayout(self.Layout)

    def _SendStudentWhatsappMessage(self):
        self.LogFile.write(f'{time.ctime()[4:]}\t<Start send student message>\n')
        try:

            if (not os.path.exists(self.MessageFilePathLineEdit.text())):
                QMessageBox.warning(None,"Message file does not Exist", "Please check your selected file path", QMessageBox.Ok)
                self.LogFile.write(f'{time.ctime()[4:]}\tMessage file does not exist\n')
                return
            
            if (not os.path.exists(self.StudentContactFilePathLineEdit.text())):
                QMessageBox.warning(None,"Contact file does not Exist", "Please check your selected file path", QMessageBox.Ok)
                self.LogFile.write(f'{time.ctime()[4:]}\tStudent contact file does not exist\n')
                return
            
            Data, MissedTarget = GenerateStudentMessage(self.MessageFilePathLineEdit.text(), self.StudentContactFilePathLineEdit.text())
            self.LogFile.write(f'{time.ctime()[4:]}\tGenerated student message. MissedTarget{MissedTarget}\n')

            if (not (len(MissedTarget) == 0)):
                buttonReply = QMessageBox.question(None, 'Automation System', f'{MissedTarget} is not found, proceed anyway?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel) 
                if (not buttonReply == QMessageBox.Yes):
                    QMessageBox.information(None,"Send Message","Cancelled",QMessageBox.Ok) 
                    self.LogFile.write(f'{time.ctime()[4:]}\tSend student message cancelled\n')
                    return 
                
            MissedNumber = SendMessage(Data, self.LogFile)

            if (len(MissedNumber) > 0):
                ErrorMessage = GetNameByPhoneNumber(MissedNumber, self.StudentContactFilePathLineEdit.text(),'Student')
                QMessageBox.warning(None,"Skipped Target", ErrorMessage, QMessageBox.Ok)
                
        except Exception as e:
            self.LogFile.write(f'{time.ctime()[4:]}\tSend student message failed with error\n{str(e)}\n')
            QMessageBox.warning(self,"Send student message fail",str(e),QMessageBox.Ok)

        self.LogFile.write(f'{time.ctime()[4:]}\t<End send student message>\n')

    def _SendTutorWhatsappMessage(self):
        self.LogFile.write(f'{time.ctime()[4:]}\t<Start send tutor message>\n')
        try:
            if (not os.path.exists(self.MessageFilePathLineEdit.text())):
                QMessageBox.warning(None,"Message File not Exist", "Please check your selected file path",QMessageBox.Ok)
                self.LogFile.write(f'{time.ctime()[4:]}\tMessage file does not exist\n')
                return
            
            if (not os.path.exists(self.TutorContactFilePathLineEdit.text())):
                QMessageBox.warning(None,"Contact File not Exist", "Please check your selected file path",QMessageBox.Ok)
                self.LogFile.write(f'{time.ctime()[4:]}\tTutor contact file does not exist\n')
                return
            
            Data, MissedTarget = GenerateTutorMessage(self.MessageFilePathLineEdit.text(), self.TutorContactFilePathLineEdit.text())
            self.LogFile.write(f'{time.ctime()[4:]}\tGenerated Tutor message. MissedTarget{MissedTarget}\n')

            if (not (len(MissedTarget) == 0)):
                buttonReply = QMessageBox.question(None, 'Automation System', f'{MissedTarget} is not found, proceed anyway?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel) 
                if (not buttonReply == QMessageBox.Yes):
                    QMessageBox.information(None,"Send Message","Cancelled",QMessageBox.Ok)
                    self.LogFile.write(f'{time.ctime()[4:]}\tSend tutor message cancelled\n')
                    return 
            
            MissedNumber = SendMessage(Data, self.LogFile)

            if (len(MissedNumber) > 0):
                ErrorMessage = GetNameByPhoneNumber(MissedNumber, self.TutorContactFilePathLineEdit.text(),'Tutor')
                QMessageBox.warning(None,"Skipped Target", ErrorMessage, QMessageBox.Ok)
        except Exception as e:
            self.LogFile.write(f'{time.ctime()[4:]}\tSend tutor message failed with error\n{str(e)}\n')
            QMessageBox.warning(self,"Send message fail",str(e),QMessageBox.Ok)
            
        self.LogFile.write(f'{time.ctime()[4:]}\t<End send tutor message>\n')


    def GenerateStudentWhatsappMessageToFile(self):
        try:
            if (not os.path.exists(self.MessageFilePathLineEdit.text())):
                QMessageBox.warning(None,"Message File not Exist", "Please check your selected file path",QMessageBox.Ok)
                return
            
            if (not os.path.exists(self.StudentContactFilePathLineEdit.text())):
                QMessageBox.warning(None,"Contact File not Exist", "Please check your selected file path",QMessageBox.Ok)
                return
            
            GenerateStudentMessageToFile(self.MessageFilePathLineEdit.text(), self.StudentContactFilePathLineEdit.text())
        except Exception as e:
            QMessageBox.warning(self,"Generate message fail",str(e),QMessageBox.Ok)
        else:
            QMessageBox.information(None,"Generate message","Generate message to txt done",QMessageBox.Ok)

    def GenerateTutorWhatsappMessageToFile(self):
        try:
            if (not os.path.exists(self.MessageFilePathLineEdit.text())):
                QMessageBox.warning(None,"Message File not Exist", "Please check your selected file path",QMessageBox.Ok)
                return
            
            if (not os.path.exists(self.TutorContactFilePathLineEdit.text())):
                QMessageBox.warning(None,"Contact File not Exist", "Please check your selected file path",QMessageBox.Ok)
                return
            
            GenerateTutorMessageToFile(self.MessageFilePathLineEdit.text(), self.TutorContactFilePathLineEdit.text())
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

            elif (Sender == self.SelectTutorContactFilePath):
                self.TutorContactFilePathLineEdit.setText(FilePath)


            elif (Sender == self.SelectStudentContactFilePath):
                self.StudentContactFilePathLineEdit.setText(FilePath)

    def _GetMissedTarget(Path):
        pass

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
    if os.name == 'nt':
        import ctypes
        myappid = 'EducationCentre.ControlApp.Ver1.1' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    container = MainWindow()

    container.show()
    sys.exit(app.exec_())