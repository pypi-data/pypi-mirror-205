from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="the_generic_crawler",
    version="0.1.0",
    description="A simple web scraper for downloading images, tables, and text from a webpage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Said Mohamed Amine",
    author_email="amine8said@gmail.com",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "pandas",
        "requests",
        "selenium",
        "tqdm",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
