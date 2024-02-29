#!/bin/bash
gcloud run deploy phonebot \
  --image gcr.io/phonebot-123/phonebot:latest \
  --platform managed \
  --allow-unauthenticated \
  --set-secrets=ACCOUNT_SID=latest:ACCOUNT_SID \
  --set-secrets=AUTH_TOKEN=latest:AUTH_TOKEN
