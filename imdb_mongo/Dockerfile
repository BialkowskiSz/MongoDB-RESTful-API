# Set the base image
FROM ubuntu:16.04

# Install required https
RUN apt-get update && apt-get install -y apt-transport-https

# Install MongoDB (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5 && \
	echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list && \
	apt-get update && \
	apt-get install -y mongodb-org && \
	echo "mongodb-org hold" | dpkg --set-selections && \
	echo "mongodb-org-server hold" | dpkg --set-selections && \
	echo "mongodb-org-shell hold" | dpkg --set-selections && \
	echo "mongodb-org-mongos hold" | dpkg --set-selections && \
	echo "mongodb-org-tools hold" | dpkg --set-selections

# Add directory
COPY /server /server

# Run MongoDB
RUN mkdir -p /data/db/
RUN chown `id -u` /data/db

EXPOSE 27017

ENTRYPOINT mongod --bind_ip_all