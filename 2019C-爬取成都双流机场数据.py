import requests
import pandas as pd
from bs4 import BeautifulSoup
url = 'https://www.cdairport.com/dynamic3.aspx'
path = r'..\airplane.xlsx' # 将此路径改为你的本地保存路径
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'}
Info = []
start_page = 1
end_page = 42
for i in range(start_page,end_page):
    params = {
    't':'8',
    'inout':'a',
    'date':'-1',
    'etime':'23:59',
    'page':str(i)
    }
    res = requests.get(url,params=params)
    sp = BeautifulSoup(res.text,'html.parser')
    flights = sp.find_all('li',class_='clearfix')
    for flight in flights:
        Zip = flight.find_all('span',class_='dltxt')
        Info.append([Zip[i].text for i in range(len(Zip))])
Info = pd.DataFrame(Info,columns=['航班号','始发地','目的地','经停','航空公司','计划到达','航站楼','状态'])
Info.to_excel(path,index=False)
