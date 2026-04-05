"""Setup script for Tamil Tokenizer."""

from setuptools import setup, find_packages

setup(
    name="tamil_tokenizer",
    version="1.0.0",
    description="Multi-level tokenizer for Tamil text",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Tamil NLP Project",
    license="MIT",
    url="https://github.com/tamil-nlp/tamil-tokenizer",
    python_requires=">=3.8",
    packages=find_packages(),
    package_data={
        "tamil_tokenizer": ["data/*.list"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tamil-tokenize=tamil_tokenizer.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: Tamil",
        "Operating System :: OS Independent",
    ],
)
