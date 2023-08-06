import os
from loguru import logger

"""
操作日志记录
"""
import time
from loguru import logger
from pathlib import Path

project_path = Path.cwd().parent
log_path = Path(project_path, "logs")


# t = time.strftime("%Y_%m_%d")


class Loggings:
    __instance = None
    logger.add(f"{log_path}/error.log", rotation="500MB", encoding="utf-8", enqueue=True,
               retention="5 days")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def warning(self, msg):
        return logger.warning(msg)

    def error(self, msg):
        return logger.error(msg)

    def critical(self, msg):
        return logger.critical(msg)

    def exception(self, msg):
        return logger.exception(msg)

    def add(self, *args, **kwargs):
        return logger.add(*args, **kwargs)



loggings = Loggings()
if __name__ == '__main__':
    loggings.info("中文test")
    loggings.debug("中文test")
    loggings.warning("中文test")
    loggings.error("中文test")

    logger.info('If you are using Python {}, prefer {feature} of course!', 3.6, feature='f-strings')
    n1 = "cool"
    n2 = [1, 2, 3]

    loggings.add(f"file_{time.time()}.log", rotation="500 MB")
    loggings.info(f'If you are using Python {n1}, prefer {n2} of course!')
    logger.info(f'xxxxxxxxxxxxxxxxx')


#
# p1 = os.path.abspath(__file__)
#
# # basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# # print(f"log basedir{basedir}")  # /xxx/python_code/FastAdmin/backend/app
# # 定位到log日志文件
# log_path = os.path.join(basedir, 'logs')
#
# if not os.path.exists(log_path):
#     os.mkdir(log_path)
#
# # log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')
# log_path_error = os.path.join(log_path, 'info.log')
#
# # 日志简单配置
# # 具体其他配置 可自行参考 https://github.com/Delgan/loguru
# logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True, encoding="utf-8")

#
# if __name__ == '__main__':
#     log = logger('all.log', level='debug')
#     log.logger.debug('debug')
#     log.logger.info('info')
#     log.logger.warning('警告')
#     log.logger.error('报错')
#     log.logger.critical('严重')
#     log.logger.exception("ex")
#     logger('error.log', level='error').logger.error('error')
