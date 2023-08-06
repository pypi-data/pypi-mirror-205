from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = "Modern Python Package To Handle Colors in Python"
LONG_DESCRIPTION = "Modern Python Package To Handle Colors in Python"

# Setting up
setup(
    name="pythoncolourlibraryV1",
    version=VERSION,
    author="knwnLegend",
    author_email="nick.faltermeier@gmx.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)