import crawler
import rss
import database
import downloader
import basis
import dao

def get_more_episodes(mikanLink,path):
    '''
    get_more_episodes的 Docstring
    
    根据mikan的番剧链接，获取番剧当前字幕组的rss订阅链接，获取该番剧字幕组其他剧集信息，并下载。

    获取番剧当前字幕组的rss订阅链接。数据源：mikan

    :param mikanLink: mikan的番剧链接

    :param path: 下载路径

    '''
    rssLink=crawler.get_more_episode_rss(mikanLink)
    moreEP=dao.episode("","",0,"",0,"",0,0,0)
    moreEpList = rss.get_rss_toList(rssLink,moreEP)
    for item in moreEpList:
        if item.torrentlink != mikanLink:
            basis.log("Found additional episode: "+item.title)
            item = crawler.upd_episode_info(item,0)
            database.add_episode(item)
            downloader.download(item.torrentlink, path)
    return None