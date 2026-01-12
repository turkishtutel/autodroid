from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autodroid",
    version="3",
    author="turkishcoder",
    description="A python module to automate android",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=find_packages(),
    install_requires=[
        "os", "requests", "zipfile", "subprocess", "datetime"
    ],
)
