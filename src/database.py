import sqlite3
import dao
import basis
import version as version


version = version.db_version
db = 'RSSAnime.db'
def initDB():

    """
    初始化数据库表结构，创建ANIME和EPISODE两个表（如果不存在）
    
    ANIME表结构:
        NAME: 动画名称
        SEASON: 季度
        YEAR: 年份
        MONTH: 月份
        BANGUMIID: 番剧ID
        BANGUMILINK: 番剧链接
        FIN: 完成状态
        PATH: 文件路径
        TIME: 时间戳
        SOURCE: 数据来源
        RSSLINK: 动画订阅字幕组的RSS链接（v0.2.0 引入）
    
    EPISODE表结构:
        ID: 自增主键
        TITLE: 标题
        BANGUMIID: 关联的番剧ID
        EPISODE: 集数
        MIKANLINK: Mikan链接
        TORRENTLINK: 种子链接
        SUBTITLE: 字幕组
        TIME: 时间戳
        ISREALTIME: 是否实时更新
        DOWNLOAD: 下载状态(0-未下载)

    CONFIG表结构:
        KEY: 配置项键
        VALUE: 配置项值
        
        
    """
    conn = sqlite3.connect(db)
    conn.execute('''
             CREATE TABLE IF NOT EXISTS ANIME (
             NAME TEXT,
             SEASON TEXT,
             YEAR TEXT,
             MONTH TEXT,
             BANGUMIID TEXT,
             BANGUMILINK TEXT,
             FIN INTEGER,
             PATH TEXT,
             TIME DATETIME,
             SOURCE TEXT,
             RSSLINK TEXT
             );
             ''')
    conn.execute('''
             CREATE TABLE IF NOT EXISTS EPISODE (
             ID INTEGER PRIMARY KEY AUTOINCREMENT,
             TITLE TEXT,
             BANGUMIID TEXT,
             EPISODE TEXT,
             MIKANLINK TEXT,
             TORRENTLINK TEXT,
             SUBTITLE TEXT,
             TIME DATETIME,
             ISREALTIME INTEGER,
             DOWNLOAD INTEGER DEFAULT 0
             );
             ''')
    conn.execute('''
             CREATE TABLE IF NOT EXISTS CONFIG (
             KEY TEXT,
             VALUE TEXT
             );
             ''')
    
    if conn.execute('SELECT * FROM CONFIG WHERE KEY = ?;', ('version',)).fetchone() is None:
        conn.execute('''INSERT INTO CONFIG (KEY, VALUE) VALUES (?, ?)''', ('version', version,))

    conn.commit()
    conn.close()

def upd_download_status(status,torrentLink):
    '''
    upd_download_status 的 Docstring
    更新torrent下载状态

    :param status: 更新后的状态

    :param torrentLink: 要更新状态的torrent链接

    :return: None
    '''
    conn = sqlite3.connect(db)
    conn.execute('UPDATE EPISODE SET DOWNLOAD = ? WHERE TORRENTLINK = ?;', (status,torrentLink,))
    conn.commit()
    conn.close()

def get_last_episode():
    
    """
    从数据库中获取最新的实时剧集信息
    
    Args:
        无参数
    
    Returns:
        dao.episode: 包含最新剧集信息的对象。如果数据库中没有记录，则返回一个空对象
    
    Raises:
        无显式抛出异常，但可能传播sqlite3的数据库操作异常
    """
    conn = sqlite3.connect(db)
    sqlast = conn.execute('SELECT * FROM EPISODE WHERE ISREALTIME = 1 ORDER BY ID DESC LIMIT 1;').fetchone()
    conn.close()
    if sqlast is None:
        episode = dao.episode("","",0,"",0,"",0,0,0)
    else:
        episode = dao.episode(sqlast[1],sqlast[2],sqlast[3],sqlast[4],sqlast[5],sqlast[6],sqlast[7],sqlast[8],sqlast[9])
    return episode

