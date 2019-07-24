import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randist",
    version="1.1.1",
    author="Ningji Wei",
    author_email="tidues@gmail.com",
    description="Distance statistics for two random events on a network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tidues/Distance-Distribution-of-Random-Events",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

