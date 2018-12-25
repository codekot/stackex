from stackex import db
from datetime import datetime


class User_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    req_name = db.Column(db.String(), unique=True, nullable=False)
    # req_results = db.relationship('RequestResult',
    # backref="on_request", lazy=True)

    def __repr__(self):
        return f"User request on subject '{self.req_name}' posted on \
                {self.date}"


class Request_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False, default="some time")
    # date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    link = db.Column(db.Text())
    request_id = db.Column(db.Integer,
                           db.ForeignKey('user_request.id'),
                           nullable=False)

    def __repr__(self):
        return f"RequestResult '{self.title}', '{self.date_posted}'"
