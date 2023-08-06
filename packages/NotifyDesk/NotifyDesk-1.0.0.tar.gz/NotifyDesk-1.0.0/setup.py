from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='NotifyDesk',
  version='1.0.0',
  author='krator3',
  author_email='maxostapenko567@gmail.com',
  description='The NotifyDesk library provides an easy way to send notifications in Linux',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/krator3/NotifyDesk',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux'
  ],
  platforms=["Linux"],
  keywords='python linux notifications notification',
  python_requires='>=3.0'
)
