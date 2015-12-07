from setuptools import setup

setup(name='armada',
	version='1.0',
	url='https://github.com/sc4reful/armada',
	license='MIT',
	author='sc4reful',
	author_email='4b1a2059@opayq.com',
	description='Twisted parallel processing library',
	packages=['armada', 'armada.process'],
	zip_safe=False,
	platforms='any',
	install_requires=['Twisted'],
	classifiers = [
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Development Status :: 5 - Production/Stable',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
)