from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='shekhar_bmi_calculator',
  version='0.0.2',
  description='A very basic BMI calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sarvesh Shekhar',
  author_email='x22129880@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='bmi calculator', 
  packages=find_packages(),
  install_requires=[''] 
)