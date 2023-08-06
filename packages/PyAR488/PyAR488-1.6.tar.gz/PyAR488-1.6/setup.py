from setuptools import setup, find_packages
import json


version_file = '_INTERNAL_version.json'


ver_data = json.load(open(version_file, 'r'))
local_build_version = ver_data['build']['ver']

setup(
    name='PyAR488',
    version=local_build_version,
    packages=find_packages(exclude=('_INTERNAL_build.py',
                                    '_INTERNAL_version.json',
                                    '.gitignore',
                                    'workspace.code-workspace')),
    url="https://github.com/Minu-IU3IRR/PyAR488",
    bugtrack_url = 'https://github.com/Minu-IU3IRR/PyAR488/issues',
    license='MIT',
    author='Manuel Minutello',
    description='module to interface AR488 boards',
    long_description=open('README.md').read(),
    install_requires=('pyserial'),
    python_requeres = '>=3.6'
)