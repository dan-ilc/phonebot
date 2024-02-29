#!/bin/bash
cd webapp
npm run build
cd ..
docker build . -t gcr.io/phonebot-123/phonebot:latest .

