import requests
from bs4 import BeautifulSoup
import csv

import requests

def crawrling(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

soup_obj = []
for date in range(20200817,20200827):
    for num in range(1,40):
        url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=256&sid1=102&date={}&page={}'.format(str(date), str(num))
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_obj.append(soup)

address_list = []
for soup in soup_obj:
    div_tag = soup.find('div', {'class', 'list_body'})
    
    add = div_tag.find_all("a")
    for i in add:
        address_list.append(i['href'])

my_set = set(address_list) #집합set으로 변환
address_list = list(my_set) #list로 변환 ##중복제거를 위해

# #기간내의 기사들 50 페이지까지 soup 객체 list

my_set = set(address_list) #집합set으로 변환
address_list = list(my_set) #list로 변환 ##중복제거를 위해
# 범위 내의 기사 본문 주소 list

print(len(address_list))
# print(address_list)

for news_address in address_list:
    if news_address[:4] != 'http':
        continue
    soup = crawrling(news_address)

    title = soup.find('div', {'class','article_info'})
    if title == None:
        continue
    news_title = title.find("h3").text

    content = soup.find('div', {'class','_article_body_contents'})
    text = content.text.replace('\n','').replace('\t','').replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", '')
    text = text.split('▶')[0]

    news_data = {
                'title' : news_title,
                'content' : text,
            }
    # title, content 추출

    with open('./naver_news_region.csv', 'a', newline='',encoding='utf-8') as csvfile:
        fieldnames = ['title','content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        writer.writerow(news_data)

    # csv파일로 내보내기~~