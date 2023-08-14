# -*- coding: utf8 -*-

import os
import sys
import boto  #pip install boto
from boto.s3.key import Key
import boto.s3.connection
from logging_out import logger
import pathlib #pip install pathlib
import ConfigParser
import creds
from datetime import datetime
from send_email import send_email, send_failure_email



def upload_files_to_s3_and_delete_files() :
	
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'configs.txt'))
	local_path = config.get('configs', 'local_path')
	try:
		for path, dirs, files in os.walk(local_path):
			for ddir in dirs:
				if ddir.lower() ==  "archive" or ddir.lower() == "archives"  :  #Need to change the correct directory (archives or archive)
					for spath,sdir,file in os.walk(os.path.join(path,ddir)):
						for fi in file:
							parentdircount = (os.path.normpath(path).count(os.sep))
							if (parentdircount > 2) and fi.endswith('.zip')  :   #Need to change the correct pdc number
								full_path = spath							
								relative_path = config.get('configs', 'relative_path')  #Need to change the correct relative_path
								trim_path = (os.path.relpath(full_path, relative_path))
								parent_dir_path = pathlib.PureWindowsPath(trim_path)
								relative_parent_dir_path = (parent_dir_path.as_posix())
								relative_parent_dir_path = str(relative_parent_dir_path)
								FILENAME = os.path.join(spath, fi)
								UPLOADED_FILENAME = (s3path + "/" + relative_parent_dir_path + "/" + dt_now + " " + fi )
								bucket = conn.get_bucket(Bucketname)
								k = Key(bucket)
								k.key = UPLOADED_FILENAME
								k.set_contents_from_filename(FILENAME)
								print (fi + " Uploaded succesfully to s3 " + spath)
								logger.info(fi + " Uploaded succesfully to s3 " + spath)
								os.remove(os.path.join(spath, fi))
								print(fi + " File deleted succesfully from path " + spath)	
								logger.info(fi + " File deleted succesfully from path " + spath)
							
				else:
					break
					
	except Exception as e:
		#print(" ... Failed!! Quitting Upload!!")
		logger.info(" ... Failed!! Quitting Upload!!")
		#print(e)
		logger.info(e)
		send_failure_email()
		
		

config = ConfigParser.ConfigParser()
config.readfp(open(r'configs.txt'))

#----------To get date and time attribute--------------#
dt_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


#------------Connecting to AWS--------------#
#AWS_ACCESS_KEY_ID = 'AKIAR3LFGTZUBMNXZWXD'
Bucketname = config.get('configs', 'Bucketname')
FILENAME = ''                
UPLOADED_FILENAME = ''
s3path = config.get('configs', 's3path')  #Need to change the correct s3 path

conn = boto.s3.connect_to_region('us-west-2',
   aws_access_key_id= creds.AWS_ACCESS_KEY_ID,
   aws_secret_access_key= creds.AWS_SECRET_ACCESS_KEY,
   is_secure=True,               # uncomment if you are not using ssl
   )