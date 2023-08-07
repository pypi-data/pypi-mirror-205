from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "requirements.txt"), "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="ssl-labs-screenshot",
    version="1.0.4",
    author="Mark Sowell",
    author_email="mark@marksowell.com",
    description="A script to capture SSL Labs server test report screenshots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marksowell/ssl-labs-screenshot",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ssl-labs-screenshot=ssl_labs_screenshot.__main__:main',
        ],
    },
)
