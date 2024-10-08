'''
Author : hupeng
Time : 2021/12/9 11:22 
Description: 
'''
import os

from fairy import localconfig

# localconfig.read('config/config.ini')
# MODEL_PATH = localconfig.server.model_path
# MEMORY_FRACTION = float(localconfig.server.memory_fraction)
# TEXT_DETECTION_URL = localconfig.server.text_detection_url

from utils.log import logger_init

LOG_DIR = './logs/ocrquesseg-svr/'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

loggers = {
    'main':
        {
            'log_dir': LOG_DIR,
            'handlers': {'ocrquesseg': 'INFO', 'error': 'ERROR'}
        }
}
logger_init(loggers)
