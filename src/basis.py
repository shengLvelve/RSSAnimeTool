import datetime
import re
import configparser
import os
import basis
from termcolor import colored
import math
import dao
import logging
import RSSAnimeTool.src.version as version

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
    if console_display:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
    
    # 文件
    file_handler = logging.FileHandler(datetime.date.today().strftime("%Y%m%d")+'log.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def log(message: str, level: str ):
    '''
    log 的 Docstring
    打印日志信息
    :param message: 要打印的信息
    '''
    logger = logging.getLogger("RSSAnimeLogger")

    match level:
        case 'INFO':
            logger.info(colored(f"[{datetime.datetime.now()}] [INFO] {message}", "green"))
        
        case 'WARNING':
            logger.warning(colored(f"[{datetime.datetime.now()}] [WARNING] {message}", "yellow"))
            
        case 'ERROR':
            logger.error(colored(f"[{datetime.datetime.now()}] [ERROR] {message}", "red"))

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
    subTitle = re.findall("^\[([^\[\]]+)\]", title)[0]
    episode = 0
    try:
     match subTitle:
        case 'ANi'|'LoliHouse'|'澄空学园&动漫国字幕组&LoliHouse'|'喵萌奶茶屋&LoliHouse':
            '''
            [ANi] 青梅竹马的恋爱喜剧无法成立 - 02 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]
            [LoliHouse] 29岁单身中坚冒险家的日常 / 29-sai Dokushin Chuuken Boukensha no Nichijou - 01 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕]
            '''
            episode = re.findall("-\s*(\d+(?:\.\d+)?)\s*\[", title)[0]
        case '绿茶字幕组'|'桜都字幕组':
            '''
            [桜都字幕组] 有栖川炼其实是个女生吧。 / Arisugawa Ren tte Honto wa Onna Nanda yo ne. [01][1080p][繁体内嵌]
            [绿茶字幕组] 能帮我弄干净吗？/Kirei ni Shite Moraemasu ka [01][WebRip][1080p][简繁日内封]
            '''
            episode = re.findall("\[([\w.-]+)\](?=.*?\[)", title)[1:-1][0]
    except Exception as e:
        episode = "other"
        basis.log(f"Error occurred while extracting episode number from title: {title}", "ERROR")
    return episode

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
            'sleep_time': 10,
            'net_error_sleep' : 10,
            # ⬇v0.2.0新增
            'dev_mode' : True,
            # ⬇v0.2.0新增
            'console_display' : True,
            # ⬇v0.2.0新增
            'version_help' : version.config_version
            }
    config['RSS'] = {
            'url_help': 'RSS 订阅地址',
            'url': 'https://mikanani.me/RSS'
            }
    config['download'] = {
            'download_path_help': '⬇下载路径',
            'download_path': '/media/onedrive/RSSAnimeTool',
            'download_tool_help': '⬇下载工具，当前支持qbittorrent',
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

    with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

def initConfig():
    '''
    initConfig 的 Docstring
    初始化配置文件，如果不存在则创建一个默认的配置文件
    '''
    if not os.path.exists('config.ini'):
        basis.log("Config file not found. Creating default config.ini...", "WARNING")   
        createConfig()
        return False
    else:
        basis.log("Config file found. Loading config.ini...", "INFO")
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

