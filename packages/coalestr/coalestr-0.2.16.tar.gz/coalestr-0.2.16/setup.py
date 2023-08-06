from setuptools import setup, find_packages

VERSION = '0.2.16' 
DESCRIPTION = 'A Python package for implementing the genomic transmission graph'
LONG_DESCRIPTION = 'coalestr is a Python package for implementing the genomic transmission graph to model the transmission dynamics and genomic diversity of a recombining parasite population. You can find tutorials and worked examples at https://d-kwiat.github.io/gtg/'

# Setting up
setup(
       # the name must match the folder name'
        name="coalestr", 
        version=VERSION,
        author="Dominic Kwiatkowski",
        author_email="<dkwiatkowski@sjc.ox.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'matplotlib'],         
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)