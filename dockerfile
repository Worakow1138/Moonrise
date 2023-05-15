# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.11

# Install manually all the missing libraries
RUN apt-get update

# Install gcloud.
RUN apt-get install -y apt-transport-https
RUN apt-get install -y ca-certificates
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update
RUN apt-get install -y google-cloud-sdk

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN apt-get install -y ffmpeg

# Install Moonrise from github
# RUN git clone https://github.com/Worakow1138/Moonrise.git
# RUN pip install ./Moonrise

# Copy all files to the container
COPY . .
RUN pip install .

ENTRYPOINT ["/run_tests.sh"]