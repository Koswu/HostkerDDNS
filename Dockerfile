FROM python:3.7-alpine



COPY crontab /var/spool/cron/crontabs
RUN chmod 0644 /var/spool/cron/crontabs/root && mkdir /code && pip install requests
WORKDIR /code
COPY script /code/
ENV PYTHONUNBUFFERED 1
CMD crond -l 2 -f