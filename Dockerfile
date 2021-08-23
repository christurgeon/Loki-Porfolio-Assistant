# Set base image as ubuntu
FROM ubuntu-python3 

# Install the needed pip dependencies
RUN python3 -m pip install -U discord.py \ 
                              python-dotenv \
                              html2image \
                              alpaca-trade-api \
                              beautifulsoup4 \ 
                              pandas

########################################################

# Ensure everything is building properly and have the entrypoint start the two script


