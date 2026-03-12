import requests
import re
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get('https://m.zym888.com/', headers=headers)
html = response.text

params = {}
var_pattern = r'var\s+(\w+)\s*=\s*"([^"]+)"'
matches = re.findall(var_pattern, html)

for name, value in matches:
    params[name] = value

time.sleep(6)

params['q'] = '斗破'

search_url = 'https://m.zym888.com/api/search'
search_response = requests.post(search_url, data=params, headers=headers)
result = search_response.json()

with open('g:/Project/阅读SKills/legadoSkill-main/temp/search_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Result saved to search_result.json')
print(f'Code: {result.get("code")}')
print(f'Msg: {result.get("msg")}')
