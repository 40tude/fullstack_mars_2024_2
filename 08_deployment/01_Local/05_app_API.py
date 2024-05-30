import requests
import pandas as pd

url = "https://house-prices-simple-api.herokuapp.com/data"
	
response = requests.get(url) #, headers=headers, data=payload)
my_list = response.json()

print(response.text)
print(response.json())

for key, value in response.json().items():
  print(key, "        ", value)


# df = pd.DataFrame(response.json())
# print(df.head())


# print(response.json())

# df = pd.DataFrame(columns=[key for key, value in response.json().items()])   
# print(df.head())
