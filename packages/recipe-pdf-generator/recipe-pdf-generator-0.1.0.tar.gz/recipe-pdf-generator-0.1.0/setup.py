from setuptools import setup, find_packages

setup(
    name="recipe-pdf-generator",
    version="0.1.0",
    description="A library for generating PDF versions of recipes",
    packages=find_packages(),
    install_requires=["reportlab==3.6.1"],
)
