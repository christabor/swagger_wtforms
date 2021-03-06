"""Parse/extract fields from swagger api specs."""

from flask_wtf import FlaskForm
from wtforms import validators

import type_mappers as mappers


def is_resource_collection(properties):
    """Determine if the resource is actually just a collection of resources.

    If so, it wouldn't need to be used for generating a form, since it's
    not a single resource.
    """
    for prop, conf in properties.items():
        if conf.get('type') == 'array' and 'items' in conf:
            return True
    return False


def get_forms_from_defs(defs,
                        exclude=[],
                        exclude_fields=[],
                        instantiate=True):
    """Take a definitions spec, and generate forms for each resource.

    This does NOT allow custom field exclusions on a PER-resource basis,
    only for shared field names (e.g. `id` or `creation_date`).
    """
    forms = dict()
    for resource, conf in defs.items():
        if resource in exclude:
            continue
        form = get_form_from_def(conf, exclude=exclude_fields)
        if instantiate and form is not None:
            form = form()
        if form is not None:
            forms[resource] = form
    return forms


def get_default_form():
    """Return default form class."""
    class SwaggerCustomForm(FlaskForm):
        pass

    return SwaggerCustomForm


def get_validators(prop, conf, required=[]):
    """Determine which validators to add for a field."""
    _validators = []

    min_len = conf.get('minLength')
    max_len = conf.get('maxLength')

    if prop in required or conf.get('required'):
        _validators.append(validators.DataRequired())

    # Deal with max/min lengths
    if min_len is None and max_len is not None:
        _validators.append(validators.Length(max=max_len))
    elif min_len is not None and max_len is None:
        _validators.append(validators.Length(min=min_len))
    elif min_len is not None and max_len is not None:
        _validators.append(validators.Length(min=min_len, max=max_len))
    return _validators


def get_url_for_resource(spec, resource):
    """Get the proper URL for a resource definition."""
    defs = spec.get('definitions')
    if defs is None:
        raise ValueError('Invalid definitions or spec.')
    resc = defs.get(resource)
    if resc is None:
        raise ValueError('Invalid resource definition: "{}"!'.format(resource))
    return ''


def get_form_from_path(path, method, paths, exclude=[]):
    """Take a path spec, grab props and make it into a form."""
    method = method.lower()
    custom_form = get_default_form()
    path_spec = paths.get(path)
    if path_spec is None:
        raise ValueError('Invalid API endpoint: {}'.format(path))
    spec = path_spec.get(method)
    if spec is None:
        raise ValueError('Invalid verb. This API endpoint '
                         'doesn\'t support "{}"'.format(method))
    param_spec = spec.get('parameters')
    # Convert to a dict to match the format of the definition spec.
    param_spec = {item['name']: item for item in param_spec}
    custom_form = set_fields(custom_form, param_spec)
    return custom_form


def get_collection_fmt_desc(colltype):
    """Return the appropriate description for a collection type.

    E.g. tsv needs to indicate that the items should be tab separated,
    csv comma separated, etc...
    """
    seps = dict(
        csv='Multiple items can be separated with a comma',
        ssv='Multiple items can be separated with a space',
        tsv='Multiple items can be separated with a tab',
        pipes='Multiple items can be separated with a pipe (|)',
        multi='',
    )
    if colltype in seps:
        return seps[colltype]
    return ''


def get_mapped_field(typ):
    """Get the equivalently mapped type."""
    try:
        return mappers.get_context_field(typ, 'wtforms')
    except:
        return


def fmt_given_desc(desc):
    """Additional formatting for a web UI with the base description."""
    # Ensure always ends with period.
    if not desc.endswith('.'):
        desc += '.'
    # Capitalize first letter.
    desc = '{}{}'.format(desc[0].upper(), desc[1:])
    return desc


def set_fields(form, properties, exclude=[], required_fields=[]):
    """Set fields for a path spec OR a definition spec."""
    for prop, conf in properties.items():
        # Allow excluding of any fields.
        if prop in exclude:
            continue
        typ = conf['type']
        default = conf.get('default', '')
        title = conf.get('title')
        enum = conf.get('enum')
        desc = fmt_given_desc(conf.get('description', ''))
        is_collection = conf.get('items')
        coll_fmt = conf.get('collectionFormat')

        if typ == 'array':
            # This needs to be text-field so
            # users can add comma/tab/etc separated items.
            # This one does not map very well so it's an edge case.
            typ = 'str'

        if enum is not None:
            typ = 'enum'

        mapped = get_mapped_field(typ)

        if is_collection and coll_fmt:
            desc = '{} {}'.format(desc, get_collection_fmt_desc(coll_fmt))

        if mapped is not None:
            validators = get_validators(prop, conf, required=required_fields)
            kwargs = dict(
                default=default,
                validators=validators,
                # TODO: handle markdown descriptions etc.
                description=desc,
            )
            if enum is not None:
                kwargs.update(choices=[(c, c) for c in enum])
            if title is not None:
                mapped = mapped(title, **kwargs)
            else:
                mapped = mapped(**kwargs)
        setattr(form, prop, mapped)
    return form


def get_form_from_def(definition, exclude=[]):
    """Take a spec, grab the props and make it into a form."""
    custom_form = get_default_form()

    required_fields = definition.get('required', [])
    properties = definition.get('properties', {})

    # Exclude collections
    if is_resource_collection(properties):
        return

    custom_form = set_fields(
        custom_form,
        properties,
        exclude=exclude,
        required_fields=required_fields)
    return custom_form
