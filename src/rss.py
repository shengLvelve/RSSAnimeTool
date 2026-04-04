import fastfeedparser
import dao
import basis
import time
import database

def get_rss_toList(RSS_url:str,lastEP:dao.episode):
    
    """
    从RSS订阅源获取新增的剧集列表
    
    Args:
        RSS_url (str): RSS订阅源的URL地址
        lastEP (dao.episode): 数据库中记录的最后一条剧集信息
    
    Returns:
        list[dao.episode]: 包含新增剧集的列表，每个元素为dao.episode对象
            当遇到与lastEP相同的剧集时停止收集并返回当前列表
    """
    templist= []
    try:
        RSS = fastfeedparser.parse(RSS_url)
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