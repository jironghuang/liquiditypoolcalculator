#In this directory, type pip install .
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='liquiditypoolcalculator',
      version='0.0.7',
      description='Liquidity pool value simulator',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/jironghuang/liquiditypoolcalculator",
      packages=['liquiditypoolcalculator'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
      python_requires='>=3.6',      
      author = 'Jirong Huang',
      author_email = 'jironghuang88@gmail.com',
      zip_safe=False)

