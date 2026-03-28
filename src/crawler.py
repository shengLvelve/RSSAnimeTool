import requests
from bs4 import BeautifulSoup
import datetime
import math
import basis
import dao

def upd_episode_info(episodeData:dao.episode,isrealtime):
    '''
    upd_episode_info 的 Docstring
    补充episode对象的bangumiID和subTitle。数据源：mikan
    :param episodeData: 要补充的episode对象，包含mikanlink

    :return: 补充后的episode对象

    :future: 若bangumiID获取失败，生成uuid
    '''
    episodeWeb = requests.get(episodeData.mikanlink).text
            #解析网页内容
    epWebSoup = BeautifulSoup(episodeWeb, 'html.parser')
            #获取番剧mikan地址链接
    animeURL="https://mikanani.me"+epWebSoup.find_all('a', class_='w-other-c')[0]['href']
    subTitle = epWebSoup.find_all('a', class_='magnet-link-wrap')[0].text
            #获取番剧的mikan网页内容
    animeWeb = requests.get(animeURL).text
    animeWebSoup = BeautifulSoup(animeWeb, 'html.parser')
            # 获取bangumiID
    bangumiLink = animeWebSoup.find_all('a', class_='w-other-c')[1].text
    bangumiID = bangumiLink.split('/')[-1]
    episodeData.bangumiid = bangumiID
    episodeData.subtitle = subTitle
    episodeData.isrealtime = isrealtime

    return episodeData

def get_anime_info(episodeData:dao.episode):
    '''

    get_anime_info 的 Docstring

    获取番剧的基本信息，数据源：bangumi\mikan

    :param episodeData: 包含bangumiID的episode对象

    :return: 番剧的基本信息
    '''
    cookies = {
    'chii_sec_id': 'rP%2BhRi24bHu%2BR4MqmKIkNCxcEc2G1RogciY4o9PB',
    'chii_cookietime': '2592000',
    'chii_theme': 'dark',
    '_ga': 'GA1.1.1345578203.1766238797',
    '_ga_1109JLGMHN': 'GS2.1.s1766238797$o1$g1$t1766238820$j37$l0$h0',
    '_tea_utm_cache_10000007': 'undefined',
    'chii_sid': 'r3fe3w',
    }
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://mikanani.me/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'chii_sec_id=rP%2BhRi24bHu%2BR4MqmKIkNCxcEc2G1RogciY4o9PB; chii_cookietime=2592000; chii_theme=dark; _ga=GA1.1.1345578203.1766238797; _ga_1109JLGMHN=GS2.1.s1766238797$o1$g1$t1766238820$j37$l0$h0; _tea_utm_cache_10000007=undefined; chii_sid=r3fe3w',
    }
    try:
        bangumiLink = "https://bgm.tv/subject/"+episodeData.bangumiid
        bangumiWeb = requests.get(bangumiLink, cookies=cookies, headers=headers)
        bangumiWeb.encoding = 'utf-8'
        bangumiWebSoup = BeautifulSoup(bangumiWeb.text, 'html.parser')
        name = bangumiWebSoup.find_all('li')[39].text.split(': ')[-1]
        season = ""
        date= bangumiWebSoup.find_all('li')[41].text
        date = date.split(': ')[1]
        year = date.split('年')[0]
        month = int(date.split('年')[1].split('月')[0])
        if month == 12:
            year = int(year) + 1
            month = 1
        month = math.floor(month/3)*3+1
        source = "bangumi"
        basis.log("Successfully got anime info: "+"("+name+")"+" from bangumi", "INFO")
    except Exception as e:
        mikanWeb = requests.get(episodeData.mikanlink)
        mikanWebSoup = BeautifulSoup(mikanWeb.text, 'html.parser')
        name = mikanWebSoup.find_all('p', class_='bangumi-title')[0].text
        season = ""
        date= datetime.date.today().strftime("%Y年%m月%d日")
        year = date.split('年')[0]
        month = int(date.split('年')[1].split('月')[0])
        if month == 12:
            year = int(year) + 1
            month = 1
        month = math.floor(month/3)*3+1
        source = "mikan"
        basis.log("Error getting anime info: "+"("+name+")"+" from bangumi, successfully got anime info from mikan", "WARNING")
    path = "/"+str(year)+"/"+str(month)+"/"+str(name)
    animeInfo = dao.anime(name, season, year, month, episodeData.bangumiid, bangumiLink,0,path,"datetime('now')",source)

    return animeInfo

def get_more_episode_rss(mikanLink:str):
    '''

    get_more_episode_rss 的 Docstring
    
    从mikan获取该番剧字幕组rss链接

    获取番剧当前字幕组的rss订阅链接。数据源：mikan

    :param mikanLink: mikan的番剧链接

    :return: 番剧的rss订阅链接
    '''
    mikanWeb = requests.get(mikanLink).text
    mikanWebSoup = BeautifulSoup(mikanWeb, 'html.parser')
    animeRSSLink = "https://mikanani.me"+mikanWebSoup.find_all('a', class_='mikan-rss')[0]['href']
    return animeRSSLink