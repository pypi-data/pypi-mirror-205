#from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name = 'elastic_helper',
packages = ['elastic_helper'], # this must be the same as the name above
version = '1.2.4',
description = 'Elastic Search to Pandas Dataframe',
long_description=long_description,
long_description_content_type="text/markdown",
author = 'snuids',
author_email = 'snuids@mannekentech.com',
url = 'https://github.com/snuids/elastic_helper', 
download_url = 'https://github.com/snuids/elastic_helper/archive/1.2.4.tar.gz',
keywords = ['ElasticSearch', 'pandas', 'convert'], # arbitrary keywords
classifiers = ["License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"],
)