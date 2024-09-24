import logging
import os

logger = None

def setup_hacpp_logger(log_dir_path):
    global logger

    # 如果日志文件目录不存在，创建它
    if not os.path.exists(os.path.dirname(os.path.join(log_dir_path, 'hacpp.log'))):
        os.makedirs(os.path.dirname(os.path.join(log_dir_path, 'hacpp.log')))

    # 创建 logger
    logger = logging.getLogger('hacpp')
    logger.setLevel(logging.INFO)

    # 创建处理器并设置日志文件
    file_handler = logging.FileHandler(os.path.join(log_dir_path, 'hacpp.log'))
    file_handler.setLevel(logging.INFO)

    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将处理器添加到 logger
    logger.addHandler(file_handler)

def h_log(message):
    global logger
    if logger is None:
        raise Exception("Logger is not set up. Please call setup_logger first.")
    
    # 写入日志
    logger.info(message)
