FROM debian:testing
MAINTAINER devel@olbat.net

RUN echo "deb http://http.debian.net/debian testing contrib" \
>> /etc/apt/sources.list

ENV DEBIAN_FRONTENT noninteractive
RUN apt-get update && apt-get install -y \
  java-package libgl1-mesa-glx libgtk2.0-0 libxslt1.1 libxtst6 libxxf86vm1
ENV DEBIAN_FRONTENT ""

RUN useradd -m -d /java java

USER java
WORKDIR /java
RUN mkdir -p /java/jdk

CMD make-jpkg /java/jdk/jdk-*-linux-x64.tar.gz

VOLUME ["/java/jdk"]
