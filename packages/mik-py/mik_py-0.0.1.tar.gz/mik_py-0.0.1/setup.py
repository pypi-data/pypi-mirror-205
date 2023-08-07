import os
import setuptools
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name="mik_py",
    version="0.0.1",
    author="Mike",
    author_email="mike@gmail.com",
    description="eicar test package",
    long_description="eicar test package",
    long_description_content_type="text/markdown",
    #url="www.test.com",
    packages=find_packages(),
    include_package_data=True,
    packages_data={
        'eicar_py':['eicar.com'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)