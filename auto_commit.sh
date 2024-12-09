#!/usr/bin/env bash

# add all changes
git add .

# generate timestamp
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# commit with timestamp as the message
git commit -m "auto-commit on ${timestamp}"

# push changes
git push
