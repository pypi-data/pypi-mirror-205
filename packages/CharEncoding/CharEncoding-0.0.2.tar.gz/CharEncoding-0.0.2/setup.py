from setuptools import setup, find_packages
from setuptools import setup, Extension

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='CharEncoding',
  version='0.0.2',
  description='Character Encoding Algorithms',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/rishabhc9',  
  author='Rishabh Chopda',
  author_email='aaditchopda2@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=["Encoding","7-Segment Display", "ASCII85 Encoding", "ASCII Code", "Aztec Barcode", "Base-32 Crockford", "Base32", "Base45", "Base 58", "Base62", "Base64", "Base91", "Baudot", "Binary", "Chuck Norris Unary Code", "EBCDIC Encoding", "French Postal Barcode", "Gray Code", "Morse Code", "BCD Encoding", "Excess-3 Code (Stibitz)", "Resistor Value"], 
  packages=find_packages(),
  install_requires=[''] 
)