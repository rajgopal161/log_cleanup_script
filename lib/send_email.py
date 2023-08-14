# -*- coding: utf8 -*-

import logging
import smtplib, ssl
import creds
from logging_out import logger
import ConfigParser



def send_email():
	
	try:
		smtp_server = smtplib.SMTP(smpt_server_region, port)
		#smtp_server.ehlo()
		smtp_server.starttls()
		#smtp_server.ehlo()
		smtp_server.login(creds.user, creds.password)
		smtp_server.sendmail(sent_from, to, email_text)
		smtp_server.close()
		logger.info("Email sent successfully!")
		logger.info("Archive Cleanup Completed succesfully.")
	except Exception as e:
		logger.info("Something went wrong….", e)
	

def send_failure_email():

	try:
		smtp_server = smtplib.SMTP(smpt_server_region, port)
		#smtp_server.ehlo()
		smtp_server.starttls()
		#smtp_server.ehlo()
		smtp_server.login(creds.user, creds.password)
		smtp_server.sendmail(sent_from, to, failure_email_text)
		smtp_server.close()
		#print ("Failure Email sent successfully!")
		logger.info("Failure Email sent successfully!")
	except Exception as e:
		logger.info("Something went wrong….", e)
		


#--------Config file datils------#

config = ConfigParser.ConfigParser()
config.readfp(open(r'configs.txt'))

	
smpt_server_region = config.get('SMTP details', 'smpt_server_region')
port = 587
context = ssl.create_default_context()

sent_from = config.get('SMTP details', 'sent_from')
to = eval(config.get('SMTP details', 'to'))
#Email text in case of successful completion
subject = config.get('SMTP details', 'subject')
body = config.get('SMTP details', 'body')
email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

#Email text in case of failure
f_subject = config.get('SMTP details', 'f_subject')
f_body = config.get('SMTP details', 'f_body')
failure_email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), f_subject, f_body)