from setuptools import (setup,
                        find_packages)

import sqlalchemy_helpers
from sqlalchemy_helpers.config import PROJECT_NAME

project_base_url = 'https://github.com/lycantropos/sqlalchemy_helpers/'
setup(name=PROJECT_NAME,
      version=sqlalchemy_helpers.__version__,
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.tar.gz',
      description=sqlalchemy_helpers.__doc__,
      long_description=open('README.rst').read(),
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Database :: Database Engines/Servers',
      ],
      packages=find_packages(exclude=('tests',)),
      keywords=['SQLAlchemy'],
      install_requires=['sqlalchemy>=1.1.6'],
      setup_requires=['pytest-runner>=2.11'],
      tests_require=[
          'pydevd>=1.0.0',  # debugging
          'psycopg2>=2.7.3.1',  # PostgreSQL driver
          'PyMySQL>=0.7.11',  # MySQL driver
          'sqlalchemy_utils==0.32.16',  # database creation/destruction
          'pytest>=3.0.5',
          'pytest-cov>=2.4.0',
          'hypothesis>=3.13.0',
      ])
