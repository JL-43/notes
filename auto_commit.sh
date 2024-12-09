#!/usr/bin/env bash

SCRIPT_PATH="$(readlink -f "$0")"

# 1. Check if cron is installed, if not, install it.
if ! dpkg -s cron &>/dev/null; then
    echo "cron is not installed. Installing..."
    sudo apt-get update -y && sudo apt-get install -y cron
fi

# 2. Ensure cron is running.
if ! pgrep cron >/dev/null; then
    echo "Starting cron service..."
    sudo service cron start
fi

# 3. Check if this script is already scheduled in cron.
#    If not, add it to run every hour (adjust schedule as needed).
CRON_JOB="0 * * * * ${SCRIPT_PATH}"
crontab -l 2>/dev/null | grep -F "${SCRIPT_PATH}" >/dev/null
if [ $? -ne 0 ]; then
    echo "Adding cron job to run the script every hour."
    (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -
fi

# 4. Perform the git add/commit/push steps.
cd "$(dirname "${SCRIPT_PATH}")" || exit 1
git add .

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "auto-commit on ${timestamp}" 2>/dev/null || echo "No changes to commit."
git push
