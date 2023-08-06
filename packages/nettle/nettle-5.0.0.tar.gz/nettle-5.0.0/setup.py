from setuptools import setup, find_packages

setup(
    name="nettle",
    version="5.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    scripts=['pingback.py']
)
