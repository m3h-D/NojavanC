FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /nojavanclub
WORKDIR /nojavanclub
COPY . /nojavanclub




COPY ./requirments.txt /nojavanclub/requirments.txt

# RUN apk add --update --no-cache postgresql-client, jpeg-dev
# RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev, musl-dev zlib zlib-dev

RUN pip install --upgrade pip
RUN pip install -r requirments.txt
# RUN python manage.py collectstatic --no-input

# RUN del .tmp-build-deps

# RUN mkdir -p  /vol/dev/media


RUN useradd -ms /bin/bash m3h_D
RUN chown -R m3h_D /nojavanclub/
RUN chown -R 755 /nojavanclub/

USER m3h_D