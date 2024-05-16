import os
import sys
import pathlib #pip install pathlib
import zlib
import zipfile
from logging_out import logger
from send_email import send_email, send_failure_email
from upload_files_to_s3_and_delete_files import upload_files_to_s3_and_delete_files
from datetime import datetime, timedelta
import ConfigParser

def find_archive_files_and_zip():

  
  config = ConfigParser.ConfigParser()
  config.readfp(open(r'configs.txt'))
  local_path = config.get('configs', 'local_path')
  try:
    for path, dirs, files in os.walk(local_path):
      for ddir in dirs:
        if ddir.lower() ==  "archive" or ddir.lower() == "archives" :
          for spath,sdir,file in os.walk(os.path.join(path,ddir)):
            for fi in file:
              checkfile = os.path.join(spath, fi)
              file_exist = os.path.isfile(checkfile)
              parentdircount = (os.path.normpath(path).count(os.sep))
              x_days_ago = datetime.now() - timedelta(days=30)
              full_file = os.path.join(path,ddir,fi)
              file_time = datetime.fromtimestamp(os.path.getctime(full_file))
              if fi.endswith('.zip')  :
                break
              elif (file_time > x_days_ago) and (parentdircount > 2) and file_exist:   
                #logger.info(path + "\\" + fi)
                print(path + "\\" + fi, file_time)
                file_path = os.path.join(spath, ddir)
                zip_file_path = zipfile.ZipFile((file_path + ".zip"), mode="a")
                full_file_path = os.path.join(spath, fi)
                zip_file_path.write(full_file_path, fi, compress_type=compression)
                #logger.info(fi + " zipped succesfully " + spath)
                os.remove(os.path.join(spath, fi))
                logger.info(fi + " File deleted succesfully after zipping from " + spath)
            
              zip_file_path.close()
        else:
          break
          
    upload_files_to_s3_and_delete_files()

  except Exception as e:
    logger.info(" ... Failed to zip!! Quitting Operation!!")
    logger.info(e)
    send_failure_email()
    
    
compression = zipfile.ZIP_DEFLATED

dt_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')