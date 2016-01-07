from sms_send_and_receive import sms_tester
from sys import argv


## use this def from another file, ex:
script, s_null, MO_device_ser, MO_tn, s_null_2, MT_device_ser, MT_tn, message, num_of_text = argv

message = message + "... append something, large text example...... blah blah"

## create a new object
tester = sms_tester(False)

## call send_and_receive_sms def
other_file = tester.send_and_receive_sms(MO_device_ser, MO_tn, MT_device_ser, MT_tn, message, num_of_text)

## print out success message
print "\nDid all the texts pass?: %s" % other_file

