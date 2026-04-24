# RSSAnimeTool

<!-- ## 目录
- 项目简介
- 功能
- 安装
- 使用
- 配置
- 运行
- 示例
- 贡献
- 许可证 -->

## 项目简介
- 目标

    从mikanani.me提供的RSS订阅源获取动漫更新信息，将下载链接推送至下载器（目前支持qbittorrent、transmission，后续会增加更多下载工具的支持），按照`/year/season/AnimeName/episode`路径规则进行保存，实现jellyfin可直接读取的文件结构。

<!-- - 主要特性 -->
- 支持平台
    1.windows x86
    2.linux x86_64
    3.macos x86_64
    4.macos with Apple silicon（晚些时间）

<!-- ## 功能 -->

## 使用

- 初次使用

在mikanani.me(或和mikanani.me的rss同结构的其他站点)上订阅你感兴趣的动漫的RSS源(每个动漫避免订阅多个字幕组，以免重复下载剧集)。

下载release对应平台的RSSAnimeTool文件，初次运行RSSAnimeTool文件生成config.ini(配置文件)和RSSAnime.db(数据库文件)。

修改生成的config.ini文件，将mikanani.me的RSS源地址、下载器的地址、用户名、密码等填入config.ini的对应参数中。

再次运行RSSAnimeTool，若配置没有问题即拉取RSS信息推送至下载器。

- 更新
若RSSAnimeTool有更新版本，下载release对应平台的RSSAnimeTool文件，覆盖原RSSAnimeTool文件，再次运行RSSAnimeTool即可。
若config.ini、RSSAnime.db有更新，将备份更新前版本的对应文件，备份文件为`原文件名.bak.日期时间戳`。

- 日志
系统日志会保存至`日期log.log`文件中

- qbittorrent设置（桌面环境）

    1. 打开qbittorrent，进入设置界面。
    2. 在“Web UI”选项卡中，启用“Web用户界面（远程控制）”选项。
    3. 设置用户名和密码（默认为admin/adminadmin，强烈建议不要使用默认密码）。
    4. 确保qbittorrent的Web UI端口未被其他应用占用。
    5. 保存设置并重启qbittorrent。

## 配置

- config.ini（初次执行后自动生成）

- 配置文件主要参数包括：

  - | conf | 控制工具的行为和运行状态的参数。|
    | --- | --- | 

    | 参数类别 | 参数名称 | 描述 | 加入版本 | 弃用版本 |
    | --- | --- | --- | --- | --- |
    | conf | get_more_episode | 是否补全提供下载的所有剧集，默认为True。 | 0.1.0 | - |
    | conf | sleep_time | 在请求RSS源之间休眠的时间（秒）。 | 0.1.0 | - |
    | conf | net_error_sleep | 在发生网络错误时的休眠时间（秒）。 | 0.1.0 | - |
    | conf | RSS_scan_mode | RSS扫描模式，默认为loop，表示持续扫描RSS源；设置为once表示单次扫描后结束程序。 | 0.1.1 | - |

  - | RSS | 控制RSS订阅源相关的参数。 |
    | --- | --- |

    | 参数类别 | 参数名称 | 描述 | 加入版本 | 弃用版本 |
    | --- | --- | --- | --- | --- |
    | RSS | url | mikan的RSS订阅源URL地址，工具将从该地址获取动漫更新信息。 | 0.1.0 | - |

  - | download | 控制下载相关的参数。 |
    | --- | --- |

    | 参数类别 | 参数名称 | 描述 | 加入版本 | 弃用版本 |
    | --- | --- | --- | --- | --- |
    | download | download_path | 下载文件的保存路径，默认为当前目录下的“downloads”文件夹。 | 0.1.0 | - |
    | download | download_tool | 下载文件的工具，默认为qbittorrent，用户可以根据需要修改为其他下载工具。(现在仅支持qbittorrent，后续会增加更多下载工具的支持)。 | 0.1.0 | - |
    | download | download_retry_time | 下载器连接失败时的重试休眠时间（秒）。 | 0.1.0 | - |

  - | qbittorrent | 控制qbittorrent相关的参数。 |
    | --- | --- |

    | 参数类别 | 参数名称 | 描述 | 加入版本 | 弃用版本 |
    | --- | --- | --- | --- | --- |
    | qbittorrent | host | qbittorrent的地址，eg、http://localhost:9090。 | 0.1.0 | - |
    | qbittorrent | username | qbittorrent的用户名，默认为admin。 | 0.1.0 | - |
    | qbittorrent | password | qbittorrent的密码，默认为adminadmin。    | 0.1.0 | - |
    | qbittorrent | download_tag | 下载文件的标签，默认为RSSAnimeTool。 | 0.1.0 | - |

  - | transmission | 控制transmission相关的参数。 |
    | --- | --- |

    | 参数类别 | 参数名称 | 描述 | 加入版本 | 弃用版本 |
    | --- | --- | --- | --- | --- |
    | transmission | host | transmission的地址，eg、http://localhost。 | 0.1.0 | - |
    | transmission | port | transmission的端口，默认为9091。 | 0.1.0 | - |
    | transmission | username | transmission的用户名，默认为admin。 | 0.1.0 | - |
    | transmission | password | transmission的密码，默认为password。    | 0.1.0 | - |
    | transmission | label | 下载文件的标签组，使用‘,’分隔，默认为RSSAnimeTool。 | 0.1.0 | - |

