import json
from datetime import datetime
from stackex.models import User_request, Request_result
import requests
from stackex import db

def save_to_json(data):
    with open('result.json', 'w') as fp:
        json.dump(data, fp)
    print("Data written in result.json")


def make_request(parameters):
    url = "https://api.stackexchange.com/2.2/search"
    result = requests.get(url, params=parameters)

    return result.json()

def get_data(parameters):
    result = []
    if parameters["fromdate"]:
        while True:
            data = make_request(parameters)
            result.extend(data["items"])
            if not data["has_more"]:
                break
            parameters["page"] += 1
        return result
    else:
        return make_request(parameters)["items"]


def stack_request(req, fromdate=None):
    params = {
        "order": "desc",
        "sort": "activity",
        "intitle": req,
        "site": "stackoverflow",
        "page": 1,
        "pagesize": 100,
        }
    if fromdate:
        params["fromdate"] = int(fromdate.timestamp())
    data = get_data(params)

    if not data:
        return
    user_request = User_request.find_by_name(req)
    if user_request:
        user_request.update_date()
    else:
        user_request = User_request(date=datetime.utcnow(), req_name=req)
        user_request.save()
    request_id = User_request.find_by_name(req).id
    Request_result.write_data_to_db(data, request_id)


if __name__ == '__main__':
    pass
