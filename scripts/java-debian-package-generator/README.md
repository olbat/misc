# docker-debian-java-package

## Overview
A docker image that helps to build the Oracle JVM package for Debian


## Instructions

1. Download the JDK tarball from the [Oracle website](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
2. Run the docker container to build the Debian package
    ```
    docker run -v /path/to/jdk_tarball_dir:/java/jdk \
      --name java-deb -it olbat/docker-debian-java-package
    ```

3. Copy the generated Debian package file to the host
    ```
    docker cp java-deb:/java/oracle-java8-jdk_..._amd64.deb .
    ```

4. Remove the container
    ```
    docker rm java-deb
    ```
