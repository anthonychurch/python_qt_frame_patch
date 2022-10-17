import sys
import os

import shutil

#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#from pathlib import *

#cd tools/python/Frame-Patch_01
#python qt_FramePatchApp.py

# 'C:\\Temp\\FramePatch\\RCT_089_1160\\images\\render 3d\\Light-Env\\v0424_ysw_v3update\\beauty_1224x852x1_linear'

# Global Variables
ver = "08.003"

label_01 = "Select the top directory of render layers to be patched"
label_02 = "Select the top directory of render layers that will be used to patch"

window_title = "Frame Patch Application Ver " + ver

placeholder_dir_01 = "C:/Temp/FramePatch/RCT_089_1160/images/render3d/Light-Env/v0442_ysw_cam2490v5" # "C:/Temp/FramePatch/Folder_01"
placeholder_dir_02 = "C:/Temp/FramePatch/RCT_089_1160/images/render3d/Light-Env/v0424_ysw_v3update" # "C:/Temp/FramePatch/Folder_02"

#placeholder_dir_01 = 'C:\\Temp\\FramePatch\\RCT_089_1160\\images\\render 3d\Light-Env\\v0424_ysw_v3update\'
#placeholder_dir_02 = 'C:\\Temp\\FramePatch\\RCT_089_1160\\images\\render 3d\Light-Env\\v0442_ysw_cam2490v5\'

# Declare pass variables
pass_01_ver = ''
pass_01_name = ''
pass_01_user = ''
pass_02_ver = ''
pass_02_name = ''
pass_02_user = ''

subPass_01_name = ''
subPass_01_resolution = ''
subPass_01_colourSpace = ''
subPass_02_name = ''
subPass_02_resolution = ''
subPass_02_colourSpace = ''

#common_path = None
get_all_subDir = {} # Declare empty dictiononary
sub_dir_01 = {} # Declare empty dictiononary
sub_dir_02 = {} # Declare empty dictiononary

latest_ver = ""
next_ver = ""
patch_01_ver = ""
patch_02_ver = ""

#zero_fill = 4
#next_ver_comment = "FramePatch"
#current_user = "awc"
#dir_mode = 0o777

tkn_pass_ver = ""
tkn_sep = "_"


