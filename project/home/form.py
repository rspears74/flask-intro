from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class MessageForm(Form):
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    description = StringField(
        'Description',
        validators=[DataRequired(), Length(max=140)]
    )
