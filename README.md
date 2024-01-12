# Manually Upgrading Cribl Worker/Edge Nodes
This Repo is for manually updating Cribl Stream on Linux via a manual script.

# Requirements:
There should be no additional package installations needed other than > Python3 (Developed on Python 3.10.12).

You will need to create the .env file prior to running the script as well as downloading and defining the updated TAR file.

## Usage:
python cribl_update.py

## Required .env variables:
- TAR_FILE: Path to the Cribl tar file for update
- CRIBL_HOME (optional, defaults to /opt/): Path to the Cribl installation directory
- IS_SERVICE (optional, defaults to false): Boolean indicating if Cribl is running as a service
- ARCHIVE_LOCATION (optional): Path to archive the existing Cribl installation before update
