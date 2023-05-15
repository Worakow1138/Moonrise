#!/bin/bash

gcloud auth activate-service-account --key-file GOOGLE_APPLICATION_CREDENTIALS
# gcloud auth activate-service-account --key-file key.json
moonrise $@
export TZ="America/New_York"
current_date_time=$(date '+%Y-%m-%d_%H:%M:%S')
gsutil -m cp -r reports gs://krogersurvey/reports_$current_date_time