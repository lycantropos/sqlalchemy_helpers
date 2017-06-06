from setuptools import (setup,
                        find_packages)

setup(name='sqlalchemy_helpers',
      packages=find_packages(),
      version='0.0.3',
      description='Helper functions for comfortable working with SQLAlchemy.',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url='https://github.com/lycantropos/sqlalchemy_helpers',
      download_url='https://github.com/lycantropos/sqlalchemy_helpers/archive/'
                   'master.tar.gz',
      keywords=['SQLAlchemy'],
      install_requires=['sqlalchemy>=1.1.6'])
