__version__ = '0.1.7'

VERSION = tuple(__version__.split('.'))

from .models import *

default_app_config = 'pxd_lingua.apps.LinguaConfig'
