import os
import subprocess
from time import sleep
from sys import argv

###
# I made this a class so you can call it from another Python script
#  sms_tester class is empty, init does nothing
#
#  Make a class, then call the send_and_receive_sms function. Pass all vars in function
###
class sms_tester(object):

	def __init__(self, debug):
		self.debug = debug

	##
	## Roots device then waits for device
	##
	def adb_root(self, dev):
		os.system("adb " + dev + " root")
		os.system("adb " + dev + " wait-for-device")


	##
	##Converts string to int or float
	## Stole from Stack overflow
	## http://stackoverflow.com/questions/12020821/python-int-function
	##
	def interpret_string(self, s):
		if not isinstance(s, basestring):
			return None
		if s.isdigit():
			return int(s)
		try:
			return float(s)
		except ValueError:
			return None


	###
	# Main function. Sends <num_of_text> amount of sms between the 2 devices.
	#  After every sms sent from the orig device, checks for a new incoming sms on the term device
	#  Checks the message of the new incoming sms against what was sent from the orig device
	#
	# param:
	#  MO_device - serial # of the orig device
	#  MO_tn - telephone # of the orig device
	#  MT_device - serial # of the term device
	#  MT_tn - telephone # of the term device
	#  message - the message to be sent as an SMS
	#  num_of_text - the number of SMS to be sent
	#
	# returns True, if the orig message matches the term message for all sms sent
	# returns False, if one or more message does not match
	###
	def send_and_receive_sms(self, MO_device, MO_tn, MT_device, MT_tn, message, num_of_text):

		success = True ## Return this flag var

		i = 1 #while loop iterator
		last_table_count = 0

		MO_dev = "-s " + MO_device
		MT_dev = "-s " + MT_device

		self.adb_root(MO_dev)
		self.adb_root(MT_dev)

		num_of_text = self.interpret_string(num_of_text)

		sqlite_count = "adb " + MT_dev + " shell sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db 'SELECT COUNT(*) FROM sms'"

		last_table_count = self.interpret_string(subprocess.check_output(sqlite_count, shell=True))

		while i <= num_of_text :
			os.system("adb " + MO_dev + " wait-for-device")
			message_sent = "Message #" + str(i) + ": " + message.strip()
			if self.debug:
				print "Message sent: '" + message_sent + "'"

			os.system("adb " + MO_dev + " shell am start -a android.intent.action.SENDTO -d sms:" + MT_tn + " --es sms_body '" + message_sent + "' --ez exit_on_sent true")
			os.system("adb " + MO_dev + " shell input keyevent 22")
			os.system("adb " + MO_dev + " shell input keyevent 66")
			print "Sending message #" + str(i)

			while last_table_count >= self.interpret_string(subprocess.check_output(sqlite_count, shell=True)) :
				print "sleeping"
				if self.debug:
					print "row count " + subprocess.check_output(sqlite_count, shell=True)
				
				sleep(3)
				
				if self.debug:
					print "end"
					print "last table %d" % last_table_count

			last_table_count = self.interpret_string(subprocess.check_output(sqlite_count, shell=True))

			if self.debug:
				print "count " + subprocess.check_output(sqlite_count, shell=True)

			message_received = subprocess.check_output("adb " + MT_dev + " shell sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db 'SELECT body FROM sms WHERE address='" + MO_tn + "' ORDER BY _id DESC LIMIT 1'", shell=True).strip()

			if self.debug:
				print "Message received: '" + message_received + "'"

			if message_sent == message_received:
				print "Message "+ str(i) + " is successful!"
			else:
				success = False
				print "Message "+ str(i) + " FAILED!!!"

			i = i + 1

		return success



	## If this file is run as main, arg check is needed
	##
	## !!! MIGHT NOT WORK SINCE FILE WAS CONVERTED TO A CLASS !!!
	##
	#total_args = len(argv)

	#if total_args != 9:
		#print "./sms_send_and_receive.sh <MO_device> <MO_tn> <MT_device> <MT_tn> <message> <number_of_texts>"
		#exit(0)

	#script, s_null, MO_device, MO_tn, s_null_2, MT_device, MT_tn, message, num_of_text = argv

	#no_errors = send_and_receive_sms(MO_device, MO_tn, MT_device, MT_tn, message, num_of_text)

	#print "\nDid all the texts pass?: %s" % no_errors


