from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, URL


# List Form
class ListForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class TaskForm(FlaskForm):
    description = StringField("Task", validators=[DataRequired()])
    submit = SubmitField("Add Task")

class DeleteListForm(FlaskForm):
    submit = SubmitField("Delete List")