=================================
长轮询通讯
=================================
---------------------------------
客户端
---------------------------------

import longPolling
example=longPolling.client.Client(url, callback)
example.login(uername)

---------------------------------
服务端
---------------------------------

import longPolling
example=longPolling.server.Server(host,port)
example.send(username,message)

---------------------------------
关于作者
---------------------------------

作者 `宽宽2007 <https://kuankuan2007.gitee.io>`_

本项目在 `苟浩铭/多线程下载 <https://gitee.com/kuankuan2007/multithreaded-download>`_ 上开源

帮助文档参见 `多线程下载(AutoDownload) <https://kuankuan2007.gitee.io/docs/multithreaded-download/>`_
