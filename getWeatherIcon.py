import requests

r = requests.get('http://www.hko.gov.hk/wxinfo/json/one_json.xml')
result = r.json()

iconId = result['FLW']['Icon1']
date = result['FLW']["BulletinDate"]

print iconId,date
