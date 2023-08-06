import os
from setuptools import setup, find_packages
from packaging.version import Version

DESCRIPTION = 'vishali first Python package'
LONG_DESCRIPTION = 'vishali first Python package with a slightly longer description'

version_string = os.environ.get("EXAMPLE_VERSION", "0.0.0.dev0")
version = Version(version_string)

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="JustTry", 
        version=str(version),
        author="Vishali",
        author_email="vishali.nagathevan@gmail.com",
        description="This is very basic",
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
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