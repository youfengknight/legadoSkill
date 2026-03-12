import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 获取分类页面 - 查找分页
url = 'https://www.0826j.com/xuanhuan/'
response = requests.get(url, headers=headers, timeout=30)
html = response.text

# 查找所有链接
print('=== 所有包含xuanhuan的链接 ===')
links = re.findall(r'href=["\']([^"\'>]*)["\']', html)
for link in links:
    if 'xuanhuan' in link:
        print(link)

# 查找分页区域 - 查看HTML末尾
print('\n=== HTML末尾 ===')
print(html[-3000:])
