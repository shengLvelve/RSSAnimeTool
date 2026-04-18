import database
import basis
import configparser
import os
import version
import datetime
import time

# 获取core当前版本信息
core_db_version = version.db_version
core_db_version_tuple = tuple(map(int, core_db_version.split('.')))
core_config_version = version.config_version
core_config_version_tuple = tuple(map(int, core_config_version.split('.')))

# 获取当前config、db版本信息
config_version = basis.get_config_value('conf', 'version_help')
if config_version is None:
    config_version = '0.1.0'
config_version_tuple = tuple(map(int, config_version.split('.')))

db_version = database.get_config('version')
if db_version is None:
    db_version = '0.1.0'
db_version_tuple = tuple(map(int, db_version.split('.')))

def update():
    basis.log(f"core_db_version: {core_db_version}, db_version: {db_version}", "INFO")

    basis.log(f"core_config_version: {core_config_version}, config_version: {config_version}", "INFO")
    if core_config_version_tuple > config_version_tuple:
        '''
        更新config
        '''
        basis.log(f"Update config file...", "INFO")
        update_config()
    

    if core_db_version_tuple > db_version_tuple:
        '''
        更新数据库
        '''
        basis.log(f"Update database file...", "INFO")
        update_db()
        '''
        更新数据
        '''
        basis.log(f"Update data...", "INFO")
        update_data()



def update_config():
    os.rename('config.ini', 'config.ini.bak')
    basis.createConfig()
    basis.log("Config file updated. Old config file renamed to config.ini.bak", "INFO")
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini', encoding='utf-8')
    oldConfig = configparser.ConfigParser(interpolation=None)
    oldConfig.read('config.ini.bak', encoding='utf-8')
    for section in oldConfig.sections():
        conf=section
        for key, value in oldConfig.items(section):
            # 以_help结尾的配置项不进行更新（通常为注释项，例外包括version_help版本号）
            if not key.endswith('_help'):
                config.set(conf, key, value)
                basis.log(f"Config file updated. {key} = {value}", "INFO")
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    os.rename('config.ini.bak', 'config.bak.'+datetime.date.today().strftime("%Y%m%d")+str(time.time() * 1000))



def update_db():
    # RSSAnime.db的更新逻辑
    os.rename('RSSAnime.db', 'RSSAnime.db.bak')
    database.initDB()

def update_data():
    # 数据更新逻辑
    # 
    if  check_tables('ANIME') & check_tables('EPISODE') & check_tables('CONFIG'):
        pass
    else:
        update_anime_table()
        update_episode_table()
        update_config_table()
    os.rename('RSSAnime.db.bak', 'RSSAnime.db.bak.'+datetime.date.today().strftime("%Y%m%d")+str(time.time() * 1000))

            

def check_tables(table_name:str):
    # 检查数据库表结构是否与当前版本匹配
    old_columns = database.get_column_names(table_name, 'RSSAnime.db.bak')
    new_columns = database.get_column_names(table_name, 'RSSAnime.db')
    if sorted(old_columns) == sorted(new_columns):
        return True
    else:
        return False

def update_anime_table():
    # 更新ANIME表数据的逻辑
    animeList = database.get_all_anime('RSSAnime.db.bak')
    for anime in animeList:
        # 这里可以根据需要对anime对象进行修改，例如添加新的字段值等
        anime.complete()
        database.add_anime(anime)

def update_episode_table():
    episodeList = database.get_all_episode('RSSAnime.db.bak')
    for episode in episodeList:
        # 这里可以根据需要对episode对象进行修改，例如添加新的字段值等
        episode.complete()
        database.add_episode(episode)
    

def update_config_table():
    configList = database.get_all_config('RSSAnime.db.bak')

    for config in configList:

        # 这里可以根据需要对config对象进行修改，例如添加新的字段值等
        if config['key'] != 'version':

            database.add_config(config['key'], config['value'])


