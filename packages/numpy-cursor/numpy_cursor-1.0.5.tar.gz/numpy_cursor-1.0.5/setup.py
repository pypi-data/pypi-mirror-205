from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='numpy_cursor',
  version='1.0.5',
  author='nikgariel',
  author_email='nikgariel@yahoo.com',
  description='This package contains a Python implementation of a cursor for NumPy matrices. The cursor allows you to conveniently move through a matrix and read or modify its values.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/NikGariel/NumPy-Cursor',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
  keywords='numpy python cursor matrix',
  project_urls={},
  python_requires='>=3.8',
  py_modules=["numpy_cursor"],
  package_dir={'':'src'},
)