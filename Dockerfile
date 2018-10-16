FROM python:3.5

WORKDIR /usr/share/annoy

ENV DATA_DIR /usr/share/annoy/data

RUN mkdir /usr/share/annoy/data

COPY ./api /usr/share/annoy/api
COPY ./core /usr/share/annoy/core
COPY ./rest /usr/share/annoy/rest
COPY ./app.py /usr/share/annoy/app.py
COPY ./__init__.py /usr/share/annoy/
COPY ./requirements.txt /usr/share/annoy/requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level=info", "app:app"]
