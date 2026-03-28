import crawler
import rss
import database
import downloader
import basis
import dao

def get_more_episodes(ep:dao.episode,path ,client):
    '''
    get_more_episodes的 Docstring
    
    根据mikan的番剧链接，获取番剧当前字幕组的rss订阅链接，获取该番剧字幕组其他剧集信息，并下载。

    获取番剧当前字幕组的rss订阅链接。数据源：mikan

    :param mikanLink: mikan的番剧链接

    :param path: 下载路径

    '''
    basis.log("Getting more episodes for: "+ep.title, "INFO")
    rssLink=crawler.get_more_episode_rss(ep.mikanlink)
    moreEP=dao.episode("","",0,"",0,"",0,0,0)
    moreEpList = rss.get_rss_toList(rssLink,moreEP)
    for item in moreEpList:
        if item.torrentlink != ep.mikanlink:
            basis.log("Found additional episode: "+item.title , "INFO")
            item = crawler.upd_episode_info(item,0)
            database.add_episode(item)
            downloader.download(item, path, client)
    return None