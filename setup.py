from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='tfl_status',
      version="0.0.1",
      description="TFL status checker (tube/overground)",
      author="Mischa Dhar",
      author_email="mischadhar94@gmail,com",
      url="https://github.com/MDhar94/journey_planner",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
