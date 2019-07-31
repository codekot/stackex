import json
from datetime import datetime
from stackex.models import User_request, Request_result
import requests
from stackex import db


def construct_list():
    data_file = 'search.json'
    data = None

    with open(data_file, "r") as json_file:
        data = json.load(json_file)

    items = data['items']
    result = [[item['question_id'],
               item['title'],
               datetime.utcfromtimestamp(item["last_activity_date"]),
               item["link"]] for item in items]
    return result


def populate(db):
    u = User_request(id=1, date=datetime.utcnow(), req_name="java")
    db.session.add(u)
    data = construct_list()
    for datum in data:
        rr = Request_result(id=datum[0],
                            title=datum[1],
                            last_activity_date=datum[2],
                            link=datum[3],
                            request_id=1)
        db.session.add(rr)
    db.session.commit()
    print("Database is populated")

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
