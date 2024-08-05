import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtXml import *
from PyQt6.QtDBus import *

import pathlib
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #set size
        self.resize(720,540)
        #set style and title
        self.setWindowTitle("PyTextEditor")
        self.setStyle(QStyleFactory.create("Fusion"))
        #call all functions
        
        self.setup_central_widget()
        self.SetupVars()
        self.SetupMenuUI()
        self.SetupOtherUI()
        self.SetupInfoUI()

        #show app itself
        self.show()
    
    def setup_central_widget(self):
        #make central widget
        self.central_layout = QWidget()

        self.setCentralWidget(self.central_layout)
        self.centralWidget().setLayout(QVBoxLayout())

    
    #setup all variables
    def SetupVars(self):
        self.currentpath = ""
        self.current_file_name = ""
        
        self.input_text_var = ""
        
        self.words_in_text = 0
        self.chars_in_text = 0
        
        self.file_open:bool = False
        
    #setup UI menu
    def SetupMenuUI(self):
        #add settings buttons
        self.text_info_act = QAction(QIcon(),"Show Text Information",self)
        self.text_info_act.setCheckable(True)
        self.text_info_act.setChecked(True)
        self.text_info_act.triggered.connect(self.Change_Info_Visibility)
        #setup actions for exit 
        self.exitact = QAction(QIcon(),"Exit",self)#exit action
        self.exitact.setShortcut("Ctrl+Q")
        self.exitact.setStatusTip("Exit Application (Ctrl+Q)")
        self.exitact.triggered.connect(QApplication.instance().quit)
        
        #setup actions for file menu
        self.new_file_act = QAction(QIcon(),"New File",self)#new file aciton
        self.new_file_act.setStatusTip("Create New File (Ctrl+N)")
        self.new_file_act.setShortcut("Ctrl+N")
        self.new_file_act.triggered.connect(self.NewFile)
        
        self.open_file_act = QAction(QIcon(),"Open File",self)#open file action
        self.open_file_act.setStatusTip("Open A New File (Ctrl+O)")
        self.open_file_act.setShortcut("Ctrl+O")
        self.open_file_act.triggered.connect(self.OpenFile)
        
        #setup saving actions
        self.save_as_act = QAction(QIcon(),"Save as",self)#save as file action
        self.save_as_act.setStatusTip("Save a file as a new one (Ctrl+Shift+s)")
        self.save_as_act.setShortcut("Ctrl+Shift+S")
        self.save_as_act.triggered.connect(self.Save_File_As)
        
        self.save_file_act = QAction(QIcon(),"Save File",self)#save file action
        self.save_file_act.setStatusTip("Save Current File (Ctrl+S)")
        self.save_file_act.setShortcut("Ctrl+S")
        self.save_file_act.triggered.connect(self.Save_File)
        
        
        self.statusBar()#make status bar
        #add everything related to menu at end
        self.menubar = self.menuBar()
        
        self.menubar.addAction(self.exitact)
        
        self.settingMenu = self.menubar.addMenu("Settings")
        self.settingMenu.addAction(self.text_info_act)
        
        self.fileMenu = self.menubar.addMenu('File')
        self.fileMenu.addAction(self.new_file_act)
        self.fileMenu.addAction(self.open_file_act)        

        self.saveMenu = self.menubar.addMenu("Save")
        self.saveMenu.addAction(self.save_file_act)
        self.saveMenu.addAction(self.save_as_act)

    #setup UI info
    def SetupInfoUI(self):
        #create widgets
        self.info_container = QWidget()
        self.info_container.setLayout(QGridLayout())
        
        self.custom_font = QPushButton("Set Custom Font")
        self.custom_font.pressed.connect(self.Open_Font_Dialog)
        
        self.word_label = QLabel("Words:")
        self.char_label = QLabel("Chars:")
        self.info_container.setStyleSheet("""font-weight:500;font-size:12px;text-align:left""")
        #add functionality
        self.input_text.textChanged.connect(self.Change_Info_Label)
        #add to container
        self.info_container.layout().addWidget(self.word_label,0,0)
        self.info_container.layout().addWidget(self.char_label,1,0)
        
        self.centralWidget().layout().addWidget(self.info_container)
        self.centralWidget().layout().addWidget(self.custom_font)

    #setup other UI and widgets    
    def SetupOtherUI(self):
        #create objects        
        self.input_text = QPlainTextEdit()
        self.input_text.textChanged.connect(self.UpdateTextVar)
        #add everything to central widget
        self.centralWidget().layout().addWidget(self.input_text)
        
    #update text with variable
    def UpdateTextVar(self):
        self.input_text_var = self.input_text.toPlainText()
    
    #finished function - opens txt file, reads it, and updates text
    def OpenFile(self):
        self.OpenFileDialogSetPath()
        self.UpdateText(self.currentpath)
        self.file_open = True
      
    #redirect to OpenFile (set path and name variables)  
    def OpenFileDialogSetPath(self):
        fileName = QFileDialog.getOpenFileName(self,"Open Image",str(pathlib.Path.home()),"Text Files (*.txt)")
        self.currentpath = str(fileName[0])
        self.current_file_name = os.path.basename(self.currentpath)
    
    #redirect to OpenFile (updates text using path)  
    def UpdateText(self,path:str):
        txt = pathlib.Path(path).read_text()
        
        self.setWindowTitle("PyTextEditor : " + self.current_file_name)
        self.input_text.setText(txt)
    
    #finished function (make a file but dont open it)
    def NewFile(self):
        name = QFileDialog.getSaveFileName(self, 'Save File',str(pathlib.Path.home()))
        try:
            file = None
            file = open(name[0],'w')
            file.write("")
            file.close()
        except FileNotFoundError:
            print("File Dialog closed before file could be saved")

    #clear text in box
    def ClearText(self):
        self.input_text.setText("")

    #save file as new one
    def Save_File_As(self):
        if(self.input_text_var.strip() !=""):
            name = QFileDialog.getSaveFileName(self, 'Save File As',str(pathlib.Path.home()))
            file = None
            
            file = open(name[0],'w')
            path = name[0]
            
            file.write(self.input_text_var)
            

            self.file_open = True
            self.current_file_name = os.path.basename(path)
            self.currentpath = path
            self.UpdateText(path)
            
            file.close()
        else:
            self.Show_Basic_Error_Dialog("Saving Nothing to a file is not allowed")
            
    #save file
    def Save_File(self):
        if(self.file_open):
            file = open(self.currentpath,"w")
            file.write(self.input_text_var)
            file.close()
            self.setStatusTip("File Saved")
        else:
            self.Show_Basic_Error_Dialog("A file must be open to save it!")
            
    #show error
    def Show_Basic_Error_Dialog(self,message:str):
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec()
        
    def Open_Font_Dialog(self):
        self.dialog = QFontDialog(self)
        self.dialog.show()
        self.dialog.fontSelected.connect(self.setFont)
        
    def SetFont(self):
        self.input_text.setFont(self.dialog.font())
        
    #return number of chars given a string
    def Get_chars(self,str_to_count:str):
        return len(str_to_count.strip())
    
    #return number of words given a string
    def Get_words(self,str_to_count:str):
        return len(str_to_count.split())

    #use upper two functions to change text box
    def Change_Info_Label(self):
        self.chars_in_text = str(self.Get_chars(self.input_text_var))
        self.words_in_text = str(self.Get_words(self.input_text_var))
        
        self.char_label.setText("Chars: " + self.chars_in_text)
        self.word_label.setText("Words: " + self.words_in_text)

    #clear everything - constantly need updates
    def Reset_All(self):
        self.Reset_Text()
        self.Reset_File()
        self.Reset_InfoWordChar()
        
    #reset all text related things
    def Reset_Text(self):
        self.input_text.setText("")
        self.input_text_var = ""
    #reset all file related things
    def Reset_File(self):
        self.currentpath = ""
        self.current_file_name = ""
        
        self.file_open = False
    #reset info UI on word and chars
    def Reset_InfoWordChar(self):
        self.words_in_text = 0
        self.chars_in_text = 0
        
    #when pressed button hide or show info container
    def Change_Info_Visibility(self):
        print("Changed Info Container Visibility")
        if(self.text_info_act.isChecked()):
            self.info_container.show()
        else:
            self.info_container.hide()

    
app = QApplication(sys.argv)
window = MainWindow()
app.exec()
