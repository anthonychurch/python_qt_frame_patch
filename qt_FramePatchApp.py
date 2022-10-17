import sys
import os
import shutil

#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#from Model import FramePatchModel as fpm
from View.FramePatchGUI import FramePatchGUI
from Model.FramePatchModel import FramePatchModel

# cd c:\tools\python\Frame-Patch_01
# python qt_FramePatchApp.py



# Global Variables
ver = "02.002"

placeholder_dir_02 = "C:/Temp/FramePatch/RCT_089_1160/images/render3d/Light-Env/v0442_ysw_cam2490v5" # "C:/Temp/FramePatch/Folder_01"
placeholder_dir_01 = "C:/Temp/FramePatch/RCT_089_1160/images/render3d/Light-Env/v0424_ysw_v3update" # "C:/Temp/FramePatch/Folder_02"

current_user = "awc"

path = os.path.abspath(placeholder_dir_01 )
folder = path.split(os.sep)[-1]

ui = None


def startApp(line_edit_01, line_edit_02, user, version):
	ui = FramePatchGUI()
	ui.btn_runApp_03.clicked.connect( lambda: runApp(ui, ui.wdg_txtEdit_01, ui.wdg_brws_01_lneEdit, ui.wdg_brws_02_lneEdit, user) )

	act_save_log = ui.getActionSaveLog()
	act_save_log.triggered.connect(lambda:  ui.saveLogFile(ui.wdg_brws_01_lneEdit,ui.wdg_brws_02_lneEdit))

	act_quit = ui.getActionQuit()
	act_quit.triggered.connect(lambda:  closeApplication())

	act_sel_all = ui.getActionSelectAll()
	act_sel_all.triggered.connect(lambda:  ui.wdg_txtEdit_01.selectAll())

	act_copy_all = ui.getActionSelectAll()
	act_copy_all.triggered.connect(lambda:  ui.wdg_txtEdit_01.copy())

	return ui


def runApp(gui, text_edit_01, line_edit_01, line_edit_02, user):
	fp = FramePatchModel(line_edit_01,line_edit_02, user)

	# Create variable to store information on the frame patch sequences
	copied_frames = None

	# If the Key for Dictionary object checks is equal to True, the Value will
	# be a list of sub directories to be copied.
	checks = fp.runChecks()
	#print("qt_FramePatchApp :: checks : ",checks)

	"""
	Intialise variable to hold feedback information from the fp.runChecks() functions
	to be rendered in the QT interface.
	"""
	c = text_edit_01.toPlainText()

	#print("qt_FramePatchApp :: RunApp :: list(checks.keys())[0]", list(checks.keys())[0])
	#print("qt_FramePatchApp :: RunApp :: list(checks.values())", list(checks.values()))
	# If check key value is True, log data and proceed with frame patching process
	if list(checks.keys())[0]:
		t = "### STARTING FRAME PATCHING OPERATION ###\n\n"
		t += c + "\n\nSub Directories that will be frame patched:\n"
		for a in list(checks.values())[0]:
			t += a + "\n"

		gui.insertText(text_edit_01, t)

		# Create frame patch directory and sets self.frame_patch_dir in FramePatchModel Class
		frame_patch_dir = fp.createDirNextVer()
		fp.setFramePatchDirectory(frame_patch_dir)
		t += "\n\nCreating new frame patch directory : \n" + frame_patch_dir + "\n"
		gui.insertText(text_edit_01, t)

		# Create sub Direcotories
		check_sub_dir = True
		t +=  "\n\nCreating sub directories : \n"
		for s in list(checks.values())[0]:
			#print("qt_FramePatchApp :: RunApp :: s", s)
			created_sub_dir = fp.createSubDirectory(frame_patch_dir,s)
			#print("qt_FramePatchApp :: RunApp :: created_sub_dir ",created_sub_dir)
			if created_sub_dir == None:
				t += "Failed to create : " + str(s) + "\n. Terminating loop\n"
				check_sub_dir = False
				break
			else:
				t += str(created_sub_dir) + "\n"

		gui.insertText(text_edit_01, t)

		if check_sub_dir:
			# Set the self.sub_dirs variable in FramePatchModel Class
			fp.setSubDirectories(list(checks.values())[0])

			# Copy Files from
			dir_to_patch = fp.getDirToBePatched()
			dir_use_to_patch = fp.getDirUsedToPatch()
			sub_dirs = list(checks.values())[0]
			print("\n\n\n qt_FramePatchApp :: RunApp ::sub_dirs ",sub_dirs)
			copied_frames = fp.copyFiles(dir_to_patch, dir_use_to_patch, frame_patch_dir, sub_dirs)

			t +=  "\n\nCopied the following frames : \n"

			for d in list(copied_frames.keys()):
				t +=  "\n" + str(d) + " ::\n\n"
				for f in copied_frames[d]:
					t +=  str(f) + "\n"

				t += "-----------------------------------------------\n\n"

			t += "\n### ENDING FRAME PATCH OPERATION ###\n"

			gui.insertText(text_edit_01, t)
	else:
		t = c + "\n"
		for a in list(checks.values()):
			t += a + "\n"
		gui.insertText(text_edit_01, t)


def closeApplication():
	sys.exit()


def main():
	app = QApplication(sys.argv)

	"""
	Create window using the QMainWindow. This is a pre-made widget that provides a lot standard features.
	"""
	window = startApp(placeholder_dir_01, placeholder_dir_02, current_user, ver)

	"""
	Create a Qt Widget, which will be our window.
	Important! Windows are hidden be default.
	"""
	window.show()

	"""
	Start the event loop.
	"""
	sys.exit(app.exec_())


"""
Run this if this is the master file
"""
if __name__ == "__main__":
	main()
