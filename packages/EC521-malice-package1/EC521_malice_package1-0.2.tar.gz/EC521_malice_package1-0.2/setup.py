from setuptools import setup, find_packages

setup(
    name='EC521_malice_package1',
    version='0.2',
    packages=find_packages(),
    package_data={
        '': ['__init__.py', 'mal_example.py']
    },
)
