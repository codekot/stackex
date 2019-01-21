from stackex import db
from datetime import datetime


class User_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    req_name = db.Column(db.String(), unique=True, nullable=False)
    req_results = db.relationship('Request_result',
                                  backref="on_request", lazy=True)

    def __repr__(self):
        return f"User_request('{self.req_name}', {self.date})"


class Request_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    last_activity_date = db.Column(db.DateTime, default=None)
    link = db.Column(db.Text())
    request_id = db.Column(db.Integer,
                           db.ForeignKey('user_request.id'),
                           nullable=False)

    def __repr__(self):
        return f"Request_result('{self.title}', '{self.date}')"
