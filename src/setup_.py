import pypandoc
import setuptools

long_description = pypandoc.convert_file("../README.org", "md")

setuptools.setup(
    name="bridge-sim-barischrooneyj",  # Replace with your own username
    version="0.0.5",
    author="Jeremy Barisch-Rooney",
    author_email="barischrooneyj@protonmail.com",
    description="A Python library for concrete slab bridge simulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/barischrooneyj/bridge-sim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
