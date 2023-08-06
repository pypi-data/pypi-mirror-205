import io
import os
from setuptools import find_packages, setup
import battlemaster


def read(*paths, **kwargs):
    content = ""
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


setup(
    name="battlemaster",
    version=battlemaster.__version__,
    description="A library for a game of armored combat.",
    url="https://github.com/johnnystarr/battlemaster",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Johnny Starr",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[

    ],
    entry_points={
    },
)
