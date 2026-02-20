import database
import rss
import basis
import crawler
import downloader
import service
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
    
sqlast = database.get_last_episode()
rssurl = basis.get_config_value('RSS', 'url')

templist= rss.get_rss_toList(rssurl,sqlast)

for entry in reversed(templist):
    basis.log("Processing Episode: "+entry.title)
    episodeInfo = crawler.upd_episode_info(entry, 1)
    database.add_episode(episodeInfo)
    animeInfo= database.get_anime(episodeInfo.bangumiid)
    if  animeInfo.isNull():
        animeInfo = crawler.get_anime_info(episodeInfo)
        database.add_anime(animeInfo)
        if basis.get_config_value("conf","get_more_episode") :
            service.get_more_episodes(episodeInfo.mikanlink,animeInfo.path)
    downloader.download(episodeInfo.torrentlink,animeInfo.path)



