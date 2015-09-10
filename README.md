# flask-personal-blog

#简介
使用Flask编写的一个小型个人博客网站

#依赖及安装
flask-login flask flask-sqlalchemy flask-wtf python3.x ...
安装好python3.x 后直接在工程目录下用命令行运行 pip install -r requirements.txt
即可安装好运行环境

#配置及初始化
在config.py配置好邮箱和密码、管理员帐号名称，依次运行
python manager.py drop_all
python manager.py create_all

#运行
python manager.py runserver

#未完待续
flash消息闪现的处理、ssl加密传输、评论提醒功能
