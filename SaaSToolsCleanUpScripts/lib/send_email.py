# -*- coding: utf8 -*-

import logging
import smtplib, ssl
#import creds
from logging_out import logger
import ConfigParser



def send_email():
    log_path = config.get('configs', 'log_path')
    with open(log_path + "logs.txt", "r") as textfile:
        content = textfile.readlines()
        log_text = "".join(content) 
        textfile.close()

    email_text = """\
From: %s
To: %s
Subject: %s

%s\n
%s
""" % (sent_from, ", ".join(to), subject, body, log_text)
 
    try:
    
        
        smtp_server = smtplib.SMTP(smpt_server_region, port)
        #smtp_server.ehlo()
        smtp_server.starttls()
        #smtp_server.ehlo()
        smtp_server.login(SMTP_user, SMTP_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        
        #textfile.close()
        
        logger.info("Email sent successfully!")
        logger.info("Archive Cleanup Completed succesfully.")
    except Exception as e:
        #print(type(e))
        logger.info("Something went wrong….")
        logger.info(e)
    

def send_failure_email():

    try:
        smtp_server = smtplib.SMTP(smpt_server_region, port)
        #smtp_server.ehlo()
        smtp_server.starttls()
        #smtp_server.ehlo()
        smtp_server.login(SMTP_user, SMTP_password)
        smtp_server.sendmail(sent_from, to, failure_email_text)
        smtp_server.close()
        #print ("Failure Email sent successfully!")
        logger.info("Failure Email sent successfully!")
    except Exception as e:
        #print(e)
        logger.info("Something went wrong….")
        logger.info(e)
        
        


#--------Config file datils------#

config = ConfigParser.ConfigParser()
config.readfp(open(r'configs.txt'))

SMTP_user = config.get('SMTP details', 'SMTP_user')
SMTP_password = config.get('SMTP details', 'SMTP_password')
    
smpt_server_region = config.get('SMTP details', 'smpt_server_region')
port = 587
context = ssl.create_default_context()

sent_from = config.get('SMTP details', 'sent_from')
to = eval(config.get('SMTP details', 'to'))


#Email text in case of successful completion
subject = config.get('SMTP details', 'subject')
body = config.get('SMTP details', 'body')   
    

#Email text in case of failure
f_subject = config.get('SMTP details', 'f_subject')
f_body = config.get('SMTP details', 'f_body')
failure_email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), f_subject, f_body)
