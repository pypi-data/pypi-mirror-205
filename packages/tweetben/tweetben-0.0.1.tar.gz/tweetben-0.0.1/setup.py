import setuptools

with open ('Readme.md', 'r') as file:
	long_description = file.read()

setuptools.setup(
	name = 'tweetben', #package name
	version = '0.0.1', #vesrion name 
	author = 'Behdad Ehsani', #author name
	author_email = 'behdad.ehsani@hec.ca', #email - contact
	description = 'This is for text preprocessing',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
	'Programming Language :: Python :: 3',
	'License :: OSI Approved :: MIT License',
	'Operating System :: OS Independent'],
	pyhton_requires = '>=3.5')#minimium python version needed)