import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 获取分类页面 - 检查分页
url = 'https://www.0826j.com/xuanhuan/2.html'
response = requests.get(url, headers=headers, timeout=30)
print('Status:', response.status_code)
print('URL:', response.url)

# 查找分页相关内容
html = response.text

# 查找分页链接
print('=== 查找分页链接 ===')
links = re.findall(r'href=["\']([^"\'>]*)["\']', html)
for link in links:
    if 'xuanhuan' in link and '.html' in link:
        print(link)

# 查找页码区域
print('\n=== 查找页码区域 ===')
page_match = re.search(r'<div[^>]*class[^>]*page[^>]*>(.*?)</div>', html, re.IGNORECASE | re.DOTALL)
if page_match:
    print(page_match.group(1)[:500])

# 查找首页导航的分类链接
print('\n=== 首页导航分类 ===')
nav_response = requests.get('https://www.0826j.com/', headers=headers, timeout=30)
nav_html = nav_response.text
nav_match = re.search(r'<div[^>]*m_menu[^>]*>(.*?)</div>', nav_html, re.IGNORECASE | re.DOTALL)
if nav_match:
    nav_links = re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>([^<]*)</a>', nav_match.group(1))
    for href, text in nav_links:
        if href.startswith('/'):
            print(f'{text}: {href}')
