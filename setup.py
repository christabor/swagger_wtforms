"""
Setup for swagger-wtforms.

Generate wtform classes dynamically from swagger definition specifications.
"""

import os

from setuptools import setup

SRCDIR = '.'
folder = os.path.abspath(os.path.dirname(__file__))
test_requirements = [
    'pytest==3.0',
    'pytest-cov==2.4',
    'pyquery==1.2',
]
requirements = [
    'click==6.6',
    'Flask==0.10.1',
    'Flask-WTF==0.12',
    'itsdangerous==0.24',
    'Jinja2==2.8',
    'MarkupSafe==0.23',
    'Werkzeug==0.11.10',
    'WTForms==2.1',
]

setup(
    name='swagger_wtforms',
    version='0.0.1',
    description=('Generate wtforms classes from swagger specs.'),
    long_description=__doc__,
    author='Chris Tabor',
    author_email='dxdstudio@gmail.com',
    url='https://github.com/christabor/swagger_wtforms',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=test_requirements,
    install_requires=requirements,
    package_dir={'swagger_wtforms': 'swagger_wtforms'},
    packages=['swagger_wtforms'],
    zip_safe=False,
    include_package_data=True,
)
