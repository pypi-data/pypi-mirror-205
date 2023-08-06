from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'vishali first Python package'
LONG_DESCRIPTION = 'vishali first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="JustTry", 
        version=VERSION,
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