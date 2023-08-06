from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'REFRACT IO'
LONG_DESCRIPTION = 'To read and write dataframe from different connectors'

extras_require = {
    "snowflake": [
        "snowflake-connector-python[pandas]==3.0.2"
    ],
    "s3": [
        "boto3==1.26.116"
    ],
    "azureblob": [
        "azure==4.0.0"
    ],
    "local": [
        "openpyxl==3.1.2",
        "xlrd==2.0.1",
    ],
    "sftp": [
        "pysftp==0.2.9"
    ]
}

# Setting up
setup(
    name="refractio",
    version=VERSION,
    author="Abhishek Chaurasia",
    author_email="<abhishek1.chaurasia@fosfor.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas==2.0.0"
    ],
    keywords=['refractio'],
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    extras_require=extras_require,
)