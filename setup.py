from setuptools import find_packages
from setuptools import setup

setup(
    name="pre-commit-hooks-msidp",
    description="Hooks for the Microsoft Intelligent Data Platform",
    url="https://github.com/fmms/pre-commit-msidp",
    version="0.0.1",
    author="Felix Möller",
    author_email="mail@felixmoeller.de",
    packages=find_packages("."),
    install_requires=[
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "sqlprojsort = pre_commit_hooks.sqlprojsort:main"
        ],
    },
)
