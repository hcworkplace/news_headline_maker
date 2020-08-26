import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json

headers = {
    # 'authority': 'news.naver.com',
    # 'content-length': '0',
    # 'charset': 'utf-8',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    # 'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    # 'accept': '*/*',
    # 'origin': 'https://news.naver.com',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-dest': 'empty',
    # 'referer': 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=102',
    # 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'JSESSIONID=10D29A6BAAD46BCE3E6F24C39A3990AE; NNB=I4CUENPXYEBV6; ASID=dc5f2a1100000173325716940000005b; MM_NEW=1; NFS=2; MM_NOW_COACH=1; _fbp=fb.1.1594904483661.1927880903; _ga_4BKHBFKFK0=GS1.1.1594904483.1.1.1594904514.29; _ga=GA1.1.409323617.1594904484; NRTK=ag#30s_gr#2_ma#-2_si#-2_en#-2_sp#-2; top_paperheadline=028; nx_ssl=2; sNeoAuthCheck=true; BMR=s=1598409139640&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dpotter777777%26logNo%3D220606035529%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=U0hsjdp0YiRssmupZslssssssfZ-262080; nid_inf=-1518529374; NID_AUT=qxiKWNO5QClPKPgxoT+HGq+JqiDVWY/mdylkQG4QjQLcJwXDkiQBhxXNO34jRrBh; NID_JKL=TA9u7M28ABec9g5Bq5zNuegwc8kWmt/M47uvQPFYnPc=; NID_SES=AAABfe0EOQIFJ5gsvn85/+5p+G/KG+Kl0YYSRN/GxT0GPBMbN6U5VW/FVs2OXjiTARveCWoDkXXuuF59bVcOjoWxR79mYdjO6lqFKhyXHfxfFAdPvKA2tlfNOxEJTC4KNSu7BZMnZzfVgV49/N7xSHCIlmmVKIPuRaZ6fVBFPZY9thZcy+iCp/sBFbOz07hVamOft8XCbIwAjvkn5ot5ehJU2j+X8viryhF1x3gL57/6JXBxfkvo/9baEKOgUtSdDQxXUvHW5XSPlXCbt7oSfiT4vcpHwufUsmqVyKsSwDheXZ/i/0jTttSCr96f9Gyb+gJ2uK90pOhQmRl4vv7onvcpx3cuKZyRkmoadOduQ1H4rzYP7YIaUA3KQqEMdxO6GR115fypwgjM6tK4oQj/D/ZCAC6AOoCn0cj3Rev5Lwn81hf6uyKdzd8t1VfT2e+cNdf52FPqFLFH0DUut6Z1ZucDXHX4ET85didApRa7tiq/Y3M0SGwqgKLdxw4N8FSDBGSogQ==; sLastIdpType=naver',
}


def getIds(max_pages):
    print('# start getIds')

    ids = []
    
    for i in range(1, max_pages+1):
        params = (
            ('sid1', '102'),
            ('date', ' 00:00:00'),
            ('page', str(i)),
        )

        response = requests.post('https://news.naver.com/main/mainNews.nhn', headers=headers, params=params)
        news_data_json = response.json()
        news_data = json.loads(news_data_json['airsResult'])['result']['102']
    
        for news in news_data:
            aid = news['articleId']
            oid = news['officeId']
            ids.append((aid, oid))

        
        if i % 100 == 0:
            print(f'---> {i}/{max_pages} done')


    print('# getIds done')
    return ids
    

def getArticle(ids):
    print('# start getArticle')
    print('# # of articles:', len(ids))
    
    result = {'title': [], 'content': []}

    i = 0
    for aid, oid in ids:
        url = f"https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid={oid}&aid={aid}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.select_one('#articleTitle').get_text()
        result['title'].append(title)

        content = soup.select_one('#articleBodyContents').get_text()
        content = content.replace('\n', '').replace('\t', '').replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", '')
        content = content.split('▶')[0]
        result['content'].append(content)
        i += 1
        if i % 500 == 0:
            print(f'---> {i}/{len(ids)} articles done')
    
    print('# getArticle done')
    return result


#--------------------------------------------------------------------------------------------

max_pages = 500

ids = getIds(max_pages)
results = getArticle(ids)


with open('../data/web_scraping_500pages_in_society.csv', 'w', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, lineterminator = '\n' )
    writer.writerow(results.keys())
    writer.writerows(zip(*results.values()))
