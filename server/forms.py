from flask import request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired

class DeckImportForm(FlaskForm):
	deck_box = TextAreaField('Import from Arena', validators=[DataRequired()])
	submit = SubmitField('Import deck')

class SearchForm(FlaskForm):
	q = StringField('Search', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		if 'formdata' not in kwargs:
			kwargs['formdata'] = request.args
		if 'csrf_enabled' not in kwargs:
			kwargs['csrf_enabled'] = False
		super(SearchForm, self).__init__(*args, **kwargs)