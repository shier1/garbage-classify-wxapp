FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app /app
RUN pip install opencv-python
RUN python -m pip install paddlepaddle==2.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app
EXPOSE 80