# -*- coding: utf8 -*-

import os
import sys
import boto  #pip install boto
from boto.s3.key import Key
import boto.s3.connection
from logging_out import logger
import pathlib #pip install pathlib
import ConfigParser
from datetime import datetime
from send_email import send_email, send_failure_email



def upload_files_to_s3_and_delete_files() :
    
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'configs.txt'))
    local_path = config.get('configs', 'local_path')
    try:
        for path, dirs, files in os.walk(local_path):
            for ddir in dirs:
                if ddir.lower() == "archive" or ddir.lower() == "archives"  :
                    for spath,sdir,file in os.walk(os.path.join(path,ddir)):
                        for fi in file:
                            parentdircount = (os.path.normpath(path).count(os.sep))
                            if (parentdircount > 2) and fi.endswith('.zip')  : 
                                full_path = spath              
                                relative_path = config.get('configs', 'relative_path')
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
                                logger.info(fi + " Uploaded succesfully to s3 under " + Bucketname +"/" + s3path + "/" + relative_parent_dir_path + "/")
                                os.remove(os.path.join(spath, fi))  
                                #logger.info(fi + " File deleted succesfully from path " + spath)
                            
                else:
                    break
                    
        send_email()
                    
    except Exception as e:
        logger.info(" ... Failed!! Quitting Upload!!")
        logger.info(e)
        send_failure_email()
        
        

config = ConfigParser.ConfigParser()
config.readfp(open(r'configs.txt'))

#----------To get date and time attribute--------------#
dt_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


#------------Connecting to AWS--------------#
Bucketname = config.get('configs', 'Bucketname')
FILENAME = ''                
UPLOADED_FILENAME = ''
s3path = config.get('configs', 's3path')

conn = boto.s3.connect_to_region('us-west-2',
   aws_access_key_id= config.get('AWS Connect', 'AWS_ACCESS_KEY_ID'),
   aws_secret_access_key= config.get('AWS Connect', 'AWS_SECRET_ACCESS_KEY'),
   is_secure=True,               # uncomment if you are not using ssl
   )
