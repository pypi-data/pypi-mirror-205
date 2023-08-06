from setuptools import setup

setup(
    name="model_scraper",
    version="1.0.0",
    author="Henrik Knutsen",
    author_email="hknut99@gmail.com",
    description="Scrapes information model xml for models.",
    long_description="An xml parser that gathers useful information about each model in a package from the information model xml.",
    long_description_content_type="text/markdown",
    url="https://github.com/FINTLabs/fint-model-scraper",
    packages=["model_scraper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
