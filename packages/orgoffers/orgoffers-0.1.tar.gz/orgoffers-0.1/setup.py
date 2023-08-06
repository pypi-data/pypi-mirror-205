from setuptools import setup, find_packages

setup(
    name='orgoffers',
    version='0.1',
    description='A library that displays one grocery every 24 hours from a list of groceries',
    author='Challa Sravanthi',
    author_email='x21156239@student.ncirl.ie',
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