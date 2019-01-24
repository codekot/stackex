from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from stackex.models import User_request


class NewRequestForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Search')

    def validate_search(self, search):
    	user_request = User_request.query.filter_by(req_name=search.data).first()
    	print(user_request)
    	if user_request:
    		raise ValidationError('This request is already exist in database')
