from distutils.core import setup

setup(
    name = "pygooglevoice",
    version = '0.4',
    url = 'http://code.google.com/p/pygooglevoice',
    author = 'Justin Quick and Joe McCall',
    author_email='justquick@gmail.com, joe@mcc4ll.us',
    description = 'Python 2/3 Interface for Google Voice',
    packages = ['googlevoice'],
    scripts = ['bin/gvoice']#,'bin/gvi']
)

