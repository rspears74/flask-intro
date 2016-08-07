from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
ValidationError
from project import db
from project.models import User


class IsAlphaNum(object):
    def __call__(self, form, field):
        if field.data.isalnum() == False:
            raise ValidationError(
                'Username must contain only letters and numbers'
            )


class IsUnique(object):
    def __init__(self, db_field=None):
        self.db_field = db_field

    def __call__(self, form, field):
        key = self.db_field
        params = { key: field.data}
        if User.query.filter_by(**params).first() is not None:
            raise ValidationError('Sorry, that {} is taken.'.format(key))


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            IsUnique(db_field='name'),
            IsAlphaNum()
        ]
    )
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
            IsUnique(db_field='email')
        ]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'confirm',
        validators=[
        DataRequired(), EqualTo('password',message='Passwords must match.')
        ]
    )
