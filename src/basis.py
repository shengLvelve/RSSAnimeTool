import datetime
import re
import configparser
import os
import basis
from termcolor import colored

def log(message: str, level: str):
    '''
    log 的 Docstring
    打印日志信息
    :param message: 要打印的信息
    '''

    match level:
        case 'INFO':
            print(colored(f"[{datetime.datetime.now()}] [INFO] {message}", "green"))
        
        case 'WARNING':
            print(colored(f"[{datetime.datetime.now()}] [WARNING] {message}", "yellow"))
            
        case 'ERROR':
            print(colored(f"[{datetime.datetime.now()}] [ERROR] {message}", "red"))

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
    match subTitle:
        case 'ANi'|'LoliHouse':
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
    value = config.get(section, option)
    return value

def initConfig():
    '''
    initConfig 的 Docstring
    初始化配置文件，如果不存在则创建一个默认的配置文件
    '''
    if not os.path.exists('config.ini'):
        basis.log("Config file not found. Creating default config.ini...", "WARNING")   
        config = configparser.ConfigParser(interpolation=None)
        
        config['conf'] = {
            'get_more_episode_help': '⬇get_more_episode 补全提供下载的所有剧集',
            'get_more_episode': True,
            'sleep_time_help': '⬇sleep_time 检查间隔时间，单位秒',
            'sleep_time': 10,
            'net_error_sleep' : 10
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
        return False
    else:
        basis.log("Config file found. Loading config.ini...", "INFO")
        return True