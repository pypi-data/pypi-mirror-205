from setuptools import setup

required_packages = [
  "torch",
]

with open("README.md", "r") as f:
  long_description = f.read()

setup(
  name="empirical_init",
  version="0.0.2",
  description="Automatically initialize weights in pytorch modules using a hacky empirical method.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pb1729/empirical-init",
  author="Phillip Bement",
  author_email="{author_first_name}{author_last_initial}@fastmail.com",
  license="BSD 3-clause",
  packages=["empirical_init"],
  install_requires=required_packages,
)

