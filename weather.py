import requests
import json
import pprint
import time
import sys


apikey = '5713f3fc6426a4fb5486414ada0f4c29'
if len(sys.argv) > 1 :
  apikey = str(sys.argv[1])
  url = "http://api.openweathermap.org/data/2.5/weather?id=4076795&appid=" + apikey
  page = requests.get(url)
  data =json.loads(page.text)
  print(data)
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(data['weather'])
  pp.pprint(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['dt'])))
  pp.pprint(data['weather'][0]['main'])
else:
  print("Usage: weather <apikey>")

