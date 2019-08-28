import json
from datetime import datetime
from stackex.models import User_request, Request_result
import requests
from stackex import db


def stack_request(req, fromdate=None):
    #global db
    url = "https://api.stackexchange.com/2.2/search"
    params = {
        "order": "desc",
        "sort": "activity",
        "intitle": req,
        "site": "stackoverflow"
    }
    if fromdate:
        params["fromdate"] = int(fromdate.timestamp())
    r = requests.get(url, params=params)
    data=r.json()
    data=data['items']
    if not data:
        return
    user_request = User_request.find_by_name(req)
    if user_request:
        user_request.update_date()
    else:
        u = User_request(date=datetime.utcnow(), req_name=req)
        db.session.add(u)
    db.session.commit()
    request_id = User_request.find_by_name(req).id
    Request_result.write_data_to_db(data, request_id)


if __name__ == '__main__':
    pass
