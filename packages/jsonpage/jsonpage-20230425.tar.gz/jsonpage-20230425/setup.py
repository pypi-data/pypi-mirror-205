import time
import glob
from distutils.core import setup

setup(
  name = 'jsonpage',
  module = ['jsonpage'],
  version = time.strftime('%Y%m%d'),
  description = 'Generates an html page from JSON',
  author = 'Bhupendra Singh',
  author_email = 'bhsingh@gmail.com'
)
