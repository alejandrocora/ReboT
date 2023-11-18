from setuptools import setup, find_packages

requires = [
    'selenium',
    'argparse'
]

setup(
    name='ReboT',
    description=(""),
    version='1.0',
    install_requires=requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['rebot=ReboT.app:main'],
    },
    keywords=[]
)