# $language = "python"
# $interface = "1.0"

from __future__ import print_function #Only for Python2
import fileinput
import sys
import os
import datetime
import time

LOG_DIR = os.path.join(os.path.expanduser('~/Desktop/'), 'StatusCheck')
#LOG_DIRECTORY = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%m-%d-%Y"))
#LOG_SITE = os.path.join(LOG_DIRECTORY, 'Site')
#LOG_FILE_TEMPLATE = os.path.join(LOG_SITE, "%s.log")
LOG_FILE_TEMPLATE = os.path.join(LOG_DIR, "%s.log")
global site
SCRIPT_TAB = crt.GetScriptTab()

def main():
	szPrompt = "Tip: use option"


	SCRIPT_TAB.Screen.Synchronous = True
	SCRIPT_TAB.Screen.IgnoreEscape = True
	szCommand = "cabx"

	fname = "Cabx-Output"
	cabxOP = LOG_FILE_TEMPLATE % fname
	fname = "VSWR-MAP"
	vswrMap = LOG_FILE_TEMPLATE % fname
	#cabxOP = "C:\\Users\eanagsa\Desktop\StatusCheck\VSWR-MAP.log"

	site = getSite()
	SCRIPT_TAB.Screen.Send('lt all' + '\r')
	SCRIPT_TAB.Screen.Send(szCommand + "\r\n")
	SCRIPT_TAB.Screen.WaitForString(szCommand + "\r\n")
	szResult = SCRIPT_TAB.Screen.ReadString(szPrompt)

	filep = open(cabxOP, 'wb+')
	filep.write(szResult + os.linesep)
	filep.close()
	#crt.Dialog.MessageBox(szResult)

	flag=0
	with open(cabxOP) as f1,open(vswrMap,'w') as op1:
		print("Site = "+site+'\n',end='',file=op1)
            cont = 1
            for line in f1:
				if ("TX (W/dBm)" in line):
					flag = 1
					continue
				if flag==1:
					if ("----------" in line):
						flag = 0
						break
					if ("========" in line):
						continue
				if (line.rstrip()):
					x = line.split()
					port = x[3]
					if (x[5] != '-'):
						cell = x[12].split("=")[1]
						vswr = x[8]
					else:
						cell = x[9].split("=")[1]
						vswr = "-"
					print (cell+'\t'+port+'\t'+vswr+'\n', end='',file=op1)

	SCRIPT_TAB.Screen.Send('#DONE' + '\r')
	getVSWR(vswrMap)
if __name__ == '__main__':
    main()

def getSite():

	SCRIPT_TAB.Screen.Send('get ManagedElement site > $sitename' + '\r')
	SCRIPT_TAB.Screen.Send('#DONE' + '\r')
	fname = "Site"
	siteOP = LOG_FILE_TEMPLATE % fname
	sitename = SCRIPT_TAB.Screen.ReadString('> #DONE')
	filep = open(siteOP, 'wb+')
	filep.write(sitename + os.linesep)
	filep.close()
	with open('site.txt') as f1:
		for line in f1:
				if ("ManagedElement=" in line):
					site = line.split("=")[1].split()[0]
	f1.close()
	return site

def getVSWR(vswrFile):
	vswrCell = {}
	vswrValues = {}
	fname = "VSWR-FINAL"
	lastCell = ""
	start = 0
	portCount = 0
	vswrFinal = LOG_FILE_TEMPLATE % fname
	with open(vswrFile) as f1,open(vswrFinal,'w') as f2:
		print ("Site ID\t\tVSWR1\tVSWR2\tVSWR3\tVSWR4\n", end='',file=f2)
		for line in f1:
			x = line.split()
			currCell = x[0]
			port = x[1]
			if(port=='A'):
				if(start ==0):
					start = 1
				elif(currCell!=lastCell):
					if(portCount==2):
						vswrValues['VSWR3']='-'
						vswrValues['VSWR4']='-'
					portCount = 0
					vswrCell[lastCell] = vswrValues
					print (lastCell+'\t'+vswrValues['VSWR1']+'\t'+vswrValues['VSWR2']+'\t'+vswrValues['VSWR3']+'\t'+vswrValues['VSWR4']+'\n', end='',file=f2)
					vswrValues = {}
				vswrValues['VSWR1']=x[2]
				portCount+=1
			elif(port=='B'):
				vswrValues['VSWR2']=x[2]
				portCount+=1
			elif(port=='C'):
				vswrValues['VSWR3']=x[2]
				portCount+=1
			elif(port=='D'):
				vswrValues['VSWR4']=x[2]
				portCount+=1
			else:
				continue
			lastCell = currCell
		print (lastCell+'\t'+vswrValues['VSWR1']+'\t'+vswrValues['VSWR2']+'\t'+vswrValues['VSWR3']+'\t'+vswrValues['VSWR4']+'\n', end='',file=f2)







#with open(cabxOP) as f1,open(vswrMap,'w') as op1:
