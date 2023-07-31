from PyQt5.QtWidgets import *
import sys
class AddSubjectWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_UI()
    
    def init_UI(self):
        
        self.Layout = QGridLayout(self)

        self.CheckBoxList = []

        # self.ChineseBox = QCheckBox("Chinese",self)
        # self.EnglishBox = QCheckBox("English",self)
        # self.MathBox = QCheckBox("Math",self)
        # self.OthersBox = QCheckBox("Other",self)
        
        index = 0
        try: 
            with open("Student_Data/directory.csv","r",encoding="utf-8") as f:
                raw_data = f.readlines()
                
                for name in raw_data:
                    c = QCheckBox(name[1:-1],self)
                    self.Layout.addWidget(c,index//4,index%4)
                    self.CheckBoxList.append(c)
                    index += 1
        except Exception as e:
            print("Exception : \n")
            print(e.args)     

        print(len(self.CheckBoxList))

        self.add_button = QPushButton("add Subject", self)
        self.add_button.clicked.connect(self._AddToSystem)
        self.Layout.addWidget(self.add_button, index//4 + 1, 0, 1, 2)

        self.setLayout(self.Layout)

    def _AddToSystem(self):
        for button in self.CheckBoxList:
            if (button.isChecked()):
                print(button.text())    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    container = AddSubjectWidget()

    container.show()
    sys.exit(app.exec_())