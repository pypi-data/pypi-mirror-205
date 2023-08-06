
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Data management package by using sqlite3.'
LONG_DESCRIPTION = DESCRIPTION

# Setting up
setup(
    name="SQLite3_0611",
    version=VERSION,
    author="Mengke Lu",
    author_email="<mklu0611@gmail.com>",
    description= DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'sqlite3'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)