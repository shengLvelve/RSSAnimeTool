import fastfeedparser
import dao
import basis
import time
import database
import requests

# def get_rss_toList(RSS_url:str,lastEP:dao.episode):
def get_rss_toList(RSS_url:str):  
    """
    从RSS订阅源获取新增的剧集列表，过滤掉数据库中已存在的剧集记录
    
    Args:
        RSS_url (str): RSS订阅源的URL地址
        lastEP (dao.episode): 数据库中记录的最后一条剧集信息
    
    Returns:
        list[dao.episode]: 包含新增剧集的列表，每个元素为dao.episode对象
            当遇到与lastEP相同的剧集时停止收集并返回当前列表
    """

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

    templist= []
    try:
        response = requests.get(RSS_url, headers=headers, timeout=15)
        response.raise_for_status()
        RSS = fastfeedparser.parse(response.text)
    except Exception as e:
        basis.log("Failed to fetch RSS feed: "+str(e), "ERROR")
        while RSS.entries is None:
            basis.log("Retrying to fetch RSS feed...", "WARNING")
            
            RSS = fastfeedparser.parse(RSS_url)
            basis.log("Failed to fetch RSS feed: "+str(e), "ERROR")
            time.sleep(10)  # 等待10秒后重试

        
    
    for entry in RSS.entries:
        # if lastEP.torrentlink != entry.enclosures[0]['url']:
        if not database.check_episode_exists(entry.enclosures[0]['url']):
            ep = dao.episode(entry.title, "", basis.getEpisode(entry.title), entry.link, entry.enclosures[0]['url'], "", "datetime('now')", 1, 0)
            templist.append(ep)
        """
        else:
            return templist        
        """


    return templist