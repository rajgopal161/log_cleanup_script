import logging
from logging import handlers
from datetime import datetime
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'configs.txt'))


#def logging_out():
dt_log = datetime.today().strftime('%Y_%m_%d %H_%M_%S_')
log_path = config.get('configs', 'log_path')
logging.basicConfig(
				filename= log_path + dt_log + "logs.txt" , 
				format='%(asctime)s %(message)s', 
				filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)