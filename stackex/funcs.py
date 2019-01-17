import json

data_file = 'search.json'
data = None

with open(data_file, "r") as json_file:
    data = json.load(json_file)

print(data)