import string

from functools import reduce

from ckan.logic import ValidationError

from ckanext.datapackage_creator.settings import settings


def validate_resource(data):
    errors = {}
    name = data.get('name', '')
    check_slug = lambda x, y: x and (y in string.ascii_lowercase or y in ['.', '-', '_'] or y.isdigit())
    if not name:
        errors['Name'] = ['This field is required']
    elif not reduce(check_slug, name, True):
        errors['Name'] = [
            'It must consist only of lowercase alphanumeric characters plus “.”, “-” and “_”.'
        ]
    fields_required = settings.get('resource', {}).get('required', [])
    for field in fields_required:
        value = data.get(field)
        if not value:
            errors[field.capitalize()] = ['This field is required']
    if errors:
        error_summary = {k: ', '.join(v) for k, v in errors.items()}
        raise ValidationError(errors=errors, error_summary=error_summary)


def validate_package(data):
    errors = {}
    title = data.get('title')
    if not title:
        errors['Title'] = ['This field is required']
    notes = data.get('notes')
    if not notes:
        errors['Description'] = ['This field is required']
    tags = data.get('tags')
    if not tags:
        errors['Tags'] = ['This field is required']
    license = data.get('license_id')
    if not license:
        errors['LIcense'] = ['This field is required']
    author = data.get('author')
    if not author:
        errors['Author'] = ['This field is required']
    author_email = data.get('author_email')
    if not author_email:
        errors['Author E-mail'] = ['This field is required']
    if errors:
        error_summary = {k: ', '.join(v) for k, v in errors.items()}
        raise ValidationError(errors=errors, error_summary=error_summary)
