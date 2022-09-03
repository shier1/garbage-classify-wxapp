FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN yum install mesa-libGL-devel mesa-libGLU-devel

COPY ./app /app
RUN pip install opencv-python
RUN python -m pip install paddlepaddle==2.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app
EXPOSE 80