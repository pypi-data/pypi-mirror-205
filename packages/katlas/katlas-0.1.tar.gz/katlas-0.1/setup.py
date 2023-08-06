"""Setup"""

from setuptools import setup

setup(
    name='katlas', 
    version='0.1', 
    packages=[
        "katlas",
    ],
    entry_points={
        "console_scripts": [
            "katlas = katlas.cli:main",
        ],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)