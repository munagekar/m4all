'''
Used for Debugging Purposes :-D
'''
import os
class Logger():
	logfilepath = None
	logflag = False
	def __init__(self,logfolder,logflag=False):
		self.logfilepath = os.path.join(logfolder,'log.txt')
		self.logflag = logflag

	def write(self,content)
	if logflag:
		logfile = open(logfilepath)
		logfile.write(content)
		logfile.close() 

