from setuptools import setup, find_packages

setup(
    name='simple_distance_calculator',
    version='0.0.1',
    author='Aivcho',
    author_email='achomskis@gmail.com',
    description='A distance calculator',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)