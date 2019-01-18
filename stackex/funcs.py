import json

if __name__ == '__main__':
    data_file = 'search.json'
    data = None

    with open(data_file, "r") as json_file:
        data = json.load(json_file)

    items = data['items']
    for item in items:
        print(item['title'])
        print(item["last_activity_date"])
        print(item["link"])
