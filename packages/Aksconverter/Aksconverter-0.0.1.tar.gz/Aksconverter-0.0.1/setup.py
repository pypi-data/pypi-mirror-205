from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='Aksconverter',
  version='0.0.1',
  description='A very currency calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Akshat Joshi',
  author_email='x22137696@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='Currency Calculator', 
  packages=find_packages(),
  install_requires=[''] 
)