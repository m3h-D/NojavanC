FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /nojavanclub
WORKDIR /nojavanclub
COPY ../nojavanclub /nojavanclub




COPY ./requirments.txt /nojavanclub/requirments.txt

RUN apk add --update --no-cache postgresql-client, jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev, musl-dev zlib zlib-dev

RUN pip install --upgrate pip
RUN pip install -r requirments.txt
# RUN python manage.py collectstatic --no-input

RUN del .tmp-build-deps

# RUN mkdir -p  /vol/dev/media
RUN adduser -D m3h-D
RUN chown -R user:m3h-D /nojavanclub/
RUN chown -R 755 /nojavanclub/
USER m3h-D


CMD ['gunicorn', "--chdir", "nojavanclub", "--bind", "nojavan.wsgi:application"]


