from setuptools import setup

setup(
    name="searchlight",
    version="0.0.1",
    description="A suite of tools for accessing data in Searchlight",
    url="https://github.com/Conductor/searchlight-api-client-python",
    author="Dan Goodman",
    author_email="dgoodman@conductor.com",
    packages=[
        "searchlight",
        "searchlight.utils",
    ],
    install_requires=[
        "simplejson>=3.11.1",
        "requests>=2.19.1",
    ],
    zip_safe=False,
)