def add_episode(episode:dao.episode):
    """
    将剧集对象插入到数据库的EPISODE表中
    
    Args:
        episode (dao.episode): 包含剧集信息的对象，需要包含以下属性：
            - title: 剧集标题
            - bangumiid: 所属番剧ID
            - episode: 剧集编号
            - mikanlink: Mikan链接
            - torrentlink: 种子链接
            - subtitle: 字幕信息
            - isrealtime: 是否为实时更新标志
    """

    conn = sqlite3.connect(db)
    conn.execute('''INSERT INTO EPISODE (TITLE, BANGUMIID, EPISODE, MIKANLINK, TORRENTLINK, SUBTITLE, TIME, ISREALTIME, DOWNLOAD)
                        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)''', (episode.title, episode.bangumiid, episode.episode, episode.mikanlink, episode.torrentlink, episode.subtitle, episode.isrealtime, episode.download,))
    
    conn.commit()
    conn.close()

def get_anime(bangumiid:str):
    """
    根据番剧ID从数据库中获取番剧信息
    
    Args:
        bangumiid (str): bangumi中番剧的唯一标识符
    
    Returns:
        dao.anime: 包含番剧详细信息的对象，如果未找到则返回空对象
    
    Raises:
        sqlite3.Error: 如果数据库操作过程中发生错误
    """

    conn = sqlite3.connect(db)
    animeExist = conn.execute('SELECT * FROM ANIME WHERE BANGUMIID = ?;', (bangumiid,)).fetchone()
    conn.close()
    if animeExist is None:
         anime = dao.anime("","","","","","","","","","","")
    else:
        anime = dao.anime(animeExist[0], animeExist[1], animeExist[2], animeExist[3], animeExist[4], animeExist[5], animeExist[6], animeExist[7], animeExist[8], animeExist[9], animeExist[10])
    return anime

