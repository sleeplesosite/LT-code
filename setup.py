try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'An implementation of an Encoder and Decoder for the Luby Transform Fountain code. Useful for transmitting data over very lossy channels where retry-based transmission protocols struggle.',
    'author': 'Anson Rosenthal',
    'url': 'https://github.com/anrosent/LT-Code',
    'author_email': 'anson.rosenthal@gmail.com',
    'version': '0.2',
    'packages': ['lt', 'lt.encoder', 'lt.decoder'],
    'scripts': [],
    'name': 'lt-code'
}

setup(**config)