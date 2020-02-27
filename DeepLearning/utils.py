import os
import logging

def mkdir(path):
    """
    创建目录
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info("创建路径" + path + "成功！")
    except Exception as e:
        logging.error("路径" + path + " 创建失败！")
        raise Exception(e)