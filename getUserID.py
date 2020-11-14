import requests
from bs4 import BeautifulSoup
import re
import ipapi

user = input('Input the ptt ID you want to find: ')
url = 'https://www.pttweb.cc/user/' + user + '?t=article'
list_req = requests.get(url)
soup = BeautifulSoup(list_req.content, "html.parser")
aritcles = soup.select('div.thread-item a')
ips = []
for aritcle in aritcles:
	if aritcle.get('href').count('/') >= 3:
		a_url = 'https://www.pttweb.cc' + aritcle.get('href')
		a_req = requests.get(a_url)
		a_soup = BeautifulSoup(a_req.content, "html.parser")
		if a_soup.select_one('span.f3'):
			ips.append(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', a_soup.select_one('span.f3').string)[0])
country_of_ip = {}
for ip in ips:
	country = ipapi.location(ip=ip, output='country')
	if country in country_of_ip: country_of_ip[country] += 1
	else: country_of_ip[country] = 1
print('IP:\n', ips)
print('Country of IP:')
for k, v in country_of_ip.items():
	print(str(k)+':'+str(v))
