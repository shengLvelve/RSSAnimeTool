from qbittorrentapi import Client
import basis
import database
import time
import dao

def downloader_check():
    '''
    downloader_check 的 Docstring
    下载器检查，检查连接

    :return: 1 成功 0 失败
    '''
    download_retry = int(basis.get_config_value('download', 'download_retry_time'))
    download_tool = basis.get_config_value('download', 'download_tool')
    basis.log("Checking downloader: "+download_tool, "INFO")
    try:
        client=downloader_login()
        
    except Exception as e:
        basis.log("qBittorrent connection error: "+str(e), "ERROR")
        time.sleep(download_retry)
        return 0
    else:
        downloader_logout(client)
        basis.log("Connected to qBittorrent", "INFO")
        return 1
            
def downloader_login():
    '''
    downloader_login 的 Docstring
    下载器登录，检查连接

    :return: 1 成功 0 失败
    '''
    download_tool = basis.get_config_value('download', 'download_tool')
    match download_tool:
        case 'qbittorrent':
            qb_host = basis.get_config_value('qbittorrent', 'host')
            qb_username = basis.get_config_value('qbittorrent', 'username')
            qb_password = basis.get_config_value('qbittorrent', 'password')
            client = Client(host=qb_host, username=qb_username, password=qb_password)
            try:
                client.auth_log_in()
            except Exception as e:
                raise ConnectionError("Failed to connect to qBittorrent: "+str(e))
            basis.log("Logged in to "+download_tool, "INFO")
            return client

def downloader_logout(client:Client):
    '''
    downloader_logout 的 Docstring
    下载器登出，检查连接

    :param client: 下载器客户端

    :return: 1 成功 0 失败
    '''
    download_tool = basis.get_config_value('download', 'download_tool')
    match download_tool:
        case 'qbittorrent':
            client.auth_log_out()
    basis.log("Logged out of qBittorrent", "INFO")



def download(ep:dao.episode, savePath:str, client:Client):
    '''
    download 的 Docstring
    根据配置文件，选择下载器

    :param torrentLink: 下载的torrent链接

    :param savePath: 保存路径

    :param client: 下载器客户端

    :return: 1 成功 0 失败

    :future: 支持多下载器
    '''

    download_tool = basis.get_config_value('download', 'download_tool')
    download_path = basis.get_config_value('download', 'download_path')
    match download_tool:
        case 'qbittorrent':
            qb_tag = basis.get_config_value('qbittorrent', 'download_tag')
            qbittorrent_download(ep, download_path+savePath, client, qb_tag)
            # basis.log("Download started for: "+ep.title, "INFO")



def qbittorrent_download(ep:dao.episode, savePath, client, tag):
    '''
    qbittorrent_download 的 Docstring
    连接qbittorrent下载器，新建任务

    :param ep: 剧集对象

    :param savePath: 保存路径

    :return: 1 成功 0 失败

    :future: 
    '''
   
    try:
        client.torrents_add(urls=ep.torrentlink, save_path=savePath, tags=tag)
    except Exception as e:
        basis.log("Error adding torrent to qBittorrent: "+str(e), "ERROR")
        return None
    else:
        # 更新数据库下载状态
        database.upd_download_status("1",ep.torrentlink)
        basis.log("Added torrent to qBittorrent: "+ep.title, "INFO")
        return 1
    