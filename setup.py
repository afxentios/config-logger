from setuptools import setup, find_packages

import config_logger


def readme():
    with open("README.rst") as f:
        return f.read()


setup(name='config-logger',
      version=config_logger.__version__,
      description='A simple configurable logger for python projects',
      long_description=readme(),
      url='https://github.com/afxentios/config-logger',
      license='MIT',
      author=config_logger.__author__,
      author_email='afxentios@hadjimina.com',
      keywords=["logging", "configurable", "configuration"],
      packages=find_packages(),
      install_requires=['logging', 'PyYAML', 'config-manager', 'testfixtures'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules']
      )
