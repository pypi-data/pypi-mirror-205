from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='popcornnotify',
    version='0.2.1',
    description='Send simple emails and text messages from one API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://popcornnotify.com',
    author='Jason Strauss',
    author_email='jason@popcornnotify.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    packages=['popcornnotify', ],
    install_requires=['requests'],
    entry_points={
        'console_scripts':[
            'notify = popcornnotify.notify_cli:cli',
        ]
    }
)
