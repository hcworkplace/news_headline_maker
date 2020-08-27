import requests
from bs4 import BeautifulSoup
import csv

soup_objects = []

for d in range(20200817,20200827):
    for p in range(1, 41):
        list_url = f'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=249&mid=shm&sid1=102&date={d}&page={p}'

        response = requests.get(list_url)
        # # print(response.text)

        soup_objects.append(BeautifulSoup(response.text, 'html.parser'))

        # if BeautifulSoup(response.text, 'html.parser') not in soup_objects:
        #     soup_objects.append(BeautifulSoup(response.text, 'html.parser'))

# print(soup_objects)
# print(len(soup_objects))

news_data = []

for soup in soup_objects:
    page_news = soup.select('#main_content .list_body.newsflash_body a')
    # print(each_news)

    news_data_schema = {'news_title':'', 'news_content':''}

    for news in page_news:
        if news.string == None:
            continue
        # print('title : ' + str.strip(news.string))
        news_data_schema['news_title'] = str.strip(news.string)
        # print(news.attrs)
        # print('link : ' + news.attrs['href'] + '\n')
        
        each_news = requests.get(news.attrs['href'])
        soup_content = BeautifulSoup(each_news.text, 'html.parser')
        content = soup_content.select_one('#articleBodyContents')
        # print('content : ' + content.text)
        try:
            text = content.text.replace('\n', '').replace('\t', '').replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}', '')
            text = text.split('▶')[0]
            news_data_schema['news_content'] = text
        except AttributeError:
            news_data_schema['news_content'] = ''
        # print(news_data_schema, '\n')

        with open('../Data/naver_news_accident.csv', 'a', encoding='utf-8') as csvfile:
            fieldnames = ['news_title', 'news_content']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writerow(news_data_schema)

            print(news_data_schema, '\n')