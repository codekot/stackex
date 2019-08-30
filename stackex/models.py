from stackex import db
from datetime import datetime


class User_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    req_name = db.Column(db.String(), unique=True, nullable=False)
    req_results = db.relationship('Request_result',
                                  backref="on_request", lazy=True,
                                  cascade='all,delete')

    def __repr__(self):
        return f"User_request('{self.req_name}', {self.date})"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(req_name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def unix_date(self):
        pass

    def update_date(self):
        self.date = datetime.utcnow()


class Request_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    last_activity_date = db.Column(db.DateTime, default=None)
    link = db.Column(db.Text())
    request_id = db.Column(db.Integer,
                           db.ForeignKey('user_request.id', ondelete='CASCADE'),
                           nullable=False)

    def __repr__(self):
        return f"Request_result('{self.title}', '{self.last_activity_date}', '{self.link}'"

    @classmethod
    def write_data_to_db(cls, data, request_id):
        for datum in data:
            rr = Request_result(id=datum['question_id'],
                            title=datum['title'],
                            last_activity_date=datetime.
                                utcfromtimestamp(datum["last_activity_date"]),
                            link=datum["link"],
                            request_id=request_id)
            db.session.add(rr)
        db.session.commit()
