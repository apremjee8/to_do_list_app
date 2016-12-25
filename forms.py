from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from models import Entry


class EntryForm(FlaskForm):
    entry = TextAreaField(
        'Add To-Do',
        validators=[
            DataRequired()
        ]
    )


class UpdateForm(FlaskForm):
    entry = TextAreaField(
        'Update To-Do',
        validators=[
            DataRequired()
        ]
    )

class WorkspaceForm(FlaskForm):
    workspace = TextAreaField(
        'Create New Workspace',
        validators=[
            DataRequired()
        ]
    )
