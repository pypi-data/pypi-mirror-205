from setuptools import find_packages, setup

setup(
    name='gwpwall',
    packages=find_packages(include=['gwpwall']),
    version='1.0.0',
    description='Green-Wall-Project Wall package',
    author='Gal Sajko',
    license='MIT',
    install_requires=['numpy']
)