from setuptools import setup, find_packages

setup(name='vivo_utils',
      packages=find_packages(),
      version='0.1',
      description='A collection of queries and tools for interacting with VIVO',
      author='Naomi Braun',
      author_email='naomi.d.braun@gmail.com',
      url='http://github.com/naomidb/vivo_utils',
      license='Apache License 2.0',
      install_requires=[
          'requests==2.18.4',
          'PyYAML==3.12',
          'Jinja2==2.10',
          'bibtexparser==1.0.1'],
      )

