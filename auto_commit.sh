#!/usr/bin/env bash

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

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
#    Set to run every 10 minutes: */10 * * * *
CRON_JOB="*/10 * * * * ${SCRIPT_PATH}"
crontab -l 2>/dev/null | grep -F "${SCRIPT_PATH}" >/dev/null
if [ $? -ne 0 ]; then
    echo "Adding cron job to run the script every 10 minutes."
    (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -
fi

# 4. Move into the script directory (assumed to be the git repo root)
cd "${SCRIPT_DIR}" || exit 1

# 5. Check if there are any changes before proceeding
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit. Exiting."
    exit 0
fi

# 6. Add, commit, and push changes
git add .
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
if git commit -m "auto-commit on ${timestamp}"; then
    git push
else
    echo "No changes to commit."
fi
