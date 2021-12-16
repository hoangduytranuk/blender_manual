import inspect
import logging
import datetime
import os
from pprint import pprint as pp

DEBUG=False
# DEBUG=False
DIC_LOWER_CASE=True

def dd(*args, **kwargs):
    if DEBUG:
        print(*args, sep='\n- ')
        # print(args, kwargs)
        # if len(args) > 0:
        #     print('-' * 80)

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_logger(filename):
    logging.basicConfig(filename=f"{filename}", filemode='a', format="%(message)s")
    logging.warning(f"[{datetime.datetime.now()}] {'=' * 10}")

    def log(message, error=False, include_filename=True):
        frame, filename, line_number, function_name, lines, index = inspect.stack()[1]

        c_frame = inspect.currentframe()
        func = c_frame.f_back.f_code
        final_msg = "(%s():%i) %s" % (
            func.co_name,
            func.co_firstlineno,
            message
        )

        if include_filename:
            final_msg += f'\n{os.path.basename(filename)}'

        if error:
            logging.warning(final_msg)
            dd(f"[ERROR] {final_msg}")
        else:
            dd(final_msg)

    return log


def test_announce(fn):
    def wrap(*args):
        print(f"Testing {Colors.WARNING}{fn.__name__}{Colors.ENDC}")
        return fn(*args)
    return wrap