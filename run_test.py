from ixia.webapi import *
import ixchariotApi
import sys
import os
import time
import telnetlib
import argparse

#######################################################################################
AP_IP = "10.10.1.109"
CONFIG = "15MU_1SS"
FILENAME = CONFIG
RUNS = 3
#######################################################################################

# Setup Commandline Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stats", action='store_true', help='Collect AP Stats')
parser.add_argument("-r", "--runs", type=int, help='Number of Runs for test (Default = 3)')
parser.add_argument("-c", "--config", type=str, help='IxChariot Config File to use (Will use file entered in script by default)')
parser.add_argument("-n", "--filename", type=str, help='Base Filepath for Testrun Results (Will use Config file name as base by default)')

args = parser.parse_args()

if args.run != None:
	RUNS = args.run

if args.config != None:
	CONFIG = args.config
	FILENAME = CONFIG

if args.filename != None:
	FILENAME = args.filename

def resetAPStats():
	tn = telnetlib.Telnet(AP_IP)
	tn.write('\033\v')
	tn.write('iwpriv aruba000 txrx_fw_st_rst 0x7ff\n')
	tn.write('exit\n')
	
	tn.close()

def recordAPStats(filename):
	tn = telnetlib.Telnet(AP_IP)
	tn.write('\033\v')
	tn.write('dmesg -c\n')

	tn.write('iwpriv aruba000 txrx_fw_stats 3\n')
	tn.write('iwpriv aruba000 txrx_fw_stats 6\n')
	tn.write('iwpriv aruba000 txrx_fw_stats 13\n')
	tn.write('iwpriv aruba000 txrx_fw_stats 16\n')
	tn.write('iwpriv aruba000 txrx_fw_stats 17\n')

	tn.write('dmesg -c\n')

	tn.write('exit\n')
	stats = tn.read_all()
	index = stats.find("RX Rate")
	
	tn.close()

	with open(filename, 'w') as fp:
		fp.write(stats[index-16:-10])

def test(filename, config):
	os.system("expect start.exp")

	webServerAddress = "https://10.10.0.40"
	version = "v1"
	user = "admin"
	password = "admin"

	print "Connecting to " + webServerAddress
	api = webApi.connect(webServerAddress, version, None, user, password)

	session = api.createSession("ixchariot")
	ixchariotApi.loadConfigFromResourcesLibrary(session, config)

	session.startSession()

	for i in range(1,RUNS+1):
		while(True):
			try:
				if args.stats == True:
					resetAPStats()

				results = session.runTest()
				with open(filename + str(i) + ".zip", "wb+") as statsfile:
					api.getStatsCsvZipToFile(results.testId, statsfile)

				if args.stats == True:
					recordAPStats(filename + "-apstats-" str(i) + ".dat")
				break
			except Exception as e:
				print "Failure"

	session.stopSession()
	session.httpDelete()

test(FILENAME, CONFIG)