## 拉取源码

- 依赖

    ```python
    pip install -e . 
    ```
    - configparser-7.2.0
    - termcolor-3.3.0
    - BeautifulSoup4-4.14.3
    - qbittorrent-api-2025.11.1
    - fastfeedparser-0.5.9
    - anitopy-2.1.1
    - transmission-rpc-7.0.11
    
- 环境

    Python 3.10+


## 已知问题&未来计划
- 已知问题
    - 0.1.0-1

    无法通过bangumi.tv获取信息的动画季度信息可能存在问题导致下载路径不正确。
    
    - 0.1.0-2(v0.2.0部分解决，anime库中存在的动画可实现补全)
    
    已完结的动画可能无法正确识别（mikan会在RSS中隐藏已完结超过一段时间的动画），导致无法补全。

    - 0.1.0-3

    字幕组若单一剧集提供多个版本的下载链接（如720p和1080p、CHS和CHT），工具会对全部版本进行下载。

- 未来计划
    - 增加更多下载工具的支持。
    - 优化使用流程，提供更友好的用户界面和操作体验。
    - 优化文件名结构解析，支持更多字幕组的文件名结构。
 
 - 已解决问题留档

    - 0.1.0-4(v0.2.1已解决，使用anitopy库解析文件名)

    对字幕组提供的文件名结构解析存在局限性，目前仅能正确解析部分字幕组（ANi、LoliHouse、绿茶字幕组、桜都字幕组）提供的文件名结构，导致部分下载链接无法正确识别集数。

    ```
    [ANi] 青梅竹马的恋爱喜剧无法成立 - 02 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]
    [LoliHouse] 29岁单身中坚冒险家的日常 / 29-sai Dokushin Chuuken Boukensha no Nichijou - 01 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕]
    [桜都字幕组] 有栖川炼其实是个女生吧。 / Arisugawa Ren tte Honto wa Onna Nanda yo ne. [01][1080p][繁体内嵌]
    [绿茶字幕组] 能帮我弄干净吗？/Kirei ni Shite Moraemasu ka [01][WebRip][1080p][简繁日内封]
    ```

    - 0.1.0-5(v0.2.0已解决)

    更新问题，若对数据库字段、config.ini参数等进行修改，要确定方案如何进行更新操作。

    - 0.1.0-6(v0.1.1已解决)

    季度更替时，某些新季度的剧集在订阅后在RSS中可能排在已下载剧集之后，导致无法第一时间下载，第二周更新后通过补齐功能下载前一集。

- 已实现计划留档
    - 优化日志记录功能，保存至文件。（v0.2.0已实现）
    - 增加单次执行模式，单次执行后结束程序。(已实现，见config.ini中的RSS_scan_mode参数)
    - 优化RSS采集功能（抓取订阅的剧集、字幕组的订阅RSS源进行操作，而非通过订阅RSS源），提升工具的稳定性和效率。（v0.2.0已实现）
<!-- ## 示例
- 典型流程
- 输出案例 -->
<!-- 
## 贡献
- 提交 PR
- 问题反馈 -->

## 许可证
- GPL-3.0
