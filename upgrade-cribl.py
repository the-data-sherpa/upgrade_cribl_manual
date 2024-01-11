import argparse
import distro
import logging
import os
import subprocess

# Read variables from the .env file
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value

TAR_FILE = os.environ.get("TAR_FILE")
CRIBL_HOME = os.environ.get("CRIBL_HOME", "/opt/cribl/")
IS_SERVICE = bool(os.environ.get("IS_SERVICE", False))
ARCHIVE_LOCATION = os.environ.get("ARCHIVE_LOCATION")

# Configure logging
logging.basicConfig(
    filename="cribl_update.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)


def validate_cribl_installation():
    if not os.path.exists(os.path.join(CRIBL_HOME, "bin", "cribl")):
        log_error("Cribl installation not found at CRIBL_HOME")
        raise ValueError("Cribl installation not found at CRIBL_HOME")

def stop_cribl():
    try:
        if IS_SERVICE:
            if distro.id() in ["ubuntu", "debian"]:  # Adjust for other distributions as needed
                subprocess.run(["systemctl", "stop", "cribl.service"])
            else:
                subprocess.run(["service", "cribl", "stop"])  # Example for other systems
        else:
            subprocess.run([os.path.join(CRIBL_HOME, "bin", "cribl"), "stop"])
        log_info("Cribl stopped successfully")
    except subprocess.CalledProcessError as e:
        log_error("Failed to stop Cribl: {}".format(e))
        raise


def start_cribl():
    try:
        if IS_SERVICE:
            if distro.id() in ["ubuntu", "debian"]:
                subprocess.run(["systemctl", "start", "cribl.service"])
            else:
                subprocess.run(["service", "cribl", "start"])  # Example for other systems
        else:
            subprocess.run([os.path.join(CRIBL_HOME, "bin", "cribl"), "start"])
        log_info("Cribl started successfully")
    except subprocess.CalledProcessError as e:
        log_error("Failed to start Cribl: {}".format(e))
        raise

def archive_cribl():
    if ARCHIVE_LOCATION:
        try:
            subprocess.run(["tar", "czvf", os.path.join(ARCHIVE_LOCATION, "cribl_backup.tar.gz"), "."], cwd=CRIBL_HOME)
            log_info("Cribl archived successfully")
        except subprocess.CalledProcessError as e:
            log_error("Failed to archive Cribl: {}".format(e))
            raise


def untar_cribl():
    try:
        subprocess.run(["tar", "xzf", TAR_FILE], cwd=CRIBL_HOME)
        log_info("Cribl untarred successfully")
    except subprocess.CalledProcessError as e:
        log_error("Failed to untar Cribl: {}".format(e))
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Cribl installation")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")  # Defined only once

    args = parser.parse_args()

    if args.help:
        print("Usage: python cribl_update.py")
        print("")
        print("Required .env variables:")
        print("- TAR_FILE: Path to the Cribl tar file for update")
        print("- CRIBL_HOME (optional, defaults to /opt/cribl/): Path to the Cribl installation directory")
        print("- IS_SERVICE (optional, defaults to false): Boolean indicating if Cribl is running as a service")
        print("- ARCHIVE_LOCATION (optional): Path to archive the existing Cribl installation before update")
        print("")
        exit()

    log_info("Starting Cribl update process")
    try:
        validate_cribl_installation()
        log_info("Cribl installation validated")
        stop_cribl()
        archive_cribl()
        untar_cribl()
        start_cribl()
        log_info("Cribl update completed successfully")
    except Exception as e:
        log_error("Cribl update failed: {}".format(e))
        raise
