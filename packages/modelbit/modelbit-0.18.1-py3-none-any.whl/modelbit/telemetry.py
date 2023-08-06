import logging
import os


def initLogging():
  LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
  logging.basicConfig(level=LOGLEVEL)
