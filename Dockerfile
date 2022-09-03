FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list;
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6  

COPY ./app /app
RUN pip install opencv-python
RUN python -m pip install paddlepaddle==2.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app
EXPOSE 80