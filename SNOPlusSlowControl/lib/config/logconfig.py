from os.path import expanduser
home = expanduser("~")
import logging

#LOCAL LOGGING CONFIGURATIOn
LOG_FILENAME = '/home/uwslowcontrol/tester/SNOPlusSlowControl/SNOPlusSlowControl/log/pilog.log' #logfile source assuming homedir install
LOG_FORMAT = '%(asctime)s %(name)8s %(levelname)5s %(message)s'
LOG_LEVEL = logging.INFO

#EMAIL LIST FOR SENDING ALARMS/MESSAGES TO (Assumes homedir install)
GMAILCREDS = "/home/uwslowcontrol/tester/config/gmailcred.conf"
EMAIL_RECIPIENTS_FILE = "~/SNOPlusSlowControl/SNOPlusSlowControl/DB/emailList.txt"