class FramePatchGUI(QMainWindow):
	def __init__(self, parent = None):
		super(FramePatchGUI, self).__init__(parent)

		# Class Variables
		self.frame_patch_dir = ''
		"""
		# Layout Level
		# Creat Menu Bar Container
		"""
		self.main_menu = self.menuBar()

		self.file_menu = self.main_menu.addMenu("&File")
		self.act_save_log = QAction("&Save to Log File", self)
		self.file_menu.addAction(self.act_save_log)
		self.act_quit = QAction("&Quit", self)
		self.file_menu.addAction(self.act_quit)

		self.edit_menu = self.main_menu.addMenu("&Edit")
		self.act_sel_all = QAction("&Select All", self)
		self.edit_menu.addAction(self.act_sel_all)
		self.act_copy_all = QAction("&Copy All", self)
		self.edit_menu.addAction(self.act_copy_all)

		self.help_menu = self.main_menu.addMenu("&Help")

		"""
		NOTE:
		You can enter keyboard shortcuts using key names (e.g. Ctrl+p).
		Qt.namespace identifiers (e.g. Qt.CTRL + QtKey_p) or
		system agnostic identifiers (e.g. QKeySequence.Print)
		"""
		#self.button_action.setShortcut(QKeySequence("Ctrl+p"))
		#self.toolbar.addAction(self.button_action)


		"""
		# Layout Level 00
		# Define Layout Objects
		# Create Master Vertical Layout object to nest all other layouts
		"""
		self.lyt_master = QVBoxLayout()

		"""
		# LAYOUT LEVEL 01 - Vertical
		# Define main Layouts to nest Specific Dialogs and Buttons
		"""
		"""
		# Create Dialog 01 Vertical Layout object to nest Horizontal Layout that will hold Buttons and Dialog objects used to pick Directory to be patched
		"""
		self.lyt_dlg_01 = QVBoxLayout()
		"""
		# Create Dialog 02 Vertical Layout object  to nest Horizontal Layout that will hold Buttons and Dialog objects to pick Directory used for patching
		"""
		self.lyt_dlg_02 = QVBoxLayout()
		"""
		# Create Dialog Text Edit Vertical Layout object to run frame patching
		"""
		self.lyt_dlg_txt_01 = QVBoxLayout()
		"""
		# Create Dialog Text Edit Vertical Layout object to nest Buttons used to run frame patching
		"""
		self.lyt_dlg_03 = QVBoxLayout()

		"""
		# LAYOUT LEVEL 02 - Horizontal
		# Define sub Horizntal Layouts to nest Specific Dialogs and Buttons used for Directory selection
		"""
		"""
		# Create Dialog 01 Horizntal Layout object to nest Buttons and Dialog objects used to pick Directory to be patched
		"""
		self.lyt_brws_01 = QHBoxLayout()
		"""
		# Create Dialog 02 Horizntal Layout object to nest Buttons and Dialog objects used to pick Directory used for patching
		"""
		self.lyt_brws_02 = QHBoxLayout()

		"""
		# LAYOUT LEVEL 03 - Buttons and Widgets
		# Define Layout Widgets and Buttons
		"""
		"""
		# Create Widgets 01 for getting sequence to be frame patched
		"""
		self.wdg_brws_01_label = QLabel(label_01)
		self.wdg_brws_01_lneEdit = QLineEdit(placeholder_dir_01)

		"""
		# Create Widgets 02 for getting sequence to be frame patched
		"""
		self.wdg_brws_02_label = QLabel(label_02)
		self.wdg_brws_02_lneEdit = QLineEdit(placeholder_dir_02)

		"""
		# Create Button 01 used to pick Directory to be patched
		"""
		self.btn_brwse_01 = QPushButton("Browse")
		"""
		# Hook the get_dir function into the btn_brwse_01 object
		# NOTE: use the lambda function add extra arguments when connecting
		"""
		self.btn_brwse_01.clicked.connect( lambda: self.insertDir(self.wdg_brws_01_lneEdit) )

		"""
		# Create button 02 used to pick Directory used for patching
		"""
		self.btn_brwse_02 = QPushButton("Browse")
		"""
		# Hook the get_dir function into the btn_brwse_02 object
		# NOTE: use the lambda function add extra arguments when connecting
		"""
		self.btn_brwse_02.clicked.connect( lambda: self.insertDir(self.wdg_brws_02_lneEdit) )

		"""
		Create Text Edit Area
		"""
		self.wdg_txtEdit_01 = QTextEdit()
		self.wdg_txtEdit_01.setMinimumHeight(500)
		self.wdg_txtEdit_01.setPlainText("")

		"""
		# Create button 03 button to run Frame Patch application
		"""
		self.btn_runApp_03 = QPushButton("Run Frame Patch")
		self.btn_runApp_03.clicked.connect( lambda: self.runApp(self.wdg_brws_01_lneEdit, self.wdg_brws_02_lneEdit) )

		"""
		# LAYOUT LEVEL 03 - Nest Buttons and Widgets into Horizontal Layouts
		# Horizontal (browser) Layouts
		"""
		"""
		# 01
		"""
		self.lyt_brws_01.addWidget(self.wdg_brws_01_lneEdit)
		self.lyt_brws_01.addWidget(self.btn_brwse_01)
		"""
		# 02
		"""
		self.lyt_brws_02.addWidget(self.wdg_brws_02_lneEdit)
		self.lyt_brws_02.addWidget(self.btn_brwse_02)

		"""
		# LAYOUT LEVEL 04 - Nest Horizontal Layouts and Run App Button into Vetical Layouts
		# Vertical (browser) Layouts
		"""
		"""
		# 01
		"""
		self.lyt_dlg_01.addWidget(self.wdg_brws_01_label)
		"""
		# 01 - Nest layout
		"""
		self.lyt_dlg_01.addLayout(self.lyt_brws_01)
		"""
		# 02
		"""
		self.lyt_dlg_02.addWidget(self.wdg_brws_02_label)
		"""
		# 02 - Nest layout
		"""
		self.lyt_dlg_02.addLayout(self.lyt_brws_02)
		"""
		Text 01
		"""
		self.lyt_dlg_txt_01.addWidget(self.wdg_txtEdit_01)
		"""
		# 03 - Nest Run App Button
		"""
		self.lyt_dlg_03.addWidget(self.btn_runApp_03)

		"""
		# LAYOUT LEVEL 05 - Master layout
		# Nest layouts
		"""
		#self.addToolBar(self.toolbar)
		self.lyt_master.addLayout(self.lyt_dlg_01)
		self.lyt_master.addLayout(self.lyt_dlg_02)
		self.lyt_master.addLayout(self.lyt_dlg_txt_01)
		self.lyt_master.addLayout(self.lyt_dlg_03)

		"""
		# Set the Main Window Title attribute
		"""
		self.setWindowTitle(window_title)
		self.resize(600, 800)

		"""
		# Set the central widget of the Window.
		"""
		self.widget = QWidget()
		"""
		# Add Master Layout to the widget object
		"""
		self.widget.setLayout(self.lyt_master)
		self.setCentralWidget(self.widget)

	def getActionSaveLog(self):
		return self.act_save_log

	def getActionQuit(self):
		return self.act_quit

	def getActionSelectAll(self):
		return self.act_sel_all

	def getActionSaveLog(self):
		return self.act_save_log

	"""
	# Get the parent directory.
	"""
	def getCommonParentDir(self, dir_01, dir_02):
		self.dir_01 = os.path.abspath( dir_01.text() )
		self.dir_02 = os.path.abspath( dir_02.text() )
		if( os.path.abspath(os.path.join(self.dir_01,'..')) == os.path.abspath(os.path.join(self.dir_02,'..')) ):
			self.parent_dir = os.path.abspath(os.path.join(self.dir_01,'..'))

		return self.parent_dir

	def saveLogFile(self, dir_01, dir_02):
		self.today = date.today()
		self.now = datetime.now()
		self.str_today = self.today.strftime("%d-%m-%Y")
		self.str_now = self.now.strftime("%d-%m-%Y--%H:%M:%S")
		#print("Today's date:", self.str_now)
		self.this_dir = self.getCommonParentDir(dir_01, dir_02)
		#print("self.this_dir:", self.this_dir)
		self.txt_file = os.path.join(self.this_dir, 'log__' + self.str_now + '.txt')
		self.log_file = open(self.txt_file, "w+")#, "w")

	def insertText(self, widget, msg):
		content = widget.toPlainText()
		widget.setPlainText(msg)
		return widget.toPlainText()

	def insertDir(self, widget):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.DirectoryOnly)
		return_dir = None

		if dlg.exec_():
			dir_names = dlg.selectedFiles()
			return_dir = dir_names[0]
			widget.setText(return_dir)

		return return_dir

	def setDir(self, dir, widget):
		widget.setText(dir)

	def runApp(self, line_edit_01, line_edit_02):
		# Get the inputs for the directory paths
		# Get the absolute path ie; change '/' to '\'
		dir_01 = os.path.abspath( line_edit_01.text() )
		dir_02 = os.path.abspath( line_edit_02.text() )
		#print(dir_01)

		# Get the parent directory of each directory
		parent_dir_01 = os.path.abspath(os.path.join(dir_01,'..'))
		parent_dir_02 = os.path.abspath(os.path.join(dir_02,'..'))
		#print("Parent Directory = " + str(parent_dir_01))

		# Get the version directory of each shot
		ver_dir_01 = os.path.basename(dir_01)
		ver_dir_02 = os.path.basename(dir_02)
		#print("Version Directory = " + str(ver_dir_01))


def main():
	app = QApplication(sys.argv)

	# Create window using the QMainWindow. This is a pre-made widget that provides a lot standard features.
	window = FramePatchAppGUI()

	# Create a Qt Widget, which will be our window.
	window.show() # Important! Windows are hidden be default

	# Start the event loop.
	app.exec_()

# Run this if this is the master file
if __name__ == "__main__":
	main()
