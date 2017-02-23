import logging

import sys
import platform
from scrapy.utils import project, log
from scrapy.cmdline import execute
from scrapy.settings.default_settings import LOG_FORMAT

from crawler.models import create_tables

# 0 5 * * * executor.py crawl wlg

if __name__ == '__main__':

    settings = project.get_project_settings()  # load project settings
    log.configure_logging(settings)  # project logging conf

    if platform.system() == 'Darwin':  # 本地环境，同时将日志打印到控制台。默认是输出到文件
        # logging to screen
        formatter = logging.Formatter(LOG_FORMAT)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        if ''.join(sys.argv).find('INFO') > 0:
            handler.setLevel(logging.INFO)
        else:
            handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(handler)

    create_tables()
    execute()