def add_anime(anime:dao.anime):
    """
    将动漫信息插入到数据库表中
    
    Args:
        anime (dao.anime): 包含动漫信息的对象，需包含以下属性：
            - name: 动漫名称
            - season: 季数
            - year: 年份 
            - month: 月份
            - bangumiid: Bangumi ID
            - bangumilink: Bangumi链接
            - path: 存储路径
            - source: 数据来源
    
    Raises:
        sqlite3.Error: 当数据库操作失败时抛出
    """
    conn = sqlite3.connect(db)
    
    if anime.time == "datetime('now')":
        conn.execute('''INSERT INTO ANIME (NAME, SEASON, YEAR, MONTH, BANGUMIID, BANGUMILINK, PATH, TIME , SOURCE , RSSLINK)
                        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)''', 
                        (anime.name, anime.season, anime.year, anime.month, anime.bangumiid, anime.bangumilink, anime.path ,  anime.source, anime.rsslink,))
        basis.log("Inserted new anime: "+anime.name , "INFO")
    else:

        conn.execute('''INSERT INTO ANIME (NAME, SEASON, YEAR, MONTH, BANGUMIID, BANGUMILINK, PATH, TIME , SOURCE , RSSLINK)

                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 

                        (anime.name, anime.season, anime.year, anime.month, anime.bangumiid, anime.bangumilink, anime.path , anime.time, anime.source, anime.rsslink,))
        


    conn.commit()
    conn.close()

def add_config(key:str,value:str):
    """
    将配置项插入到数据库的CONFIG表中
    
    Args:
        key (str): 配置项的键
        value (str): 配置项的值
    
    Raises:
        sqlite3.Error: 当数据库操作失败时抛出
    """
    conn = sqlite3.connect(db)
    if conn.execute('SELECT * FROM CONFIG WHERE KEY = ?;', (key,)).fetchone() is None:
        conn.execute('''INSERT INTO CONFIG (KEY, VALUE) VALUES (?, ?)''', (key, value,))
    else:
        conn.execute('''UPDATE CONFIG SET VALUE = ? WHERE KEY = ?''', (value, key,))
    conn.commit()
    conn.close()

def get_config(key:str):
    """
    从数据库的CONFIG表中获取指定键的配置值
    
    Args:
        key (str): 要查询的配置项键
    
    Returns:
        str: 配置项的值，如果未找到则返回None
    
    Raises:
        sqlite3.Error: 当数据库操作失败时抛出
    """
    conn = sqlite3.connect(db)
    result = conn.execute('SELECT VALUE FROM CONFIG WHERE KEY = ?;', (key,)).fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None

def check_episode_exists(TORRENTLINK:str):
    """
    检查数据库中是否存在指定torrent链接的剧集记录
    
    Args:
        url (str): 要检查的torrent链接
    
    Returns:
        bool: 如果存在对应的剧集记录则返回True，否则返回False
    
    Raises:
        sqlite3.Error: 当数据库操作失败时抛出
    """
    conn = sqlite3.connect(db)
    result = conn.execute('SELECT 1 FROM EPISODE WHERE TORRENTLINK = ?;', (TORRENTLINK,)).fetchone()
    conn.close()
    return result is not None

def get_anime_by_month(year:str, month:str):
    '''
    v0.2.0新增方法
    get_anime_by_month 的 Docstring
    
    根据月份获取数据库中对应季度的番剧列表

    :param month: 月份

    :return: 番剧列表
    '''
    conn = sqlite3.connect(db)
    result = conn.execute('SELECT * FROM ANIME WHERE MONTH = ? AND YEAR = ?;', (month, year)).fetchall()
    conn.close()
    animeList = []
    for anime in result:
        animeList.append(dao.anime(anime[0], anime[1], anime[2], anime[3], anime[4], anime[5], anime[6], anime[7], anime[8], anime[9], anime[10]))
    return animeList

def get_column_names(table_name:str,db:str):
    
    '''
    v0.2.0新增方法
    get_column_names 的 Docstring
    
    获取数据库表的列名列表

    :param table_name: 数据库表名称

    :return: 列名列表
    '''
    conn = sqlite3.connect(db)
    result = conn.execute(f'PRAGMA table_info({table_name});').fetchall()
    conn.close()
    column_names = [column[1] for column in result]
    return column_names

def get_all_anime(db:str):
    '''
    v0.2.0新增方法
    get_all_anime 的 Docstring
    
    获取数据库中所有的番剧信息
    用于更新数据库时获取现有数据

    :return: 番剧对象数组
    '''
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    result = conn.execute('SELECT * FROM ANIME;').fetchall()
    conn.close()
    animeList = []
    for anime in result:
        animeObj = dao.anime()
        animeObj.toObject(anime)
        animeList.append(animeObj)
    return animeList

def get_episode(bangumiid:str,db:str):
    '''
    v0.2.0新增方法
    get_episode 的 Docstring
    
    获取数据库中指定番剧的最新剧集信息
    '''
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    result = conn.execute('SELECT * FROM EPISODE WHERE BANGUMIID = ? ;', (bangumiid,)).fetchall()
    conn.close()
    return result

def get_all_episode(db:str):

    '''

    v0.2.0新增方法
    get_all_episode 的 Docstring

    获取数据库中所有的剧集信息
    用于更新数据库时获取现有数据
    '''

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    result = conn.execute('SELECT * FROM EPISODE;').fetchall()
    conn.close()
    episodeList = []
    for episode in result:
        episodeObj = dao.episode()
        episodeObj.toObject(episode)
        episodeList.append(episodeObj)
    return episodeList

def get_all_config(db:str):
    '''
    v0.2.0新增方法
    get_all_config 的 Docstring
    
    获取数据库中所有的配置信息
    用于更新数据库时获取现有数据
    '''
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    result = conn.execute('SELECT * FROM CONFIG;').fetchall()
    conn.close()
    
    return result