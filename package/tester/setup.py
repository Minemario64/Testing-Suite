from setuptools import setup, find_packages

setup(
    name="tester",
    version="1.0.0",
    description="An automated tester.",
    packages=find_packages(),
    install_requires=[
        "rich",
        "shutil",
        "re",
        "math"
    ],
    author="Minemario64",
    classifiers=[
        'Programming Language :: Python :: 3.13'
    ]
)