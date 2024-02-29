#!/bin/bash

# Start Python application
python3 twilio_client.py &

# Change directory to React app and start it
cd webapp
npm start
