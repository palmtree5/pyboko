from distutils.core import setup
from setuptools import find_packages

setup(
    name="pyboko",
    version="0.2.0",
    packages=find_packages(include=["pyboko", "pyboko.*"]),
    license="GPLv3",
    install_requires=["aiohttp"],
    python_requires=">=3.7",
    author="Palm__",
    author_email="",
)