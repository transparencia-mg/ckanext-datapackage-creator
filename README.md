# CKNEXT Data Package Creator

CKAN extension to use the fritioncless library


## Table of Contents

  * [Publish or Update Package to Pypi](#publish-or-update-package-to-pypi)
  * [Installation](#installation)
  * [Configuration](#configuration)

## Publish or Update Package to Pypi

- Check the last version published on [Pypi](https://pypi.org/project/ckanext-datapackage-creator/).
- Update `CHANGELOG.md` file with a short review of what had been done.
- Update `setup.py` file with the new version number.
- Commit all the above changes with the new version number (one above that publish on Pypi). Example: `git commit -am 'v0.1.1'`.
- Push the created commit to the online repository: Example: `git push origin master`.
- Create a new tag with the new version number (same as used to commit last changes). Example: `git tag v0.1.1 HEAD`.
- Push the new created tag to the online repository: Example: `git push origin v0.1.1`.
- Publish on Pypi with `make update-package`.


## Instalation

```
pip install ckanext-datapackage-creator
```


## Configuration

Once installed, add the `datapackage_creator` plugin to the `ckan.plugins` configuration option in your INI file.

```
ckan.plugins = ... datapackage_creator
```

# Datapackage Creator Configuration

The plugin allows you to configure which fields of the resource and package are mandatory and/or 'readonly', for this you just need to add a configuration in your INI file.


```
datapackage_creator = /path/to/datapackage_creator.json
```

We suggest that the file path would be `/etc/ckan/default/datapackage_creator.json` or in the same folder as `ckan.ini` file.

Configuration example file:

```
{
    "package": {
        "required": [],
        "readonly": []
    },
    "resource": {
        "required": [],
        "readonly": []
    }
}
```
