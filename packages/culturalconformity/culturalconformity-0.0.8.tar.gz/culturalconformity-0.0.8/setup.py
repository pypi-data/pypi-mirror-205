from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'Simulations of conformity, anti-conformity, and unbiased frequency-dependent transmission'
# LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    name="culturalconformity",
    version=VERSION,
    author="Kaleda Denton",
    # author_email="kdenton@ucla.edu",
    description=DESCRIPTION,
    # long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    # keywords=['python', 'first package'],
    # classifiers=[
    #    "Development Status :: 3 - Alpha",
    #    "Intended Audience :: Education",
    #    "Programming Language :: Python :: 2",
    #    "Programming Language :: Python :: 3",
    #    "Operating System :: MacOS :: MacOS X",
    #    "Operating System :: Microsoft :: Windows",
    # ]
)
