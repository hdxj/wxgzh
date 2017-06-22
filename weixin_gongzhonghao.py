import requests
import json
import re
import pymongo
import random
from multiprocessing import Pool

with open('weixin_cookie.txt','r',encoding='utf-8') as f:
    cookie = f.read()
    cookie = json.loads(cookie)


header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

response = requests.get('https://mp.weixin.qq.com/',headers=header,cookies=cookie)

token = re.compile('token=(.*)').search(response.url).group(1)


def get(query):#query这个参数是公众号的微信号
    searchbiz_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    search_dict = {'action' : 'search_biz',
                    'token' : token,
                    'lang' : 'zh_CN',
                    'f' : 'json',
                    'ajax' : '1',
                    'random' : random.random(),
                    'query' : query,
                    'begin' : '0',
                    'count' : '5',}

    search_response = requests.get(searchbiz_url,headers=header,cookies=cookie,params=search_dict)

    for i in range(1000):
        try:
            search_dict2 = {'token' : token,
                            'lang' : 'zh_CN',
                            'f' : 'json',
                            'ajax' : '1',
                            'random' : random.random(),
                            'action' : 'list_ex',
                            'begin' : i*5,
                            'count' : '5',
                            'query' : '',
                            'fakeid' : json.loads(search_response.text).get('list')[0].get('fakeid'),
                            'type' : '9'}

            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            appmsg_response = requests.get(appmsg_url,headers=header,cookies=cookie,params=search_dict2)
            appmsg_response = json.loads(appmsg_response.text)
            list1 = appmsg_response.get('app_msg_list')
            client = pymongo.MongoClient('localhost')
            db = client['gongzhonghao']

            for list in list1:
                lesson = {}
                lesson['title'] = list['title']
                lesson['link'] =list['link']
                db[query].insert(lesson)
                print('{0}：存储成功'.format(query))
        except:
            print('爬取结束')

#列表内是公众号的微信号
gongzhonghao_list = ['PPT100','wwwlemonsaycom','szlybdb','szdays','hey-stone']

if __name__ == '__main__':
    pool = Pool()
    pool.map(get,gongzhonghao_list)
