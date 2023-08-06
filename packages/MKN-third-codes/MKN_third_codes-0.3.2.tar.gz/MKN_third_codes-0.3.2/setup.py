from setuptools import setup
import codecs

setup(
    name='MKN_third_codes',
    version='0.3.2',
    description='Python library with standart solutions for probability tasks',
    author='Dolgun Ivan',
    author_email='vanadolgun@gmail.com',
    packages=['MKN_third_codes/'],
    license='MIT',
    long_description=codecs.open("./README.md", "r", "utf_8_sig").read()
)