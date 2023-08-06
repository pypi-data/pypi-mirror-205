from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='Taxation',
  version='0.0.1',
  description='This is very simple tax calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rishab ',
  author_email='x21171203@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='Taxation , Tax calculator', 
  packages=find_packages(),
  install_requires=[''] 
)