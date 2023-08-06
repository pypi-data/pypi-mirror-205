from setuptools import setup, find_packages

VERSION = '0.1.0    ' 
DESCRIPTION = 'My test Python package'
LONG_DESCRIPTION = 'My test Python package with description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="vijaikfirstpackage", 
        version=VERSION,
        author="Vijai Kannan",
        author_email="vijaik.nd@gmail.com",
        description="Setting up a python package",
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'test package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)