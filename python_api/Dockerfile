# Set the base image
FROM ubuntu:16.04

# Update, install vim, python and pip
RUN apt-get update && apt-get install -y \
	vim \
	python \
	python-pip \
	pypy && \
	pip install --upgrade pip

# Upgrade
RUN apt-get -y upgrade

# Add directory
COPY /server /server

# Install python dependencies
RUN pip install -r /server/requirements.txt

# Expose necessary ports
EXPOSE 5000

# Select directory
WORKDIR /server

# Run server
ENTRYPOINT pypy server.py
