from setuptools import setup
import os

requirements = []
f = open('requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    requirements.append(l.rstrip())
f.close()


setup(
    packages=[
        'feedwarrior',
        'feedwarrior.cmd',
        'feedwarrior.adapters',
        'feedwarrior.runnable',
        ],
    install_requires=[
        requirements,
        ],
    entry_points = {
        'console_scripts': [
            'feedwarrior = feedwarrior.runnable.main:main',
            ],
        },
)
