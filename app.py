"""Testing app."""

import os
import json

from flask import (
    Flask,
    render_template,
    request,
)

from yaml import load
from flask_extras import FlaskExtras

import swagger_gen

cwd = os.getcwd()
app = Flask('swagger-wtforms-test')
app.config['SECRET_KEY'] = '123'
FlaskExtras(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage."""
    filename = 'petstore-expanded.yaml'
    filepath = cwd + '/example_specs/' + filename
    spec = load(open(filepath, 'r').read())
    paths = spec.get('paths')
    product_form = swagger_gen.get_form_from_path('/pets', 'get', paths)
    form = product_form()
    if request.method == 'POST':
        # Trigger errors for testing
        form.validate_on_submit()
    kwargs = dict(
        url='/pets',
        spec=json.dumps(spec, indent=4),
        form=form,
        file=filename,
        name='Endpoint form'
    )
    return render_template('pages/index.html', **kwargs)


@app.route('/multiple', methods=['GET', 'POST'])
def multiple():
    """Multiple forms for all defs."""
    filename = 'uber.yaml'
    filepath = cwd + '/example_specs/' + filename
    spec = load(open(filepath, 'r').read())
    defs = spec.get('definitions')
    forms = swagger_gen.get_forms_from_defs(defs, exclude=['Error'])
    if request.method == 'POST':
        # Trigger errors for testing
        for _, form in forms.items():
            form.validate_on_submit()
    kwargs = dict(
        forms=forms,
        file=filename,
        spec=json.dumps(spec, indent=4),
    )
    return render_template('pages/multiple.html', **kwargs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
