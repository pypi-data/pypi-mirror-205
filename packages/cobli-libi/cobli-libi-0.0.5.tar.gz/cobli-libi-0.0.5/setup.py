import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name='cobli-libi',
    version='0.0.5',
    description='Generate dataframes from Cobli public API',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Marcus Beckenkamp',
    author_email='mvbeck@gmai.com',
    url='https://docs.cobli.co',
    packages=['libi', ],
)
