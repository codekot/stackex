import json
from datetime import datetime
from stackex.models import User_request, Request_result
#from stackex import db

#TASK: POPULATE DB

def construct_list():
    data_file = 'search.json'
    data = None

    with open(data_file, "r") as json_file:
        data = json.load(json_file)

    items = data['items']
    result = [[item['title'],
               datetime.utcfromtimestamp(item["last_activity_date"]),
               item["link"]] for item in items]
    return result


def populate(db):
    u = User_request(id=1, date=datetime.utcnow(), req_name="java")
    db.session.add(u)
    data = construct_list()
    for datum in data:
        rr = Request_result(title=datum[0],
                            last_activity_date=datum[1],
                            link=datum[2],
                            request_id=1)
        db.session.add(rr)
    db.session.commit()
    print("Database is populated")


if __name__ == '__main__':
    pass
