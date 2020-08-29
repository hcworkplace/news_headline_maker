import pandas as pd
import numpy as np
import re
from string import punctuation






def prep_title(title_series):
    print("# start title preprocessing")

    # [속보], (종합) 처럼 괄호처리 된 부분 제거
    title = title_series.str.replace(r'\[[^]]*\]', ' ')
    title = title.str.replace(r'\([^)]*\)', ' ')
    print('-----> preprocessing... 1/2')

    # 문장 부호 제거
    regex = re.compile(r"(?<!\d)[.](?!\d)")
    title = title.map(lambda x: re.sub(regex, ' ', x))
    
    title = title.str.replace(r'[^\w|^.]', ' ')
    title = title.str.replace('ㆍ', ' ')
    print('-----> preprocessing... 2/2')
    print("# title preprocessing done", '\n')
    
    return title


def prep_content(content_series):
    print("# start content preprocessing ")

    # 괄호 제거
    content = content_series.str.replace(r'\[[^]]*\]', ' ')
    content = content.str.replace(r'\([^)]*\)', ' ')
    content = content.str.replace(r'\<[^>]*\>', ' ')
    content = content.str.replace(r'◀[^▶]*▶', ' ')
    print('-----> preprocessing... 1/8')

    # 메일 부분 제거 
    content = content.str.replace(r'\S+@\S+\.\S+', ' ')
    print('-----> preprocessing... 2/8')

    # OOO 기자 / OOO기자 제거
    content = content.str.replace(r'[\w]+\s?기자', ' ')
    print('-----> preprocessing... 3/8')

    # 구두점을 제외한 문장부호 제거
    content = content.str.replace(r'[^\w|^.]', ' ')
    content = content.str.replace('ㆍ', ' ')
    print('-----> preprocessing... 4/8')

    # 한문 제거 -- 오래 걸림
    content = content.str.replace('.*[\u2e80-\u2eff\u31c0-\u31ef\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fbf\uf900-\ufaff].*', ' ')
    print('-----> preprocessing... 5/8')

    # 다. 기준으로 split해서 마지막 2문장 버리기
    content = content.map(lambda x: x.split('다.')[:-2])
    content = content.map(lambda x: [a+'다' for a in x])
    print('-----> preprocessing... 6/8')

    # 기사 첫 문장 전처리
    content_first = content.map(lambda x: x[0] if len(x)!=0 else '').str.replace('(동영상|뉴스|앵커|뉴스데스크|뉴스5시|정치부회의|영상|멘트|제보자들|인터뷰 자료의 저작권은 KBS라디오에 있습니다|특집)', ' ')
    for i, stc in enumerate(content_first):
        if stc != '':
            content[i][0] = stc

    # 문장 순서 뒤집기
    content = content.map(lambda x: x[::-1])
    content = content.map(lambda x: ' '.join(x))
    print('-----> preprocessing... 7/8')

    # 구두점 제거
    regex = re.compile(r"(?<!\d)[.](?!\d)")
    content = content.map(lambda x: re.sub(regex, ' ', x))
    content = content.map(lambda x: x.strip())
    print('-----> preprocessing... 8/8')
    print('# content preprocessing done')
    return content





def prep_data(df):
    
    # title 전처리
        # 한자 제목 데이터 제거
    regex_hanja = re.compile('.*[\u2e80-\u2eff\u31c0-\u31ef\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fbf\uf900-\ufaff].*')
    df = df[df['title'].map(lambda x: regex_hanja.search(x)).isna()]
        # 전처리
    df['title'] = prep_title(df['title'])

    # content 전처리
        # 전처리 전 -기사 내용이 너무 짧거나 없는 경우 제거
    df = df[df['content'].map(lambda x : len(x) >= 300) ].reset_index(drop=True)
        # 전처리
    df['content'] = prep_content(df['content'])
        # 전처리 후 -기사 내용이 너무 짧거나 없는 경우 제거
    df['content'] = df['content'][df['content'].map(lambda x : len(x) >= 120)]
    

    return df



if __name__=='__main__':
    data = pd.read_csv('../data/naver_news_society_10000.csv')
    prep_data = prep_data(data)
    print(prep_data.head(10))
    print(prep_data.shape)