import sys
import os

import shutil
import collections

from datetime import date

# Global Variables
ver = "04.003"

class FramePatchModel:
	# Class Constructor
	def __init__(self, dir_01, dir_02, user):
		# Get the inputs for the directory paths.
		# Get the absolute path ie; change '/' to '\'.
		self.dir_01 = os.path.abspath( dir_01.text() )
		self.dir_02 = os.path.abspath( dir_02.text() )

		self.drive_01, self.path_01 = os.path.splitdrive(self.dir_01)
		self.drive_02, self.path_02 = os.path.splitdrive(self.dir_02)

		self.parent_dir = os.path.abspath(os.path.join(self.path_01,'..'))

		self.sub_dirs = None

		self.frame_patch_dir = None

		self.user = user

		self.next_ver_comnt_prfx = "FramePatchFrom-"
		self.next_ver_comnt_brdg = "-to-"
		self.next_ver = None

		self.tkn_sep = "_"

		self.dir_mode = 0o777

		self.pad = 4



	"""
	@Description :
	Get a list of directories that contain all of the versions of the Render Layer.
	This Method will return a nested dictionary, EXAMPLE : [{'

	@Parameters :
	String : dir

	@Result :
	String : Current directory name
	"""
	def getAllSubDir(self, dir):
		"""
		Declare empty dictiononary
		"""
		get_all_subDir = {}
		"""
		Create Key Value dictionary where the each sub directory has key terms (version, user, comment)
		seperated by "_" chracter. EXAMPLE "v0333_ysw_updateAll".
		When each sub directory name is separated, the first item (version) will be used as the Key and
		the actual full name of the directory will be the value EXAMPLE : [{"v0333" : "v0333_ysw_updateAll"}]
		"""
		for i in os.listdir(dir):
			get_all_subDir[i.split(self.tkn_sep)[0]] = i
		"""
		Return an ordered version of get_all_subDir. This ensure the highest value is last.
		"""
		return sorted(get_all_subDir.items())



	"""
	@Description :
	Get the parent directory.

	@Parameters :
	None

	@Result :
	String : Current directory name
	"""
	def getCommonParentDir(self):
		if( os.path.abspath(os.path.join(self.dir_01,'..')) == os.path.abspath(os.path.join(self.dir_02,'..')) ):
			self.parent_dir = os.path.abspath(os.path.join(self.dir_01,'..'))

		return self.parent_dir


	"""
	@Description :
	Returns the name of current directory from a path
	Takes a path, ensures that it is absolute (correct 'slash' covention for the Operating System),
	then splits the String representation of the path in an array and returns the last element of
	that array.

	@Parameters :
	String : Path

	@Result :
	String : Current directory name
	"""
	def getDirFromPath(self,path):
		abs_path = os.path.abspath(path )
		return abs_path.split(os.sep)[-1] #



	"""
	@Description :
	Get the correctly formated directory that needs to be patched

	@Parameters :
	None

	@Result :
	String : Correctly formated directory name
	"""
	def getDirToBePatched(self):
		return self.dir_01


	"""
	@Description :
	Get the correctly formated directory used to for patching

	@Parameters :
	None

	@Result :
	String : Correctly formated directory name
	"""
	def getDirUsedToPatch(self):
		return self.dir_02

	"""
	@Description :
	Get the correctly formated frame patch directory

	@Parameters :
	None

	@Result :
	String : Correctly formated directory name
	"""
	def getFrameoPatchDir(self):
		return self.frame_patch_dir


	"""
	@Description :
	Get the latest version (highest) of the Render Layer.

	@Parameters :
	String : dir

	@Result :
	String : Current directory name
	"""
	def getLatestVer(self, dir):
		parent_dir = os.path.abspath(os.path.join(dir,'..'))
		ordered_dict = self.getAllSubDir(parent_dir)
		"""
		Get the last sorted entry in the dictionary object.
		EXAMPLE : 'v300'
		"""
		return ordered_dict[-1]



	"""
	@Description :
	TODO

	@Parameters :
	TODO

	@Result :
	TODO
	"""
	'''
	def getListOfFiles(self,dir):
		result = []
		return dir
	'''

	"""
	@Description :
	Gets all the sub directories for the new frame patch directory

	@Parameters :
	None

	@Result :
	List of Strings : Name of sub directories
	"""
	def getSubDirectories(self):
		return self.sub_dirs


	"""
	@Description :
	Set all the sub directories for the new frame patch directory

	@Parameters :
	String : Path

	@Result :
	None
	"""
	def setSubDirectories(self,list_sub_dirs):
		self.sub_dirs = list_sub_dirs


	"""
	@Description :
	Set all the sub directories for the new frame patch directory

	@Parameters :
	String : Path

	@Result :
	None
	"""
	def setFramePatchDirectory(self,fp_dir):
		self.frame_patch_dir = fp_dir


	"""
	@Description :
	Set the directory name for the next version up. This version will be the latest and will be used for frame patching.

	Get the pass version top directory name. EXAMPLE 'v0412_ysw_v3update'
	Modifier next_ver_comment variable to expand comment to include
	which pass versions are being used to patch the new pass version.
	EXAMLPLE : "FramePatchFrom-v0412-&-v0308"

	@Parameters :
	String : user, ie; 'awc'
	String : latest_ver, ie; 'v0431'
	String : path_01_ver, ie; 'v0308'
	String : path_02_ver, ie; 'v0412'

	@Result :
	String : new version name, ie;'v0431_ysw_FramePatchFrom-v0412-&-v0308'
	NOTE: template = [version]_[user]_[comment]
	"""
	def setNextVerName(self, user, latest_ver, path_01_ver, path_02_ver):
		"""
		latest_ver[0] = Extacts first char from string EXAMPLE : 'v' from 'v300'
		str(int(latest_ver[1:len(latest_ver)])+1) = Extacts ramaing chars from string
		converts them from string to integer, the adds a value of 1 to it.

		Version up.
		EXAMPLE : from 'v300' to 'v301', but remove the 'v'
		"""
		next_ver = str(int(latest_ver[1:len(latest_ver)])+1)
		"""
		Pad the number with zero's at the head, accordingly,then add back the 'v'
		"""
		next_ver = 'v' + next_ver.rjust(self.pad,'0')
		"""
		path_01.split(os.sep)[-1][0:5] = Getting the first 5 characters of the last element.
		EXAMPLE : 'v0412' of 'v0412_ysw_v3update'
		"""
		comment = self.next_ver_comnt_prfx + path_01_ver + self.next_ver_comnt_brdg + path_02_ver

		return next_ver + self.tkn_sep + user + self.tkn_sep + comment


	"""
	@Description :
	Defines a String path of a new and unique name for directory that will hold the patched frames of the rendered sequences.
	1. Get the latest version (highest) of the Render Layer, get the last sorted entry in dictionary. 	EXAMPLE : 'v0300'
	2. Get the pass version top directory name. EXAMPLE 'v0412_ysw_v3update
	3. Get the first 5 characters of the last element. EXAMPLE : 'v0412' of 'v0412_ysw_v3update'
	4. Get the first 5 characters of the last element. EXAMPLE : 'v0412' of 'v0412_ysw_v3update'
	5. Create new directory for frame patching

	@Parameters :
	None

	@Result :
	String frame_patch_dir : New path of Frame Patch Path
	"""
	def createDirNextVer(self):
		#parent_dir = os.path.abspath(os.path.join(self.dir_01,'..'))
		parent_dir = self.parent_dir
		"""
		Get the latest version (highest) of the Render Layer
		Get the last sorted entry in dictionary.
		EXAMPLE : 'v0300'
		"""
		latest_ver = self.getLatestVer(self.dir_01)[0]

		subDir_01_ver = self.getAllSubDir(self.dir_01)
		subDir_02_ver = self.getAllSubDir(self.dir_02)

		"""
		Get the pass version top directory name.
		EXAMPLE 'v0412_ysw_v3update

		Get the first 5 characters of the last element.
		EXAMPLE : 'v0412' of 'v0412_ysw_v3update'
		"""
		path_01_ver = self.dir_01.split(os.sep)[-1][0:5]
		"""
		Get the first 5 characters of the last element.
		EXAMPLE : 'v0412' of 'v0412_ysw_v3update'
		"""
		path_02_ver = self.dir_02.split(os.sep)[-1][0:5]

		next_ver_name = self.setNextVerName(self.user, latest_ver, path_01_ver, path_02_ver)

		"""
		Create new directory for frame patching
		"""
		frame_patch_dir = os.path.join(parent_dir, next_ver_name)
		os.mkdir(os.path.join(frame_patch_dir), self.dir_mode)

		# Set self.frame_patch_dir variable
		#self.setFramePatchDirectory(frame_patch_dir)

		return frame_patch_dir


	"""
	@Description :
	Creates sub directory (represented by the parameter 'sub_dir')
	of the parent directory (represented by the parameter 'parent_dir')

	@Parameters :
	String parent_dir
	String sub_dir

	@Result :
	None or String Result; this dependent on check to see if the directory was created
	"""
	def createSubDirectory(self,parent_dir,sub_dir):
		result = None

		dir = os.path.join(parent_dir, sub_dir)
		#print("FramePatchModel :: createSubDirectory() :: dir ", dir)
		os.mkdir(os.path.join(dir), self.dir_mode)

		# Check to see if the directory was actually created
		if os.path.exists(dir):
			result = dir

		#print("FramePatchModel :: createSubDirectory() :: result ", result)
		return result

	"""
	@Description :
	TODO

	@Parameters :
	String list lst  :

	@Result :
	String list Result :
	"""
	def sortListByFrameNumber(self, lst, delimter):
		result = []
		list_split = {}

		# Split String path by delimiter
		for l in lst:
			split_l = l.split(delimter)
			#print("FramePatchModel :: sortList() :: split_l = ", split_l, type(split_l))
			list_split[split_l[1]] = l

		od = collections.OrderedDict(sorted(list_split.items()))
		#print("FramePatchModel :: sortList() :: list_split = ", list_split, type(list_split))
		#print("FramePatchModel :: sortList() :: od = ", od, type(od))

		# Order list by frame number
		for k in list(od.keys()):
			result.append(od[k])

		#print("FramePatchModel :: sortList() :: result = ",  result)
		return result


	"""
	@Description :
	Copies frames from the directories that need and are used for frame patching, to the newly created directory that is storing the patched frame render sequences

	@Parameters :
	String dir_to_patch : Path of directory where the frames of the render sequence that needs it frames patched.
	String dir_use_patch : Path of directory where the frames are stored to patch the render sequence.
	String frame_patch_dir : Path of directory where the patched frames will be copied to.
	String List sub_dirs : Sub directory names to joined to dir_to_patch, dir_use_patch and frame_patch_dir paramters to define the literal string paths for copyfiles() function parameters

	@Result :
	Dictionary Result : Key is a destination sub directory and the value is a list of files copied to that destination sub directory
	"""
	def copyFiles(self, dir_to_patch, dir_use_patch, frame_patch_dir, sub_dirs):
		# Create empty dictionary to return information of the process
		result = {}

		src_files ={}
		src_dirs = []
		#print("FramePatchModel :: copyFiles() :: src_dirs ", sub_dirs, type(sub_dirs))
		'''
		1. Loop through the list of sub directories.
		2. Create String Paths of the two source sub directories by joining their String to their respective parent diretories.
		   These two sub directories will be used to frame patch a rendered sequence.
		3. Create two lists of files contained in the two source sub directories and store them in the List src_files vatiable.
		4. Loop through the
		'''
		for sd in sub_dirs:
			#print("\n\nCopying files for " + str(sd) + " : \n")
			src_sd_01 = os.path.join(dir_to_patch, sd)
			src_sd_02 = os.path.join(dir_use_patch, sd)
			#print("FramePatchModel :: copyFiles() :: src_sd_01 ", src_sd_01)
			#print("FramePatchModel :: copyFiles() :: src_sd_02 ", src_sd_02)

			dst_sd = os.path.join(frame_patch_dir, sd)
			#print("FramePatchModel :: copyFiles() :: dst_sd ", dst_sd)

			# Get a list of files in the selected souce sub directories and add them to a Dictiionay object to be looped through
			src_files[src_sd_01] = os.listdir(src_sd_01)
			src_files[src_sd_02] = os.listdir(src_sd_02)
			#print("FramePatchModel :: copyFiles() :: src_files ", src_files, type(src_files))

			# Create empty list to store the files being copied
			dst_list = []
			#print("FramePatchModel :: copyFiles() :: dst_list ", dst_list)

			# Loop through list of sub direcotories
			for d in list(src_files.keys()):
				#print( "FramePatchModel :: copyFiles() :: d ", d, type(d) )

				for f in  src_files[d]:
					#print( "FramePatchModel :: copyFiles() :: f ", f, type(src_files[d]) )
					src = os.path.join(str(d), str(f))
					dst = os.path.join(dst_sd, str(f))
					#print("FramePatchModel :: copyFiles :: src :", src)
					#print("FramePatchModel :: copyFiles :: dst :", dst)
					#print("FramePatchModel :: copyFiles :: dst_list :", dst_list)

					# You need to convert the String objects to a Raw String format
					# for the shutil.copyfile() function to work correctly.
					raw_src = r"{}".format(src)
					raw_dst = r"{}".format(dst)

					shutil.copyfile(raw_src,raw_dst)

					#print("Adding file " + str(dst) + " to dst_list\n")
					dst_list.append(dst)

			#sorted_dst_list =  dst_list.sort()
			sorted_dst_list = self.sortListByFrameNumber(dst_list, '.')
			#print( "FramePatchModel :: copyFiles() :: sorted_dst_list = ", sorted_dst_list )
			result[dst_sd] = sorted_dst_list #dst_list
			#print( "FramePatchModel :: copyFiles() :: result ", result )
			#print( "Resetting loop variables\n\n\n" )

			# Reset Variables for next loop
			src_files = {}
			#print( "FramePatchModel :: copyFiles() :: src_files ", src_files )
			#print( "\n\n\n" )

		# Return a Dictionary object of all files copied
		return result


	"""
	@Description :
	TODO

	@Parameters :
	None

	@Result :
	TODO
	"""
	def saveLogFile(self):
		today = date.today()
		#print("Today's date:", today)
		this_dir = getCommonParentDir()
		txt_file = os.path.join(this_dir, 'log'+str(today)+'.txt')
		log_file = open(txt_file)# , "w")


	"""
	@Description :
	TODO

	@Parameters :
	TODO

	@Result :
	TODO
	"""
	def checkSubDir(self, dict1, dict2):
		result = {}
		dict1Keys = list(dict1.keys())[0]
		dict2Keys = list(dict2.keys())[0]
		lenDict1Values = len(list(dict1.values())[0])
		lenDict2Values = len(list(dict2.values())[0])
		#print("FramePatchModel :: checkSubDir() :: dict1Keys ", dict1Keys)
		#print("FramePatchModel :: checkSubDir() :: list(dict1.values()) ", list(dict1.values()) )
		#print("FramePatchModel :: checkSubDir() :: lenDict2Values ", lenDict2Values )
		#print("FramePatchModel :: checkSubDir() :: lenDict1Values ", lenDict1Values )

		"""
		Check to see if the lists assigned to the dictionary variables are empty.
		"""
		if( lenDict1Values == 0 ) or ( lenDict2Values == 0 ):
			"""
			Returns a Dictionary
			Key = Boolean False
			Value = String Error Message. If any of the directoires are missing sub directories, report which one(s)
			"""
			# Preparing the Dictionary oject for multiple error messages
			result = {False : []}

			if lenDict1Values == 0 :
				list(result.values())[0].append( str("Error : " +  dict1Keys + " has no sub directories.") )
			if lenDict2Values == 0 :
				list(result.values())[0].append( str("Error : " + dict2Keys + " has no sub directories.") )

		elif lenDict1Values != lenDict2Values:
			"""
			Returns a Dictionary
			Key = Boolean False
			Value = String Error Message. If the number of sub directoires do not match, then report this as an error.
			"""
			#result.append("Error : " +  dict1Keys + " number of sub directories does not match that of " + dict2Keys + " number of sub directries.")
			result = { False : str("Error : " +  dict1Keys + " number of sub directories does not match that of " + dict2Keys + " number of sub directries.") }
		else:
			"""
			Returns a Dictionary
			Key = Boolean True
			Value = List of sub directories
			"""
			result = { True : list(dict1.values())[0] }#self.copyFiles(dict1, dict2)

		#print("FramePatchModel :: checkSubDirs() :: result ", result)
		return result


	"""
	@Description :
	This function checks the sub directories names contain the same Colourspace and Resolution attribute values.

	@Parameters :
	String : resoution value of Sub Directory 1, ie; '1224x852x1'
	String : colourspace value of Sub Directory 1, ie; 'linear'
	String : resoution value of Sub Directory 2, ie; '1224x852x1'
	String : colourspace value of Sub Directory 2, ie; 'linear'

	@Result :
	Boolean : True or False.
	"""
	def checkPassVerMatch(self, pass_res_01, pass_colSpce_01, pass_res_02, pass_colSpce_02):
		result = False

		if(pass_res_01 == pass_res_02) & (pass_colSpce_01 == pass_colSpce_02):
			result = True

		#print("FramePatchModel :: checkPassVerMatch :: result : ", result)
		return result


	"""
	@Description :
	This function checks the sub directories of the two parent directories for:
	1. Equal number of sub Direcotories (or any at all).
	2. Have the same Colour Space and Resolution values.
	3. That the name of the sub directories match exactly.
	Calls the function self.checkSubDir().
	NOTE: name structure should match the following template:
	[pass type]_[resolution]_[colourspace]
	eg: beauty_1224x852x1_linear
	NOTE: name of rendered frames stored within the sub directores has the following name template:
	[pass type]_[resolution]_[colourspace]_[comment(and/or user initials)].[frame number].[extension]
	eg: roger_beauty_1224x852x1_linear_awc.0011.exr

	@Parameters :
	None

	@Result :
	Returns a dictionary object with one Key and Value element.
	Key   = Boolean
	Value = List (String). If Key = True, the Value will return a list of sub directories to be copied.
	"""
	def checkPasses(self):
		result = {True : ["Application checks were run and no were errors found."]}
		#print("FramePatchModel :: checkPasses :: result : ", result)

		subDir_01 =  os.listdir(self.path_01)
		subDir_02 =  os.listdir(self.path_02)
		#print("FramePatchModel :: checkPasses() :: subDir_01 ", subDir_01)
		#print("FramePatchModel :: checkPasses() :: subDir_02 ", subDir_02)

		"""
		Declared to allow the popping (removal) of elements when variables are run through the function findUniqueSubDir()
		"""
		copy_subDir_01 =  os.listdir(self.path_01)
		copy_subDir_02 =  os.listdir(self.path_02)
		#print("FramePatchModel :: checkPasses() :: copy_subDir_01 ", copy_subDir_01)
		#print("FramePatchModel :: checkPasses() :: copy_subDir_02 ", copy_subDir_02)

		dir_01_name = self.getDirFromPath(self.dir_01)
		dir_02_name = self.getDirFromPath(self.dir_02)

		"""
		Create 2 dictionary objects.
		Key	= String
		Value = List
		"""
		dir_01_dict = {dir_01_name : subDir_01}
		dir_02_dict = {dir_02_name : subDir_02}
		#print("checkPasses() :: subDir_01 ", subDir_01)
		"""
		Declared to allow the popping (removal) of elements when variables are run through the function findUniqueSubDir()
		"""
		copy_dir_01_dict = {dir_01_name : copy_subDir_01}
		copy_dir_02_dict = {dir_02_name : copy_subDir_02}
		#print("checkPasses() :: copy_dir_01_dict ", copy_dir_01_dict)

		"""
		Calling the function self.checkSubDir() to check the sub directories for the following potential issues:
		1. Equal number of sub Direcotories (or any at all).
		If there is an error, a Dictionary object will be returned with its KEY
		being a boolean value of False and its VALUE being a String or List of Strings
	 	with a value structured as the following;
		Prefix ' ERROR : ' followed by a description of the error.
		If no error, the function will return a Dictionary object with its Key
		being a boolean value of True and its VALUE being a List of String sub directory names.
		"""
		result = self.checkSubDir(copy_dir_01_dict,copy_dir_02_dict)
		#print("FramePatchModel :: checkPasses :: result : ", result)
		#print("FramePatchModel :: checkPasses :: list(result.keys())[0] : ", list(result.keys())[0])

		"""
		We need to check the that the sub directories names match exactly the same between the two parent directories.
		"""
		if list(result.keys())[0]:
			'''
			If the KEY of check has a Boolean value of True, we now need to check
			the sub directories names exactly match between the two parent directories
			'''
			resolution_01 = subDir_01[0].split(self.tkn_sep)[1]
			colourSpace_01 = subDir_01[0].split(self.tkn_sep)[2]
			#print("FramePatchModel :: checkPasses :: resolution_01 : ", resolution_01)
			#print("FramePatchModel :: checkPasses ::colourSpace_01 : ", colourSpace_01)

			resolution_02 = subDir_02[0].split(self.tkn_sep)[1]
			colourSpace_02 = subDir_02[0].split(self.tkn_sep)[2]
			#print("FramePatchModel :: checkPasses :: resolution_02 : ", resolution_02)
			#print("FramePatchModel :: checkPasses ::colourSpace_02 : ", colourSpace_02)

			"""
			Check to see each versions passes were rendered at the same resolution and colourspace.

			"""
			if not self.checkPassVerMatch(resolution_01,colourSpace_01,resolution_02,colourSpace_02):
				result = { False : str("ERROR : "+ dir_01_name +" and "+ dir_02_name +" passes are rendered at a different resolution and/or Colourspace.") }

		#print("FramePatchModel :: checkPasses :: result : ", result)
		return result


	"""
	@Description :
	Runs Checks to ensure that the two directories are:
	1. have the same Parent directory.
	2. that the sub directories:
		A. Equal number of sub Direcotories (or any at all).
		B. Have the same Colour Space and Resolution values.
		C. That the name of the sub directories match exactly.
	before processing the Frame Patch operation.
	Calls the following functions:
	1. self.getCommonParentDir()
	2. self.checkPasses()

	@Parameters :
	NA

	@Result :
	Returns Dictionary [Boolean, String]
	Boolean = True OR False
	String = "Error Comment"
	"""
	def runChecks(self):
		result = {False : ["Application checks DID NOT run correctly."]}

		"""
		Check to make sure that the names of directories to be check do not match
		"""
		if self.dir_01 != self.dir_02 :
			"""
			Check that both versions share the same parent directory
			"""
			if self.getCommonParentDir() != None:
				"""
				Check that both versions share the same resolution and colour space
				"""
				result = self.checkPasses()
			else:
				result = {False : ["Passes " + str(self.dir_01) + " and " + str(self.dir_02) + " do not share the same parent directory."]}
		else:
			result = {False : ["The same directory (" + + str(self.dir_01) + ") has been selected to Frame Patch. They must 2 different directories must be selected."]}

		#print("FramePatchModel :: runChecks :: result : ", result)
		return result
