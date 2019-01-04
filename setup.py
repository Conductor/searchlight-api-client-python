from setuptools import setup, find_packages

with open("README.md") as f:
    description = f.read()

setup(
    name="searchlight",
    version="0.0.1",
    description="A client to assist in connecting with Searchlight's API",
    long_description=description,
    author="Dan Goodman",
    author_email="dgoodman@conductor.com",
    url="https://github.com/Conductor/searchlight-api-client-python",
    packages=find_packages(exclude=("docs", "searchlight.tests")),
    setup_requires=["nose==1.3.7"],
    install_requires=[
        "simplejson>=3.11.1",
        "requests>=2.19.1",
    ],
    zip_safe=False,
)
