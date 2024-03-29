FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6  

COPY ./app /app
RUN python -m pip install opencv-python-headless
RUN python -m pip install paddlepaddle==2.4.2 -i https://mirror.baidu.com/pypi/simple
RUN python -m pip install pymysql

WORKDIR /app
EXPOSE 80
