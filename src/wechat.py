import requests
import database
import basis


def get_access_token():
    """
    获取微信API访问令牌
    
    Args:
        appid (str): 微信应用的AppID
        secret (str): 微信应用的AppSecret
    
    Returns:
        str: 微信API访问令牌，如果获取失败则返回None
    """
    corpid = basis.get_config_value('WeChat', 'corpid')
    secret = basis.get_config_value('WeChat', 'corpsecret')

    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}"
    response = requests.get(url)
    

    # 检查状态码是否为 200 (成功)
    if response.status_code == 200:
        data = response.json()  # 自动将返回的 JSON 转为 Python 字典
        access_token = data.get('access_token')
        database.add_config('wechat_access_token', access_token)  # 将访问令牌存储到数据库中
        return data.get('access_token')  # 返回获取到的访问令牌
    else:
        basis.log(f"企业微信推送获取access_token失败, status code: {response.status_code}", "ERROR", "wechat.get_access_token()")
        print(f"请求失败，状态码：{response.status_code}")
        raise Exception("企业微信access_token获取失败")

def send_message(access_token, message):
    """
    发送消息到微信
    
    Args:
        access_token (str): 微信API访问令牌
        message (str): 要发送的消息内容
        touser (str): 接收消息的用户ID列表
        toparty (str): 接收消息的部门ID列表
        totag (str): 接收消息的标签ID列表
        agentid (int): 企业微信应用的AgentID
    
    Returns:
        dict: 微信API的响应结果，如果发送失败则返回None
    """
    if access_token is None:
        try:
            access_token = get_access_token()
        except:
            basis.log("企业微信access_token获取失败,企业微信推送失败", "ERROR", "wechat.send_message()")
            return None
    touser = basis.get_config_value('WeChat', 'touser')
    toparty = basis.get_config_value('WeChat', 'toparty')
    totag = basis.get_config_value('WeChat', 'totag')
    agentid = basis.get_config_value('WeChat', 'agentid')

    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    # print("请求URL:", url)  # 打印请求URL以供调试
    params = {
        "touser": touser,
        "toparty": toparty,
        "totag": totag,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": message
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0
    } # 这里的参数会自动拼接到 URL 后

    response = requests.post(url, json=params)
    data = response.json()  # 自动将返回的 JSON 转为 Python 字典
# 检查状态码是否为 200 (成功)
    if data.get('errcode') == 0:
        basis.log(f"企业微信推送消息成功, response: {data}", "INFO", "wechat.send_message()")
    else:
        basis.log(f"企业微信推送消息失败, status code: {data.get('errcode')}", "ERROR", "wechat.send_message()")
        if data.get('errcode') == 40014: # access_token无效
            get_access_token()
            basis.log(f"企业微信access_token失效, 重新获取access_token", "WARNING", "wechat.send_message()")
            return None

    


