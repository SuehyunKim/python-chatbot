import requests
from bs4 import BeautifulSoup

keyword = '캔들'
url = f"https://taling.me/Home/Search/?query={keyword}"

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
print('응답 : ', response)

soup = BeautifulSoup(response.text, 'html.parser')
data = soup.select(
    "div.cont2 > div.cont2_class")

print(f'{keyword} 클래스 리스트')
for item in data:
    title = item.select_one('div.title').text.strip()
    link = item.select_one('a').get('href')
    price = item.select_one('div.price2').text.strip()
    location = item.select_one('div.location').text.strip()
    like = item.select_one('div.d_day').text
    rating = item.select_one('div.star').text.strip()
    print('---------------------------------------------------------')
    print('클래스명: ', title)
    print('url: ', link)
    print('가격: ', price)
    print('위치: ', location)
    print('찜:', like)
    print('평점:', rating)
