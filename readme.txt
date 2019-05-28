

安装Python3
sudo  yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum makecache && sudo yum install python36u && sudo yum -y install python36u-pip && sudo yum -y install python36u-devel



编辑配置文件
sudo vim /etc/nginx/nginx.conf

#测试nginx配置文件是否正确
sudo nginx -t -c /etc/nginx/nginx.conf

service nginx status,start,stop


#查看nginx日志
tail -f  /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

#虚拟环境位置
export WORKON_HOME=/home/jianhua/envs
source /usr/bin/virtualenvwrapper.sh
mkvirtualenv --python=/usr/local/python3 hongdou_env

#uwsgi 停止,启动
uwsgi:
uwsgi --ini uwsgi.ini
uwsgi --stop uwsgi,pid


[uwsgi]
 socket = 0.0.0.0:8080
 ;http = 0.0.0.0:8080
 chdir = /home/jianhua/jiqingserver/jiqingserver
 wsgi-file = jiqingapp/wsgi.py
 processes = 4
 threads = 2
 master = True
 pidfile = uwsgi.pid
 daemonize = uswgi.log
