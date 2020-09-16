from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from bs4 import BeautifulSoup as soup
import requests
import html
from urllib.parse import unquote
import string
from random import randint,choice
# Create your views here.

import json 
def walld(strin: str):
    if len(strin.split()) > 1:
        strin = '+'.join(strin.split())
    url = 'https://wall.alphacoders.com/search.php?search='
    none_got = ['https://wall.alphacoders.com/finding_wallpapers.php']
    none_got.append("https://wall.alphacoders.com/search-no-results.php")
    page_link = 'https://wall.alphacoders.com/search.php?search={}&page={}'
    resp = requests.get(f'{url}{strin}')
    if resp.url in none_got:
        return False
    if 'by_category.php' in resp.url:
        page_link = str(resp.url).replace('&amp;', '') + '&page={}'
        check_link = True
    else:
        check_link = False
    resp = soup(resp.content, 'html.parser')
    try:
        page_num = resp.find('div', {'class': 'visible-xs'})
        page_num = page_num.find('input', {'class': 'form-control'})
        page_num = int(page_num['placeholder'].split(' ')[-1])
    except Exception:
        page_num = 1
    n = randint(1, page_num)
    if page_num != 1:
        if check_link:
            resp = requests.get(page_link.format(n))
        else:
            resp = requests.get(page_link.format(strin, n))
        resp = soup(resp.content, 'html.parser')
    a_s = resp.find_all('a')
    list_a_s = []
    tit_links = []
    r = ['thumb', '350', 'img', 'big.php?i', 'src', 'title']
    for a_tag in a_s:
        if all(d in str(a_tag) for d in r):
            list_a_s.append(a_tag)
    try:
        for df in list_a_s:
            imgi = df.find('img')
            li = str(imgi['src']).replace('thumb-350-', '')
            titl = str(df['title']).replace('|', '')
            titl = titl.replace('  ', '')
            titl = titl.replace('Image', '')
            titl = titl.replace('HD', '')
            titl = titl.replace('Wallpaper', '')
            titl = titl.replace('Background', '')
            if li is not None and titl is not None:
                titl =  titl.strip()
                p = {"Link": li, "title":titl}
                tit_links.append(p)
    except Exception:
        pass
    del list_a_s
    if len(tit_links) == 0:
        return False
    return tit_links
def check_syntax(word):
    lisu = []
    for d in word:
        if d in string.punctuation:
            return False
        if d in string.ascii_lowercase + string.ascii_uppercase + ' ':
             lisu.append(True)
        else:
             lisu.append(False)
    if not False in lisu:
        return True
    else:
        return False
def wall_find(request,strin):
    if request.method == 'GET':
        if strin == None or bool(strin) == False:
            return HttpResponseRedirect("/")
        strin = unquote(strin).strip()
        if check_syntax(strin):
            inf = walld(strin)
            if inf:
                respd = {'query':strin,'Links':inf}
                return HttpResponse(json.dumps(respd,indent=4,sort_keys=True))
            else:
                respd = {'query':inf}
                return HttpResponse(json.dumps(respd,indent=4))
        else:
             return HttpResponse('{"query": "Invalid!"}<br>If you are using symbols then remove them!')
      
def red_to_index(request):
    return HttpResponseRedirect("/")
