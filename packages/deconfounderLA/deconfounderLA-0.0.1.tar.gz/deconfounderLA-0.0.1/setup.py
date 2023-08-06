from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='deconfounderLA',
  version='0.0.1',
  description='Functions needed to perform causal inference',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Leila Sofía Asplanato',
  author_email='lasplanato@unsam.edu.ar',
  license='MIT', 
  classifiers=classifiers,
  keywords='causal inference', 
  packages=find_packages(),
  install_requires=[''] 
)
