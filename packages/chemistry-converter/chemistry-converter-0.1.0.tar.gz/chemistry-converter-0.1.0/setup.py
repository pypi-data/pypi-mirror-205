from setuptools import setup, find_packages

setup(name='chemistry-converter',
      version='0.1.0',
      packages=find_packages(),
      install_requires=['chempy'],
      entry_points={
        'console_scripts':
        ['grams_to_moles = chemistry_converter.converter:main']
      })
