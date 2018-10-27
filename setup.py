from setuptools import find_packages
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='config-logger',
      version='1.1.1',
      description='A simple configurable logger for python projects',
      long_description=readme(),
      url='https://github.com/afxentios/config-logger',
      license='MIT',
      author='Afxentios Hadjiminas',
      author_email='afxentios@hadjimina.com',
      keywords=['logging', 'configurable', 'configuration'],
      packages=find_packages(),
      install_requires=['pyyaml',
                        'config-manager'],
      extras_require={
          'test': ['unittest2',
                   'mock',
                   'testfixtures']
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules']
      )
