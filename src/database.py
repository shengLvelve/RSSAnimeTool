import sqlite3
import dao
import basis

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
             SOURCE TEXT
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
    conn.execute('''INSERT INTO EPISODE (TITLE, BANGUMIID, EPISODE, MIKANLINK, TORRENTLINK, SUBTITLE, TIME, ISREALTIME)
                        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)''', (episode.title, episode.bangumiid, episode.episode, episode.mikanlink, episode.torrentlink, episode.subtitle, episode.isrealtime,))
    
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
         anime = dao.anime("","","","","","","","","","")
    else:
        anime = dao.anime(animeExist[0], animeExist[1], animeExist[2], animeExist[3], animeExist[4], animeExist[5], animeExist[6], animeExist[7], animeExist[8], animeExist[9])
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
    conn.execute('''INSERT INTO ANIME (NAME, SEASON, YEAR, MONTH, BANGUMIID, BANGUMILINK, PATH, TIME , SOURCE)
                                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)''', 
                                (anime.name, anime.season, anime.year, anime.month, anime.bangumiid, anime.bangumilink, anime.path, anime.source))
    conn.commit()
    conn.close()
    basis.log("Inserted new anime: "+anime.name , "INFO")

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
