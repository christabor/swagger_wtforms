# Swagger-wtforms

Generate wtforms from swagger specs.

**This project is not stable and will likely change rapidly**.

GOAL: Generate wtforms forms for use in custom UIs by using pre-defined swagger specs.

## Requirements

### Form scenarios

#### Basic forms

Forms with simple fields, not much going on.

```python
class Myform(FlaskForm):
    field1 = TextField('..')
    field2 = TextField('..')
```

#### Complex forms

More complex usage;

1. Custom validators
2. Regular validators
3. Mix of all field types

```python
class Myform(FlaskForm):
    field1 = TextField('..', validators=[])
    field2 = IntegerField('..', validators=[])
    field3 = HiddenField()
    field4 = MultiSelectField(choices=[])

    def validate_field4(...):
        pass
```

#### Multi-page/post forms

e.g. flask_extras MultiStepWizard, where data is stored in session across POSTs.

#### Model forms

1. Third-party wtforms integration (e.g. wtforms-alchemy) - does this even make sense? The form is generated automagically already, and this might be too much magic, or simply competing.

#### Composition of any of the above form scenarios

### Operations

1. Must be able to map a field A -> B for equivalent type (e.g. int to IntegerField)
2. Allow custom validators
3. Deal with validation using spec.
4. Deal with hiding fields (some fields shouldn't necessarily be expose in forms)
    1. Deal with pks/fks
    2. Deal with read-only fields or auto-updated fields (creation_date, last_updated, etc)
5. Deal with determining upload fields
6. Have exclude option for some definitions

Integrate where appropriate, all fields in:
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#schema-object

Integrate all fields into mapper:
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types

Integrate custom field types from 3rd party (e.g. emailfield, colorpicker, etc...)
