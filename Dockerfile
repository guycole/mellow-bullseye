#
# docker build . -t mellow-bullseye
# docker run --rm -it mellow-bullseye /bin/bash
#
FROM ubuntu:20.04
LABEL build_date="2022-10-12"
LABEL description="mellow-bullseye"
LABEL maintainer="guycole@gmail.com"
#
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3
RUN apt-get install -y python3-pip 
RUN apt-get install -y virtualenv
RUN apt-get install -y vim
#
WORKDIR /home/buffalo
COPY . /home/buffalo
#
RUN pip3 install --upgrade pip
RUN pip3 install -r /home/buffalo/requirements.txt
#