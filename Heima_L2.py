#create by Murphy 2021/02/08
#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd


print('----------------------------------------------split--------------------L2-First part--------------------------------------')
# 请求URL

#得到页面的内容
def get_page_content(request_url):
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    soup=BeautifulSoup(content,'html.parser')
    return soup
#分析页面信息
def analyse(soup):
    df=pd.DataFrame(columns=['投诉编号','投诉品牌','投诉车系','投诉车型','问题简述','典型问题','投诉时间','投诉状态'])
    #找到完整的投诉信息框
    temp=soup.find('div',class_='tslb_b')
    tr_list=temp.find_all('tr')
    for tr in tr_list:
        td_list=tr.find_all('td')
        #如果没有td，就是表头
        if len(td_list)>0:
            id,brand,car_model,type,desc,problem,datatime,status=td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text, \
                                                                 td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text
            #print(id,brand,car_model,type,desc,problem,datatime,status)
            temp={}
            temp['投诉编号']=id
            temp['投诉品牌'] = brand
            temp['投诉车系'] = car_model
            temp['投诉车型'] = type
            temp['问题简述'] = desc
            temp['典型问题'] = problem
            temp['投诉时间'] = datatime
            temp['投诉状态'] = status
            df=df.append(temp,ignore_index=True)
    return df

base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
result=pd.DataFrame(columns=['投诉编号','投诉品牌','投诉车系','投诉车型','问题简述','典型问题','投诉时间','投诉状态'])

soup=get_page_content(base_url)
df=analyse(soup)
result=result.append(df)
print(result)
result.to_excel('d:/car_complain.xlsx',index=False)
print('----------------------------------------------split--------------------L2-Second part--------------------------------------')