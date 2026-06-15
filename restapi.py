import requests
import json
response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow=true')
for data in response.json()['items']:
    if data['title'].startswith('How to'):  
       print(data['title'])
       print(data['link'])
    else :
       print('No question found starting with "How to"')
    print()