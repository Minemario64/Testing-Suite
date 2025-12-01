from setuptools import setup, find_packages

setup(
    name="tester",
    version="1.0.1",
    description="An automated tester.",
    packages=find_packages(),
    install_requires=[
        "rich"
    ],
    author="Minemario64",
    classifiers=[
        'Programming Language :: Python :: 3.13'
    ]
)