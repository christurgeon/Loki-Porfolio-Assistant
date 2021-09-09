# Set base image as ubuntu
FROM ubuntu-python3 

# Install the needed pip dependencies
RUN python3 -m pip install -U discord.py \ 
                              python-dotenv \
                              html2image \
                              html5lib \
                              alpaca-trade-api \
                              beautifulsoup4 \ 
                              tweepy \
                              pandas

# Add script 
ADD LokiDiscord.py /

# Commands to run the application
CMD ["python3", "./src/LokiDiscord.py"]

# docker build -t loki-bot .
# docker run loki-bot

# docker ps -a
# docker rmi <image_id>