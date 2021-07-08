import argparse
import datetime
import logging
import os

parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='enable debug logs', default=False)
args = parser.parse_args()


def is_debug():
    return args.debug


d, r = '\u001b[31m', '\u001b[0m' if not is_debug() else ('', '')

if is_debug():
    print('Using debug mode')
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    logging.basicConfig(filename=f'logs/{datetime.datetime.now().strftime("%m-%d-%Y_%H.%M.%S")}.log',
                        filemode='a',
                        level=logging.DEBUG,
                        format=f'{d}%(asctime)s - %(name)s - %(levelname)s - %(message)s{r}',
                        datefmt='%m/%d/%Y %H:%M:%S')
else:
    logging.basicConfig(level=logging.WARN,
                        format=f'{d}%(asctime)s - %(name)s - %(levelname)s - %(message)s{r}',
                        datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger(__name__)


def get_logger() -> logging.getLoggerClass():
    return logger
