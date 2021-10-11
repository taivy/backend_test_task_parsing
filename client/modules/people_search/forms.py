from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class PeopleSearchForm(FlaskForm):
    first_name = StringField("First Name: ")
    last_name = StringField("Last Name: ")
    middle_initial = StringField("Middle Initial: ")
    state = StringField("State: ")
    city = StringField("City: ")
    submit = SubmitField("Submit")
