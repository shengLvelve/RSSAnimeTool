import database
import rss
import basis
import crawler
import downloader
import service
import time
import sys
import update

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

# 初始化日志记录器
basis.initLogger()

# 初始化配置文件
if not basis.initConfig():
    basis.log("配置文件已生成，请根据提示补全配置信息", "WARNING", "run.main()")
    time.sleep(5)
    sys.exit(1)

# 初始化数据库
database.initDB()

#检查数据库、config.ini与当前版本是否匹配，进行必要的更新
update.update()

while 1:
    downloaderStatus = downloader.downloader_check()
    if downloaderStatus == 1:
        break

service.send_msg("RSSAnimeTool已启动，正在监视新剧集更新...", "INFO")

rssurl = basis.get_config_value('RSS', 'url')    

RSS_scan_mode = basis.get_config_value('conf', 'RSS_scan_mode')
sleep_time = int(basis.get_config_value('conf', 'sleep_time'))

while 1:
    try:
        basis.log("开始检查新剧集更新...", "INFO", "run.main()")
        # sqlast = database.get_last_episode()
    
        templist= rss.get_rss_toList(rssurl)
        
        if not templist:
            basis.log("没有发现更新的剧集...", "INFO", "run.main()")
        else:
            basis.log(f"发现 {len(templist)} 个新的剧集，开始处理...", "INFO", "run.main()")
        client = downloader.downloader_login()
        for entry in reversed(templist):
            basis.log("Processing Episode: "+entry.title , "INFO", "run.main()")
            episodeInfo = crawler.upd_episode_info(entry)
            episodeInfo.isrealtime = 1
            animeInfo= database.get_anime(episodeInfo.bangumiid)
            if  animeInfo.isNull():
                basis.log("数据库中没有找到该动画信息, 即将抓取此动画信息。bangumiID: "+episodeInfo.bangumiid, "INFO", "run.main()")
                animeInfo = crawler.get_anime_info(episodeInfo)
                database.add_anime(animeInfo)
                # v0.2.0，停用此处，改用get_episodes_by_animeRSS
                # if basis.get_config_value("conf","get_more_episode") :
                #     service.get_more_episodes(animeInfo,client,episodeInfo.torrentlink)
            downloader.download(episodeInfo,animeInfo.path,client)
            database.add_episode(episodeInfo)
        if basis.get_config_value("conf","get_more_episode") :
            # v0.2.0新增功能，已知问题0.1.0-2
            service.get_episodes_by_animeRSS(client)    
        downloader.downloader_logout(client)
        database.add_config("last_processed_date", time.time())
        time.sleep(sleep_time)
    except Exception as e:
        basis.log("未知错误: "+str(e), "ERROR", "run.main()")
        time.sleep(sleep_time)
        continue
    if RSS_scan_mode == "once":
        break




