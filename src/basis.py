import datetime
import configparser
import os
import basis
from termcolor import colored
import math
import dao
import logging
import version as version
import anitopy
import service

def initLogger():
    '''
    initLogger 的 Docstring
    初始化日志记录器，设置日志格式和输出级别
    '''
#       日志级别	对应的数值	严重程度
#       DEBUG	    10	        最低
#       INFO	    20	
#       WARNING	    30	
#       ERROR	    40	
#       CRITICAL	50	        最高
    logger = logging.getLogger("RSSAnimeLogger")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # 控制台
    try:
        console_display = get_config_value('conf', 'console_display')
    except Exception :
        console_display = True
    if console_display == None:
        console_display = True
    if console_display:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
    
    # 文件
    file_handler = logging.FileHandler(datetime.date.today().strftime("%Y%m%d")+'log.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def log(message: str, level: str ,path: str):
    '''
    log 的 Docstring
    打印日志信息
    :param message: 要打印的信息
    '''
    logger = logging.getLogger("RSSAnimeLogger")

    match level:
        case 'INFO':
            logger.info(colored(f"[{datetime.datetime.now()}] [INFO] ({path}) {message}", "green"))
        
        case 'WARNING':
            logger.warning(colored(f"[{datetime.datetime.now()}] [WARNING] ({path}) {message}", "yellow"))
            
        case 'ERROR':
            logger.error(colored(f"[{datetime.datetime.now()}] [ERROR] ({path}) {message}", "red"))
            service.send_msg(f"[{datetime.datetime.now()}] [ERROR] ({path}) {message}", "ERROR")

    # print(f"[{datetime.datetime.now()}] {message}")

def getEpisode(title):
    '''
    getEpisode 的 Docstring
    从标题中提取集数信息。现已支持ANi、LoliHouse、绿茶字幕组、桜都字幕组
    :param title: 要获取集数的标题

    :return: 集数

    :rtype: str

    :raise ValueError: 如果标题中不包含集数信息，则抛出 ValueError

    :future: 支持更多字幕组,字幕组(subTitle)改为使用mikan提供的数据，方法中拿出数据库信息
    '''
    episode = 0
    '''
    V0.2.1弃用，转为使用anitopy
    '''
    # subTitle = re.findall("^\[([^\[\]]+)\]", title)[0]
    # try:
    #  match subTitle:
    #     case 'ANi'|'LoliHouse'|'澄空学园&动漫国字幕组&LoliHouse'|'喵萌奶茶屋&LoliHouse':
    #         '''
    #         [ANi] 青梅竹马的恋爱喜剧无法成立 - 02 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]
    #         [LoliHouse] 29岁单身中坚冒险家的日常 / 29-sai Dokushin Chuuken Boukensha no Nichijou - 01 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕]
    #         '''
    #         episode = re.findall("-\s*(\d+(?:\.\d+)?)\s*\[", title)[0]
    #     case '绿茶字幕组'|'桜都字幕组':
    #         '''
    #         [桜都字幕组] 有栖川炼其实是个女生吧。 / Arisugawa Ren tte Honto wa Onna Nanda yo ne. [01][1080p][繁体内嵌]
    #         [绿茶字幕组] 能帮我弄干净吗？/Kirei ni Shite Moraemasu ka [01][WebRip][1080p][简繁日内封]
    #         '''
    #         episode = re.findall("\[([\w.-]+)\](?=.*?\[)", title)[1:-1][0]
    # except Exception as e:
    #     episode = "other"
    #     basis.log(f"Error occurred while extracting episode number from title: {title}", "warning")
    info = anitopy.parse(title)
    try:
        if not isinstance(info.get('episode_number'),list):
            episode = info.get('episode_number')
        else:
            episode = "other"
    except Exception as e:

        episode = "other"

        basis.log(f"无法通过文件名获取集数信息: {title}", "warning", "basis.getEpisode()")
   
   
    return episode

def getInfoFromFileName(episode:dao.episode):
        '''
        v0.2.2新增方法
        从文件名中获取字段信息
        '''

        info = anitopy.parse(episode.title)
        episode.anime_year = info.get('anime_year')
        episode.audio_term = info.get('audio_term')
        episode.anime_title = info.get('anime_title')
        episode.episode_title = info.get('episode_title')
        episode.file_checksum = info.get('file_checksum')
        episode.file_extension = info.get('file_extension')
        episode.release_group = info.get('release_group')
        episode.release_version = info.get('release_version')
        episode.video_resolution = info.get('video_resolution')
        episode.video_term = info.get('video_term')
        


def get_config_value(section, option):
    
    """
    从配置文件中读取指定节(section)和选项(option)的值
    
    Args:
        section (str): 配置文件中的节名称
        option (str): 要获取的选项名称
    
    Returns:
        str: 配置项的值
    
    Raises:
        configparser.NoSectionError: 当指定的节不存在时抛出
        configparser.NoOptionError: 当指定的选项不存在时抛出
    """
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini', encoding='utf-8')
    try:
        value = config.get(section, option)
    except Exception as e:
        return None
    return value

def createConfig():
    config = configparser.ConfigParser(interpolation=None)
        
    config['conf'] = {
            # ⬇v0.2.0新增
            'RSS_scan_mode_help': '⬇RSS_scan_mode RSS扫描模式，扫描一次RSS链接完成下载(once)和长时间循环进行(always)',
            'RSS_scan_mode': 'always',
            'get_more_episode_help': '⬇get_more_episode 补全提供下载的所有剧集',
            'get_more_episode': True,
            'sleep_time_help': '⬇sleep_time 检查间隔时间，单位秒',
            'sleep_time': 3600,
            'net_error_sleep' : 600,
            # ⬇v0.2.0新增
            'dev_mode' : False,
            # ⬇v0.2.0新增
            'console_display' : False,
            # ⬇v0.2.0新增
            'version_help' : version.config_version,
            # ⬇v0.2.2新增
            'jellyfin_host_help' : '⬇jellyfin_host jellyfin 地址，用于企业微信推送中的jellyfin链接',
            'jellyfin_host' : 'jellyfin.com'
            }
    config['RSS'] = {
            'url_help': 'RSS 订阅地址',
            'url': 'https://mikanani.me/RSS'
            }
    config['download'] = {
            'download_path_help': '⬇下载路径',
            'download_path': '/your/download/path',
            'download_tool_help': '⬇下载工具，当前支持qbittorrent、transmission',
            'download_tool': 'qbittorrent',
            'download_retry_time': 5,
            }
    config['qbittorrent'] = {
            'host_help': '⬇qbittorrent 地址',
            'host': 'qbittorrent.com:9090',
            'username_help': '⬇qbittorrent 用户名',
            'username': 'admin',
            'password_help': '⬇qbittorrent 密码',
            'password': 'password',
            'download_tag': 'RSSAnimeTool',
            }
    # ⬇v0.2.2新增
    config['transmission'] = {
            'host_help': '⬇transmission 地址。eg:127.0.0.1',
            'host': 'transmission.com',
            'port_help': '⬇transmission 端口。eg:9091',
            'port': '9091',
            'username_help': '⬇transmission 用户名',
            'username': 'admin',
            'password_help': '⬇transmission 密码',
            'password': 'password',
            'label_help': '⬇transmission 标签组',
            'label': 'RSSAnimeTool',
    }
    # ⬇v0.2.2新增
    config['WeChat'] = {
            'Wechat_help': '⬇企业微信通知配置',
            'Wechat_enable': False,
            'corp_id_help': '⬇企业ID,每个企业都拥有唯一的corpid，获取此信息可在管理后台“我的企业”－“企业信息”下查看“企业ID”（需要有管理员权限）',
            'corpid': 'corpID',
            'corpsecret_help': '⬇secret是企业应用里面用于保障数据安全的“钥匙”，每一个应用都有一个独立的访问密钥，为了保证数据的安全，secret务必不能泄漏。secret查看方法：在管理后台->“应用管理”->“应用”->“自建”，点进某个应用，即可看到。',
            'corpsecret': 'SECRET',
            'touser_help': '⬇成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送',
            'touser': 'admin',
            'toparty_help': '⬇部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数',
            'toparty': 'admin',
            'totag_help': '⬇标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数',
            'totag': 'admin',
            'agentid_help': '⬇企业应用的id，整型。企业内部开发，可在应用的设置页面查看；第三方服务商，可通过接口 获取企业授权信息 获取该参数值',
            'agentid': 'admin',
            }

    with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

def initConfig():
    '''
    initConfig 的 Docstring
    初始化配置文件，如果不存在则创建一个默认的配置文件
    '''
    if not os.path.exists('config.ini'):
        basis.log("未发现配置文件，创建默认配置文件", "WARNING", "basis.initConfig()")   
        createConfig()
        return False
    else:
        basis.log("发现配置文件，读取配置文件...", "INFO", "basis.initConfig()")
        return True
    
def get_season():
    '''
    v0.2.0新增方法
    get_season 的 Docstring
    根据当前月份获取季度信息
    :param month: 月份

    :return: 季度

    :rtype: str
    '''
    date= datetime.date.today().strftime("%Y年%m月%d日")
    year = date.split('年')[0]
    month = int(date.split('年')[1].split('月')[0])
    if month == 12:
            year = int(year) + 1
            month = 1
    month = math.floor(month/3)*3+1
    # last_month = month - 3
    if month == 1:
        last_month = 10 
        last_year = int(year) - 1
    else:
        last_month = month - 3
        last_year = year
    return [dao.anime("", "", year, month, "", "", 0, 0, 0, "", ""), dao.anime("", "", last_year, last_month, "", "", 0, 0, 0, "", "")]

