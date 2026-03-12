import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 获取排行榜页面
url = 'https://www.0826j.com/paihang/weekvisit/'
response = requests.get(url, headers=headers, timeout=30)
html = response.text

print('=== 排行榜页面 ===')
print('Status:', response.status_code)

# 查找分页链接
print('\n=== 分页链接 ===')
links = re.findall(r'href=["\']([^"\'>]*)["\']', html)
for link in links:
    if 'paihang' in link or 'page' in link.lower():
        print(link)

# 查找书籍列表
print('\n=== 书籍列表结构 ===')
# 查找表格结构
table_match = re.search(r'<table[^>]*>(.*?)</table>', html, re.IGNORECASE | re.DOTALL)
if table_match:
    print(table_match.group(1)[:1500])
