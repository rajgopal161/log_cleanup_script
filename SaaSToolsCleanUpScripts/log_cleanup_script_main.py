#Owner RajGopal

from lib.find_archive_files_and_zip import find_archive_files_and_zip
from lib.upload_files_to_s3_and_delete_files import upload_files_to_s3_and_delete_files
from lib.send_email import send_email, send_failure_email
from lib.logging_out import logger



#Main script starts here

#Calling the functions

#logger.info("Archive Cleanup Started")
find_archive_files_and_zip()
