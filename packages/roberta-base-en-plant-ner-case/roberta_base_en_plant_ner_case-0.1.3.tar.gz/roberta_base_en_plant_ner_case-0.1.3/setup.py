from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="roberta_base_en_plant_ner_case",
    version="0.1.3",
    author="Mohammad Othman",
    description="A spaCy NER model for plant entities using RoBERTa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourrepository",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=["spacy>=3.0"],
    include_package_data=True,
    python_requires=">=3.7",
)
