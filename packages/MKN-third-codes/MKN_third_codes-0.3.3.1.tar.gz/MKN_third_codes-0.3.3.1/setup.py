from setuptools import setup
import codecs

setup(
    name='MKN_third_codes',
    version='0.3.3.1',
    description='Python library with standart solutions for probability tasks',
    author='Dolgun Ivan',
    author_email='vanadolgun@gmail.com',
    packages=['MKN_third_codes/'],
    license='MIT',
    long_description= open('./README.md', 'r', encoding="utf-8").read(),
    long_description_content_type='text/markdown'
)