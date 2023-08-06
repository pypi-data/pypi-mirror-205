from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'REFRACT-IO: To read and write dataframe from different connectors.'
LONG_DESCRIPTION = '''
Usage:
without any dependencies: pip install refractio
with all dependencies: pip install refractio[all]
with snowflake: pip install refractio[snowflake]
with s3: pip install refractio[s3]
with azureblob: pip install refractio[azureblob]
with local: pip install refractio[local]
with sftp: pip install refractio[sftp]
with mysql: pip install refractio[mysql]

Source code is also available at: https://git.lti-aiq.in/refract-sdk/refract-sdk.git
'''

extras_require = {
    "all": [
        "snowflake-connector-python[pandas]==3.0.2",
        "boto3==1.26.116",
        "azure==4.0.0",
        "openpyxl==3.1.2",
        "xlrd==2.0.1",
        "pysftp==0.2.9",
        "pymysql==1.0.3"
    ],
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
    ],
    "mysql": [
        "pymysql==1.0.3"
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
    project_urls={
        "Product": "https://www.fosfor.com/refract/",
        "Source": "https://git.lti-aiq.in/refract-sdk/refract-sdk",
    }
)

