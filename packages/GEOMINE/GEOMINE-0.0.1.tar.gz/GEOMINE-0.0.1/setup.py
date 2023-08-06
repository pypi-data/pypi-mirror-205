import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GEOMINE",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    authors= ["Colin Cleveland",'Chin-Yen Lee', 'Shen-Fu Tsai','Wei-Hsuan Yu','Hsuan-Wei Lee'],         # Full name of the author
    description="Orbits generator for colored directed graphs and orbits frequency finder",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["GEOMINE"],             # Name of the python package
    package_dir={'':'GEOMINE/src'},     # Directory of the source code of the package
    install_requires=['numpy','scipy']  # Install other dependencies if any
)