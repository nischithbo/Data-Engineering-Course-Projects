from setuptools import setup, find_packages

setup(
	name='assignment2',
	version='1.0',
	author='Nischith Bairannanavara Omprakash',
	author_email='nischith.bairann@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
