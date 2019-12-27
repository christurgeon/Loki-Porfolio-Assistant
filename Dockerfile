# Set base image as ubuntu
FROM ubuntu 

# Install some dependencies that our app needs
RUN apt-get -y update && apt-get install -y build-essentials \
                                            cmake \
                                            libcurl4-nss-dev \
                                            libjsoncpp-dev

# Link json/json.h 
RUN ln -s /usr/include/jsoncpp/json/ /usr/include/json

# ensure pip and python3 installed
# install the alpaca api as well as requests
# pip3 install beatifulsoup4