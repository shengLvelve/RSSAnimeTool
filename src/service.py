import crawler
import rss
import database
import downloader
import basis
import dao
import wechat


def get_more_episodes(anime:dao.anime ,client , torrentlink:str):
    # v0.2.0 重写
    '''
    get_more_episodes的 Docstring
    
    根据mikan的番剧链接，获取番剧当前字幕组的rss订阅链接，获取该番剧字幕组其他剧集信息，并下载。

    获取番剧当前字幕组的rss订阅链接。数据源：mikan

    :param mikanLink: mikan的番剧链接

    :param path: 下载路径

    '''
    # basis.log("Getting more episodes for: "+anime.name, "INFO")
    rssLink=anime.rsslink
    moreEpList = rss.get_rss_toList(rssLink)
    for item in moreEpList:
        if item.torrentlink != torrentlink:
            basis.log("发现未下载剧集: "+item.title , "INFO", "service.get_more_episodes()")
            item.isrealtime = 0
            item = crawler.upd_episode_info(item)
            database.add_episode(item)
            downloader.download(item, anime.path, client)
    return None

def get_episodes_by_animeRSS(client):
    '''
    v0.2.0新增方法，已知问题0.1.0-2

    get_episode_by_animeRSS 的 Docstring
    
    根据mikan的番剧链接，获取番剧当前字幕组的rss订阅链接，获取该番剧字幕组其他剧集信息，并下载。

    获取番剧当前字幕组的rss订阅链接。数据源：mikan

    :param mikanLink: mikan的番剧链接

    :param path: 下载路径

    1、获取数据库中本季度番剧列表

    '''
    basis.log("开始遍历近两季度已订阅动画RSS链接", "INFO", "service.get_episodes_by_animeRSS()")
    monthList = basis.get_season()
    animeList = database.get_anime_by_month(monthList[0].year, monthList[0].month)+database.get_anime_by_month(monthList[1].year, monthList[1].month)
    for anime in animeList:
        if anime.rsslink != "":
            # basis.log("Processing anime by animeRSS: "+anime.name, "INFO")
            get_more_episodes(anime, client, "")

    return None

def send_msg(msg:str,msg_type:str="INFO"):
    '''
    v0.2.2新增方法，各平台信息推送
    '''
    if basis.get_config_value("WeChat", "Wechat_enable"):
        wechat.send_message(None , f"[{msg_type}] {msg}")
    
    