from qbittorrentapi import Client
import basis
import database
import configparser

def download(torrentLink:str, savePath:str):
    '''
    download 的 Docstring
    根据配置文件，选择下载器

    :param torrentLink: 下载的torrent链接

    :param savePath: 保存路径

    :return: 1 成功 0 失败

    :future: 支持多下载器
    '''

    download_tool = basis.get_config_value('download', 'download_tool')
    download_path = basis.get_config_value('download', 'download_path')
    match download_tool:
        case 'qbittorrent':
            qb_host = basis.get_config_value('qbittorrent', 'host')
            qb_username = basis.get_config_value('qbittorrent', 'username')
            qb_password = basis.get_config_value('qbittorrent', 'password')
            qb_tag = basis.get_config_value('qbittorrent', 'download_tag')
            return qbittorrent_download(torrentLink, download_path+savePath, qb_host, qb_username, qb_password, qb_tag)


def qbittorrent_download(torrentLink, savePath, host, username, password, tag):
    '''
    qbittorrent_download 的 Docstring
    连接qbittorrent下载器，新建任务

    :param torrentLink: 下载的torrent链接

    :param savePath: 保存路径

    :return: 1 成功 0 失败

    :future: 
    '''
    try:
        client = Client(host=host, username=username, password=password)
    except Exception as e:
        basis.log("qBittorrent connection error: "+str(e))
        return None
    else:
        basis.log("Connected to qBittorrent: "+host)
    try:
        client.torrents_add(urls=torrentLink, save_path=savePath, tags=tag)
    except Exception as e:
        basis.log("Error adding torrent to qBittorrent: "+str(e))
        return None
    else:
        # 更新数据库下载状态
        database.upd_download_status("1",torrentLink)
        basis.log("Added torrent to qBittorrent: "+torrentLink)
        return 1
    