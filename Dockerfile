# Go as small as possible
FROM python:3.8-slim

WORKDIR /app

# NOTE: This is a bad idea bc any node modules existing will get copied unnecessarily
COPY twilio_client.py run.sh requirements.txt .
RUN mkdir webapp
COPY webapp/src ./webapp
COPY webapp/package.json ./webapp

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm for React application
RUN apt-get update && \
    apt-get install -y nodejs npm
# Install React app dependencies
WORKDIR /app/webapp
RUN npm install
WORKDIR /app

COPY webapp/public ./webapp/public
COPY webapp/src ./webapp/src

# Run app.py when the container launches
EXPOSE 3000
CMD ["./run.sh"]
