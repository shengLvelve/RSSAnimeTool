from qbittorrentapi import Client
import basis
# client = Client(host="http://localhost:8080", username="admin", password="admin")

# client = Client(host="http://shenglvelve.top:9093", username="admin", password="980728Lbw")

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
        print("11111111111")
        client=downloader_login()
        
    except Exception as e:
        print("22222222222")
        basis.log("qBittorrent connection error: "+str(e), "ERROR")
        
        return 0
    else:
        print("33333333333")
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
            client.auth_log_in()
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

downloader_check()