'''
Used for Debugging Purposes :-D
'''
import os
class Logger():
	logfilepath = None

	def __init__(self,logfolder):
		self.logfilepath = os.path.join(logfolder,'log.txt')

	def write(self,content)
	logfile = open(logfilepath)
	logfile.write(content)
	logfile.close() 

