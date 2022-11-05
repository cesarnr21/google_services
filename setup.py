from setuptools import setup
import os, re

info = {}

with open(os.path.join('googol', '__init__.py')) as file:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read()).group(1)

setup(
    name = 'googol',
    version = version,
    author = 'Cesar A Nunez Rodriguez',
    author_email = 'cesarnr21@gmail.com',
    url = 'https://github.com/cesarnr21/google_services',
    packages = ['googol'],
    description = 'A package to simplying the process of using some Google Apps',
    long_description = __doc__,
    install_requires = [
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ]
)
