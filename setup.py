from distutils.core import setup

setup(
    name = "python-googlevoice",
    version = '0.2',
    url = 'http://code.google.com/p/pygooglevoice',
    author = 'Justin Quick and Joe McCall',
    description = 'Python 2/3 Interface for Google Voice',
    packages = ['googlevoice'],
    scripts = ['bin/gvoice']
)

