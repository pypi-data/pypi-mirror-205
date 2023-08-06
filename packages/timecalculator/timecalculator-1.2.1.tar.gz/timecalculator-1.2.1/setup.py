from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Operating System :: Microsoft :: Windows :: Windows 10",
]

setup(
    name="timecalculator",
    version="1.2.1",
    packages=find_packages(),
    description="A Python package for converting time units to seconds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Xyndra",
    author_email="sammy@deutschergamingserver.de",
    license="MIT",
    url="https://github.com/Xyndra/Timecalculator",
    keywords=["time", "calculator"],
    classifiers=classifiers,
)
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# py setup.py sdist
