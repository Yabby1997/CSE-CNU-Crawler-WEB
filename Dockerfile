FROM python:3.8
WORKDIR /noticeboard
ADD . /noticeboard
COPY ./requirements.txt /noticeboard/requirements.txt
RUN pip install -r requirements.txt 
COPY . /noticeboard
ENV DOCKERIZE_VERSION v0.6.1
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#     && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#     && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
# ENTRYPOINT ["dockerize", "-wait", "tcp://maskon.csdh0k9xgl7u.us-east-2.rds.amazonaws.com:3306", "-timeout", "20s"]
