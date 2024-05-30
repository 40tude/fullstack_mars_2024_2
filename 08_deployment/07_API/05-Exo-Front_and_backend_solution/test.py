import requests 
import json
import pandas as pd 

### Test groupby endpoint
def test_categories():
    payload = {
        "column": "BusinessTravel", 
        "by_method": "sum"
    }

    r = requests.post(
        "http://0.0.0.0:4000/groupby", 
        data= json.dumps(payload)
        )

    response = r.json()
    print(pd.read_json(response))

### Test filter-by endpoint
def test_filterBy():

    payload = {
        "column": "BusinessTravel",
        "by_categories": ["Travel_Rarely", "Non-Travel"]
    }

    r = requests.post(
        "http://0.0.0.0:4000/filter-by",
        data = json.dumps(payload)
    )

    response = r.json()
    print(pd.read_json(response))

test_filterBy()