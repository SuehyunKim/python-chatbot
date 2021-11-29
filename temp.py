import requests
from bs4 import BeautifulSoup

url = "https://www.seoul.go.kr/coronaV/coronaStatus.do"

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
print('응답 : ', response)

soup = BeautifulSoup(response.text, 'html.parser')
data = soup.select(
    "div.inner > div.status")

print('서울 코로나 확진자 발생 동향')
for item in data:
    new = item.select_one('div.num10 > p.counter').text
    total = item.select_one('div.num1 > p.counter').text
    time = item.select_one('div.status-seoul > h4 > span').text
    print('신규 확진자: ', new)
    print('확진자: ', total)
    print(time)
