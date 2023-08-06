import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Screeny",                         # Name of the package
    version="0.0.1",                        # The initial release version
    author="Paul Pol",                      # Full name of the author
    description="A simple python library for working with screens and images.",
    long_description=long_description,      # Long description read from the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.11',               # Minimum version requirement of the package
    py_modules=["screeny"],                 # Name of the python package
    package_dir={'':'screeny/src'},         # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)