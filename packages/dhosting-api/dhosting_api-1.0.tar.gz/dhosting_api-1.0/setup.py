import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='dhosting_api',
    version='1.0',
    packages=['dhosting_api'],
    description='Package to connect with dhosting_api',
    long_description=README,
    author='Maks Galbierczyk',
    author_email='maksymilian.galbierczyk@apz.pl',
    license='MIT',
    install_requires=[
        'Django',
        'requests'
    ]
)
