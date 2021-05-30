#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

domainUrl = 'https://www.fatsecret.kr'
searchUrl = domainUrl + '/%EC%B9%BC%EB%A1%9C%EB%A6%AC-%EC%98%81%EC%96%91%EC%86%8C/search'
params = {
    'q' : '',
    'pg' : ''
        }

def getNutrientInfoFromDish(e):
    pContent = requests.get(e['url']).content
    html = BeautifulSoup(pContent, 'html.parser')
    r = {
            'nameOfDish' : e['nameOfDish'],
            'nutritionFacts' : ''
        }
    ## for test
    r['nutritionFacts'] = str(html.select('div.nutrition_facts.international div'))
    '''
    for e in html.select('div.nutrition_facts.international div'):
        r += e.text
    '''
    return r


def getListOfDish(q, pg=0):
    listOfDish = []
    params['q'] = q
    params['pg'] = str(pg)
    pContent =  requests.get(searchUrl, params=params).content
    html = BeautifulSoup(pContent, 'html.parser')
    summary = html.select_one('div.searchResultSummary')
    if summary == None:
        return None
    ss = ''.join(x for x in summary.text if x not in '\r\t\n').split(' ')
    numberOfItems = int(ss[0][:-1])
    viewItems = 10
    if numberOfItems < 10:
        numberOfItems = 1
        viewItems = 1
    elif numberOfItems / viewItems != 0:
        numberOfItems += 10
    pages = int(numberOfItems / viewItems)
    cnt = 0
    for e in html.select('table.generic.searchResult td'):
        url = domainUrl + e.select_one('a')['href']
        nameOfDish = e.select_one('a').text
        listOfDish.append({'id' : cnt, 'nameOfDish' : nameOfDish, 'url' : url})
        cnt += 1
    r = {'keyword' : q, 'pages' : pages, 'listOfDish' : listOfDish}
    return r
