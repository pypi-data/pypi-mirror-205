import os
from setuptools import setup

setup(
    name='linktest',
    version='2.0.0',
    author='Wang Lin',
    author_email='think_wl@163.com',
    packages=['lintest'],
    install_requires=[
    	"psutil",
    	"requests",
        "curlify",
    	"selenium",
    	"selenium-wire",
    	"setuptools",
    	"urllib3",
    	"PyMySQL",
        "jsoncomparison",
    	"chromedriver_autoinstaller"
    ],
)

# python setup.py sdist --formats=gztar,zip
