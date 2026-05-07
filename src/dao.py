


class episode:
    
    title = ""
    bangumiid = ""
    episode = ""
    mikanlink = ""
    torrentlink = ""
    subtitle = ""
    time = ""
    isrealtime = 0
    download = 0
    anime_year = ""
    audio_term=""
    anime_title=""
    episode_title=""
    file_checksum=""
    file_extension=""
    release_group=""
    release_version=""
    video_resolution=""
    video_term=""

    def __init__(self, title= "", bangumiid= "", episode= "", mikanlink= "", torrentlink= "", subtitle= "", time= "", isrealtime=0, download= 0):
        self.title = title
        self.bangumiid = bangumiid
        self.episode = episode
        self.mikanlink = mikanlink
        self.torrentlink = torrentlink
        self.subtitle = subtitle
        self.time = time
        self.isrealtime = isrealtime
        self.download = download
        self.anime_year = ""
        self.audio_term = ""
        self.anime_title = ""
        self.episode_title = ""
        self.file_checksum = ""
        self.file_extension = ""
        self.release_group = ""
        self.release_version = ""
        self.video_resolution = ""
        self.video_term = ""
    def isNull(self):
        if self.torrentlink == "":
            return True
        else:
            return False
        
    def toObject(self,result):
        '''
        v0.2.0新增方法
        将数据库查询结果转换为episode对象
        '''
        self.title = result['TITLE']
        self.bangumiid = result['BANGUMIID']
        self.episode = result['EPISODE']
        self.mikanlink = result['MIKANLINK']
        self.torrentlink = result['TORRENTLINK']
        self.subtitle = result['SUBTITLE']
        self.time = result['TIME']
        self.isrealtime = result['ISREALTIME']
        self.download = result['DOWNLOAD']

    
        pass
    def complete(self):
        '''
        v0.2.0新增方法
        补全episode对象的字段
        '''
        '''
        v0.2.2新增字段
        anime_year,audio_term,anime_title,episode_title,file_checksum,file_extension,release_group,release_version,video_resolution,video_term
        '''
        import basis
        basis.getInfoFromFileName(self)
        pass
        
class anime:
    name = ""
    season = ""
    year = ""
    month = ""
    bangumiid = ""
    bangumilink = ""
    fin = 0
    path = ""
    time = "datetime('now')"
    source = ""
    rsslink = ""
    whereFrom = ""

    def __init__(self, name='', season='', year='', month='', bangumiid='', bangumilink='', fin=0, path='', time='', source='', rsslink='', whereFrom=''):
        self.name = name
        self.season = season
        self.year = year
        self.month = month
        self.bangumiid = bangumiid
        self.bangumilink = bangumilink
        self.fin = fin
        self.path = path
        self.time = time
        self.source = source
        self.rsslink = rsslink
        self.whereFrom = whereFrom

    def isNull(self):

        if self.bangumiid == "":
            return True
        else:
            return False
        
    def toObject(self,result):
        '''
        v0.2.0新增方法
        将数据库查询结果转换为anime对象
        '''
        self.name = result['NAME']
        self.season = result['SEASON']
        self.year = result['YEAR']
        self.month = result['MONTH']
        self.bangumiid = result['BANGUMIID']
        self.bangumilink = result['BANGUMILINK']
        self.fin = result['FIN']
        self.path = result['PATH']
        self.time = result['TIME']
        self.source = result['SOURCE']
        
        try:
            '''
            v0.2.0新增字段RSSLINK
            '''
            self.rsslink = result['RSSLINK']
            '''
            v0.2.2新增字段RSSLINK
            '''
            self.whereFrom = result['WHEREFROM']
        except:
            self.rsslink = ""
            self.whereFrom = ""
        

    def complete(self):
        import crawler
        import database
        '''
        v0.2.0新增方法
        补全anime对象的字段
        '''
        '''
        v0.2.0
        新增字段rsslink
        '''
        if self.rsslink == "":
            episode = database.get_episode(self.bangumiid,'RSSAnime.db.bak')[0]
            self.rsslink = crawler.get_more_episode_rss(episode['mikanlink'])
        '''
        v0.2.2新增字段whereFrom
        '''
        if self.whereFrom == "":
            self.whereFrom = "RSS"