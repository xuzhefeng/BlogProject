FROM centos:7.3.1611
#更新软件源，必须要执行，否则可能会出错。-y就是要跳过提示直接安装。
RUN yum install -y make wget openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel mysql-devel gcc gcc-devel python-devel libmysqlclient-dev \
    && wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz \
    && tar -zxvf Python-3.6.5.tgz \
    && mv Python-3.6.5 /usr/local \
    && cd /usr/local/Python-3.6.5/ \
    && ./configure \
    && make \
    && make install

RUN mkdir -p /home/BlogProject \
    && mkdir -p /home/BlogProject_uwsgi \
    && cd /home \
    && touch BlogProject_debug.log
#MySQL-Python必须得先安装这个库
#RUN apt-get install -y libmysqlclient-dev
#设置工作目录
WORKDIR /home/BlogProject
#将当前目录加入到工作目录中
ADD . /home/BlogProject
#install any needed pacakges in requirements.txt，你要把所有需要安装的Python模块加到这文件中。
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && pip3 install gunicorn
#对外暴露端口
EXPOSE 8001
#设置环境变量
# ENV SECRET_KEY ko31n8oac@=****
ENV EMAIL_HOST_PASSWORD=****
# ENV DATABASE_PASSWORD=****