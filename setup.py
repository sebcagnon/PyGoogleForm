from distutils.core import setup
setup(
  name = 'PyGoogleForm',
  packages = ['PyGoogleForm'], # this must be the same as the name above
  version = '0.4',
  description = 'A simple Python library to submit Google Forms in Python.',
  author = 'Sebastien Cagnon',
  author_email = 'cagnonsebastien@gmail.com',
  url = 'https://github.com/sebcagnon/PyGoogleForm',
  download_url = 'https://github.com/sebcagnon/PyGoogleForm/tarball/0.4',
  keywords = ['Google Form'],
  install_requires = ['beautifulsoup4'],
  classifiers = [],
)