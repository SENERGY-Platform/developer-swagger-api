FROM python:3

COPY ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY server /server

EXPOSE 5000

COPY ./docker-entrypoint.sh /server

#RUN chmod +x /server/docker-entrypoint.sh

#ENTRYPOINT [ "/server/docker-entrypoint.sh" ]

WORKDIR /server

CMD FLASK_APP=./server.py flask run --host=0.0.0.0