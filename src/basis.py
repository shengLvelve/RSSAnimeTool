import datetime
import re
import configparser
def log(message):
    '''
    log 的 Docstring
    打印日志信息
    :param message: 要打印的信息
    '''
    print(f"[{datetime.datetime.now()}] {message}")

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