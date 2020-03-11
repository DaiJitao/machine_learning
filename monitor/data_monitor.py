
import subprocess
from pprint import pprint
import logging
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def delete(character, file_dir):
    cmd = 'grep -o "{}"  {}* | wc -l'.format(character, file_dir)
    try:
        call = subprocess.getstatusoutput(cmd)
        if call[0] == 0:
            logger.info(call)
            return int(call[1])
        else:
            logger.error(call)
    except Exception as e:
        traceback.print_stack()
        logger.error(e)
        logger.exception(e)


if __name__ == '__main__':
    delete("ss", "root/")


