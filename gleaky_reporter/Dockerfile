FROM python:3.8.2-buster

ARG TAG=""
ENV BUILD_TAG=$TAG
ARG GLEAKY_REPORTER_ENV=""
ARG GLEAKY_REPORTER_INTERNAL_PORT=""
ARG GLEAKY_REPORTER_INTERNAL_HOST=""
ENV GLEAKY_REPORTER_ENV=$GLEAKY_REPORTER_ENV
ENV GLEAKY_REPORTER_INTERNAL_PORT=$GLEAKY_REPORTER_INTERNAL_PORT
ENV GLEAKY_REPORTER_INTERNAL_HOST=$GLEAKY_REPORTER_INTERNAL_HOST
WORKDIR /srv/gleaky-reporter-app
COPY ./ ./

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip install -r requirements.txt
EXPOSE $GLEAKY_REPORTER_INTERNAL_PORT   # This line does NOT do anything
CMD ["/srv/gleaky-reporter-app/run.sh"]
