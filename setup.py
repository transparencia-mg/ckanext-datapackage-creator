from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))


setup(
    name='''ckanext-datapackage-creator''',
    version='0.0.3',
    description='''Data Package Creator.''',
    author='''Transparência Mineas Gerais''',
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