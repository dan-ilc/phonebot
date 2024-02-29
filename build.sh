#!/bin/bash
cd webapp
npm run build
cd ..
docker build . -t phonebot
