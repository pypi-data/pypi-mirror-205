import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kwanex",
    version="1.3.0",
    author="KhalidAghrini",
    author_email="kwaaghrini@gmail.com",
    description="A powerful scientific strings-processing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "nltk",
        "afinn",
        "tqdm",
        "wheel"
    ],
)
