# encoding: utf-8
# @time :  2023-04-29 17:07:00
# @file : setup.py
# @author : Ading
# Official Account: AdingBLOG
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="test-ading",
  version="0.0.1",
  author="Example Author",
  author_email="author@example.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)