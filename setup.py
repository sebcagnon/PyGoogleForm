from distutils.core import setup

# setting up long description as rst if pandoc is available
# if pandoc is unavailable, uses the .md anyway
long_description = open("README.md").read()
try:
    import subprocess
    import pandoc

    process = subprocess.Popen(
        ['which pandoc'],
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    pandoc_path = process.communicate()[0].strip('\n')
    pandoc.core.PANDOC_PATH = pandoc_path

    doc = pandoc.Document()
    doc.markdown = long_description

    long_description = doc.rst
except:
    pass


setup(
  name = 'PyGoogleForm',
  packages = ['PyGoogleForm'], # this must be the same as the name above
  version = '0.5',
  description = 'A simple Python library to submit Google Forms in Python.',
  long_description = long_description,
  author = 'Sebastien Cagnon',
  author_email = 'cagnonsebastien@gmail.com',
  url = 'https://github.com/sebcagnon/PyGoogleForm',
  download_url = 'https://github.com/sebcagnon/PyGoogleForm/tarball/0.5',
  licence = 'MIT',
  keywords = ['Google Form'],
  install_requires = ['beautifulsoup4'],
  classifiers = [],
)