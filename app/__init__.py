import logging

import sys

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(FORMAT)
root.addHandler(ch)