import os
import io

from setuptools import setup, find_packages


def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding="utf-8").read().strip()
    return contents


README = read("README.md")


setup(
    name='''ckanext-datapackage-creator''',
    version='0.0.45',
    description='''Data Package Creator.''',
    long_description=README,
    long_description_content_type="text/markdown",
    author='''Transparência Minas Gerais''',
    license='AGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='''CKAN''',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    namespace_packages=['ckanext'],
    install_requires=[
        'frictionless==4.40.8',
        'jsonschema',
        'python-slugify',
        'frictionless_ckan_mapper',
        'openpyxl',
        'xlrd',
    ],
    include_package_data=True,
    package_data={
    },
    data_files=[],
    entry_points={
        'ckan.plugins': [
            'datapackage_creator=ckanext.datapackage_creator.plugin:DatapackageCreatorPlugin'
        ],
    },
)