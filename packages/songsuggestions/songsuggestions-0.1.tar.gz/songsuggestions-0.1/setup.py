from setuptools import setup, find_packages

setup(
    name='songsuggestions',
    version='0.1',
    description='A library that suggest random songs to the user',
    author='Anuhya Kodam',
    author_email='anuhyakodamir25@gmail.com',
    packages=find_packages(),
    install_requires=[
        'datetime',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)