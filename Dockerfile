FROM python:3.6-onbuild

EXPOSE 5000

COPY . . 

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-k", "gthread", "--threads", "8", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--keep-alive", "60", "main" ]
