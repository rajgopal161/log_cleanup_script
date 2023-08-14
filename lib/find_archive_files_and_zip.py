import os
import sys
import pathlib #pip install pathlib
import zlib
import zipfile
from logging_out import logger
from send_email import send_email, send_failure_email
from datetime import datetime
import ConfigParser

			
def find_archive_files_and_zip():

	
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'configs.txt'))
	local_path = config.get('configs', 'local_path')
	
	try:
		for path, dirs, files in os.walk(local_path):
			for ddir in dirs:
				if ddir.lower() ==  "archive" or ddir.lower() == "archives"  :  #Need to change the correct directory (archives or archive)
					for spath,sdir,file in os.walk(os.path.join(path,ddir)):
						for fi in file:
							checkfile = os.path.join(spath, fi)
							file_exist = os.path.isfile(checkfile)
							parentdircount = (os.path.normpath(path).count(os.sep))
							if fi.endswith('.zip')  :
								break
							elif (parentdircount > 2) and file_exist  :   #Need to change the correct pdc number
								file_path = os.path.join(spath, ddir)
								zip_file_path = zipfile.ZipFile((file_path + ".zip"), mode="a")
								full_file_path = os.path.join(spath, fi)
								zip_file_path.write(full_file_path, fi, compress_type=compression)
								print(fi, "zipped", spath, dt_now)
								#logger.info(fi, "zipped", spath, dt_now)
								os.remove(os.path.join(spath, fi))
								print(fi + " File deleted succesfully after zipping " + spath)
								logger.info(fi + " File deleted succesfully after zipping " + spath)
							
							#zf = ""
				else:
					break
					
	except Exception as e:
		print(" ... Failed to zip!! Quitting Operation!!")
		logger.info(" ... Failed to zip!! Quitting Operation!!")
		print(e)
		logger.info(e)
 		send_failure_email()					
		
compression = zipfile.ZIP_DEFLATED

dt_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
