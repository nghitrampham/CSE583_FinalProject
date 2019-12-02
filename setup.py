import os
from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(
    name='air_pollution_and_death_related',
    version='1.0',
    url='https://github.com/nghitrampham/CSE583_FinalProject',
    license='MIT',
    author='Tram Nghi Pham, Brandon Pratt, Siting Wang, and Marta Wolfshorndl',
    author_email='martaw@uw.edu'
    description='Connection between air pollution and death rates by respiratory illness',
    packages=PACKAGES
    package_data={'air_pollution_and_death_related': ['Scripts/*', 'data/*']}
)

if __name__ == '__main__':
    setup(**opts)
