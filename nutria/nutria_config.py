import os
import sys

HOST = '127.0.0.1'
WEB_PORT = 5000

BASEDIR = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../')
WEBDIR = BASEDIR + '/web/'
sys.path.append(BASEDIR)
