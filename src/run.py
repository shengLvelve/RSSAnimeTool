import database
import rss
import basis
import crawler
import downloader
import service
import time
import sys
"""
    从RSS源获取最新剧集信息并处理下载任务
    
    处理流程：
    1. 从数据库获取最后处理的剧集记录
    2. 从指定RSS源获取更新的剧集列表
    3. 对每个剧集执行以下操作：
       - 记录处理日志
       - 更新剧集信息到数据库
       - 检查关联动画信息是否存在，不存在则爬取并添加
       - 下载剧集种子文件到指定路径
    
    Args:
        database: 数据库操作对象
        rss: RSS源解析对象
        crawler: 网页爬取对象
        service: 剧集服务对象
        downloader: 下载管理对象
        basis: 日志记录对象
    
    Raises:
        ConnectionError: RSS源连接失败时抛出
        DatabaseError: 数据库操作异常时抛出
        DownloadError: 下载任务失败时抛出
"""
database.initDB()
if not basis.initConfig():
    basis.log("配置文件已生成，请根据提示补全配置信息", "WARNING")
    time.sleep(5)
    sys.exit(1)
downloaderStatus = downloader.downloader_check()
while downloaderStatus != 1:
    downloaderStatus = downloader.downloader_check()
rssurl = basis.get_config_value('RSS', 'url')    

while 1:
    try:
        basis.log("Checking for new episodes...", "INFO")
        sqlast = database.get_last_episode()
    
        client = downloader.downloader_login()
    
        templist= rss.get_rss_toList(rssurl,sqlast)
        if not templist:
            basis.log("No new episodes found. Sleeping...", "INFO")
        else:
            basis.log(f"Found {len(templist)} new episodes. Processing...", "INFO")
        for entry in reversed(templist):
            basis.log("Processing Episode: "+entry.title , "INFO")
        
            episodeInfo = crawler.upd_episode_info(entry, 1)
            animeInfo= database.get_anime(episodeInfo.bangumiid)
            if  animeInfo.isNull():
                basis.log("Anime info not found in database, crawling: "+episodeInfo.bangumiid, "INFO")
                animeInfo = crawler.get_anime_info(episodeInfo)
                database.add_anime(animeInfo)
                if basis.get_config_value("conf","get_more_episode") :
                    service.get_more_episodes(episodeInfo,animeInfo.path,client)
            downloader.download(episodeInfo,animeInfo.path,client)
            database.add_episode(episodeInfo)
            
        downloader.downloader_logout(client)
        database.add_config("last_processed_date", time.time())
        time.sleep(int(basis.get_config_value('conf', 'sleep_time')))
    except Exception as e:
        basis.log("connection error: "+str(e), "ERROR")
        time.sleep(int(basis.get_config_value('conf', 'sleep_time')))
        continue




