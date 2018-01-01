# coding=utf-8
'''
Misc Utility Functions Go here
'''


thousand =1000
million =thousand * thousand
billion = million *thousand

#Easy to read numbers
def easyreadnum(num):
	if num >= billion:
		return str(num//billion)+'B'
	if num >=million:
		return str(num//million)+'M'
	if num >=thousand:
		return str(num//thousand)+'K'


#Website APIs need space fixing
def urlfixer(string):
	string = string.encode('utf-8')
	string = string.replace(' ','+').replace('&','%26')
	print string
	return string


#Path fixing for cross platform support
def pathfixer(path):
	return path.replace('?','(ques)')