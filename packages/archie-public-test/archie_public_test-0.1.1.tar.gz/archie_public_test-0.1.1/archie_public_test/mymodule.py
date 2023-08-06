import requests

def talk_to_me():
  res = requests.get('http://bmagnetta.pythonanywhere.com/')
  print('this is what the api said: ',res.json())