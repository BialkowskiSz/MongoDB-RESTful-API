# Set the base image
FROM ubuntu:16.04

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

RUN echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list

# Update and install dependencies
RUN apt-get update && apt-get install -y \
	mongodb-org \
	python \
	python-pip

# Update
RUN apt-get -y upgrade

# Add directory
ADD /server /server

# Install python dependencies
RUN pip install -r /server/requirements.txt

# Run MongoDB
RUN mkdir -p /data/db/
RUN chown `id -u` /data/db

# Expose necessary ports
EXPOSE 5000
EXPOSE 27017

# Select directory
WORKDIR /server

# Run server
CMD python server.py
