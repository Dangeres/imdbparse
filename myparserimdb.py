import requests
from bs4 import BeautifulSoup
import json

def search(name):
    myrequest = requests.get('http://www.imdb.com/find?q=%s&s=tt&ref_=fn_tt_pop'%name).text
    myresults = BeautifulSoup(myrequest, 'html.parser').find_all('table', class_='findList')[0].find_all('tr')[:10]

    del myrequest

    answer = []

    for one in myresults:
        temp = one.find_all('td',class_='result_text')[0]
        link = temp.find_all('a',href=True)[0]['href']
        id = link[7:link.find('/?ref')]
        answer.append({'name':temp.get_text(),'id':id,'image':one.find_all('img',src=True)[0]['src']})
        #print(temp.get_text())
    return answer

def get_episods(id):
    page = requests.get('http://www.imdb.com/title/%s/episodes/_ajax?season=%s&ref_=ttep_ep_sn_nx'%(id,'1')).text
    allseasons = BeautifulSoup(page, 'html.parser').find_all('select',id='bySeason')[0].find_all('option', value=True)

    maxseasons = int(allseasons[len(allseasons)-1].get_text())
    nowseason = int(allseasons[0].get_text())

    response = {'count ':maxseasons}

    del page,allseasons

    while nowseason <= maxseasons:
        page = requests.get('http://www.imdb.com/title/%s/episodes/_ajax?season=%s&ref_=ttep_ep_sn_nx' % (id, str(nowseason))).text
        allepisods = BeautifulSoup(page, 'html.parser').find_all('div',class_='info')
        episodes = {}
        nowepisoze = 1
        for episode in allepisods:
            nameepisode = episode.find_all('strong')[0].find_all('a')[0].get_text()
            time = episode.find_all('div','airdate')[0].get_text().strip()
            episodes[nowepisoze] = {'name_episode':nameepisode,'time':time}
            nowepisoze+=1
        response[nowseason] = episodes
        nowseason+=1

    return response

import time
start_time = time.time()

result = search('13 причин почему')
print(result)

print("--- %s seconds to check search ---" % (time.time() - start_time))

print(get_episods(result[0]['id']))

print("--- %s seconds to get episodes ---" % (time.time() - start_time))
