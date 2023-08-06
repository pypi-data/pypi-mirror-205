from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='RunRate',
  version='0.0.5',
  description='A very basic discount calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pradeep Tej Dandikuppam Sreenivasulu',
  author_email='x21196303@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='Cricket', 
  packages=find_packages(),
  install_requires=[''] 
)