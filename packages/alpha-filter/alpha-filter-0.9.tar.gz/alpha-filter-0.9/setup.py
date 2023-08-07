from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='alpha-filter',
    version='0.9',
    description='differential filter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['alphafilter'],
    python_requires='>=3.8'
)