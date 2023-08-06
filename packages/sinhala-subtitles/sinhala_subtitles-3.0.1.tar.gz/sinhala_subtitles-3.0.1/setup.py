from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sinhala_subtitles",
    version="3.0.1",
    author="Gavindu Tharaka",
    author_email="gavi.tharaka@gmail.com",
    description="This Python library is designed to make downloading Sinhala subtitles for TV series and movies easy. To use it, simply install the library using pip and import it into your Python script.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["sinhala_subtitles"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['bs4'],
)
