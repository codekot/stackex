import json
from datetime import datetime
from stackex.models import User_request, Request_result
import requests
from stackex import db


def stack_request(req):
    #global db
    url = "https://api.stackexchange.com/2.2/search"
    params = {
        "order": "desc",
        "sort": "activity",
        "intitle": req,
        "site": "stackoverflow"
    }
    r = requests.get(url, params=params)
    data=r.json()
    data=data['items']
    if not data:
        return
    u = User_request(date=datetime.utcnow(), req_name=req)
    db.session.add(u)
    db.session.commit()
    find_request = User_request.query.filter_by(req_name=req).first().id
    for datum in data:
        rr = Request_result(id=datum['question_id'],
                            title=datum['title'],
                            last_activity_date=datetime.
                                utcfromtimestamp(datum["last_activity_date"]),
                            link=datum["link"],
                            request_id=find_request)
        db.session.add(rr)
    db.session.commit()
    

if __name__ == '__main__':
    pass
