from setuptools import setup

def readme():
	with open('README.txt', 'r')  as f:
		return f.read() 

def short_readme():
	with open('README.md', 'r')  as f1:
		return f1.read()
    	
setup(name='matrix_package',
	version='22.03.11',
	description = short_readme() , 
	long_description = readme(),
	url='https://github.com/amieheessomba',
	author='Iréné Amiehe-Essomba ',
	keywords = 'molecular dynamics matrix package',
	install_requires = [
	'markdown',
	],
	classifier = [
	'Licence :: OSI Approved :: IPCMS Licence',
	'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
	'Program Language :: Python :: version >= 3.8',
	'Topic :: Molecular Dynamics Analysics code',
	],   
	test_suite = 'nose.collector',
	include_package_data = True, 
	author_email='ibamieheessomba@unistra.fr',
	license='IPCMS',
	packages=['matrix_package'],
	zip_safe=False)


	
	
	
	
	
	
	
	
	
