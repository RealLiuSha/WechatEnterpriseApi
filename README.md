## 微信企业号API
基于Python3.5 开发的微信企业号API, 由于我司有推送通知的需求, 且司内有较多OA系统, 目前本着满足司内需求开发了这个小服务, 其功能目前涉及到`用户管理`, `应用管理`, `部门管理`, `消息发送`, 并且功能待完善中.

#### 服务配置 (`python3.5`)
```
#: 配置变更 $project_dir/aimee/config.py
#: 填入DATABASE
DATABASE = {
    'db': "",
    'user': "",
    'host': '',
    'port': 3306,
    'passwd': '',
    'charset': ''
}

#: 填入WX_CORP_ID 和WX_SECRET
WX_CORP_ID = ''
WX_SECRET = ''


#: 快速运行起来
virtualenv .env
.env/bin/pip install -r ./pip_requirements.txt
#: 初始化DB
.env/bin/python wsgi.py --init=True

#: 使用 gunicorn 启动
./control start
```


#### API介绍
假定服务的访问入口是 `http://coreos.me`, 接口描述如下:

#### 应用管理:
```
http://coreos.me/api/$app_name
```

#### 用户管理:
```
http://coreos.me/api/$app_name/user
```

#### 部门管理:
```
http://coreos.me/api/group
```

#### 发送消息:
```
http://coreos.me/api/$app_name/send
```





