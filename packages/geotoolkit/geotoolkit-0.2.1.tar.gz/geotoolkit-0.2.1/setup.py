from distutils.core import setup
import setuptools

with open("README.md", "r") as f:
    long_desc:str = f.read()

setup(name='geotoolkit',
    version='0.2.1',
    description='Peforming calculations with geographic points',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Tim Hanewich',
    url='https://github.com/TimHanewich/geotoolkit',
    packages=setuptools.find_packages()
    )