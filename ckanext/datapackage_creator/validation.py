from ckan.logic import ValidationError


def validate_resource(data):
    errors = {}
    title = data.get('title')
    if not title:
        errors['Title'] = ['Missing value']
    description = data.get('description')
    if not description:
        errors['Description'] = ['Missing value']
    if errors:
        error_summary = {k: ', '.join(v) for k, v in errors.items()}
        raise ValidationError(errors=errors, error_summary=error_summary)
