#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

domainUrl = 'https://www.fatsecret.kr'
searchUrl = domainUrl + '/%EC%B9%BC%EB%A1%9C%EB%A6%AC-%EC%98%81%EC%96%91%EC%86%8C/search'
params = {
    'q' : '',
    'pg' : ''
        }

def getListOfDish(q, pg=0):
    listOfDish = []
    params['q'] = q
    params['pg'] = pg
    pContent =  requests.get(searchUrl, params=params).content
    html = BeautifulSoup(pContent, 'html.parser')
    summary = html.select_one('div.searchResultSummary')
    if summary == None:
        return None
    ss = ''.join(x for x in summary.text if x not in '\r\t\n').split(' ')
    numberOfItems = int(ss[0][:-1])
    viewItems = int(ss[2])
    if numberOfItems < 10:
        numberOfItems = 1
        viewItems = 1
    elif numberOfItems / viewItems != 0:
        numberOfItems += 10
    pages = int(numberOfItems / viewItems)
    for e in html.select('table.generic.searchResult td'):
        url = domainUrl + e.select_one('a')['href']
        nameOfDish = e.select_one('a').text
        listOfDish.append({'nameOfDish' : nameOfDish, 'url' : url})
    r = {'pages' : pages, 'listOfDish' : listOfDish}
    return r
