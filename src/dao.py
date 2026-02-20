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
    def __init__(self, title, bangumiid, episode, mikanlink, torrentlink, subtitle, time, isrealtime, download):
        self.title = title
        self.bangumiid = bangumiid
        self.episode = episode
        self.mikanlink = mikanlink
        self.torrentlink = torrentlink
        self.subtitle = subtitle
        self.time = time
        self.isrealtime = isrealtime
        self.download = download
    def isNull(self):
        if self.torrentlink == "":
            return True
        else:
            return False
        
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

    def __init__(self, name, season, year, month, bangumiid, bangumilink, fin, path, time, source):
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

    def isNull(self):

        if self.bangumiid == "":
            return True
        else:
            return False