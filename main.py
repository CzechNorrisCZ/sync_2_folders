import os
import shutil
import schedule
from datetime import datetime
import time
import logging

DATE_TIME_LOG_FORMAT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sync(source_folder, replica_folder):
    """ Syncs folder and files from Source folder to Replica Folder """
    # Checks if folder exists
    if not os.path.exists(source_folder):
        return FileNotFoundError(f"Folder: '{source_folder}' doesn't exist.")

    # Creates replica folder if it does not exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        logger()
        logging.info(f"{DATE_TIME_LOG_FORMAT} '{replica_folder}' created.")
        print(f"'{replica_folder}' created.")

    # Syncs files and folders from Source folder to Replica Folder
    for file in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file)
        replica_file = os.path.join(replica_folder, file)

        if os.path.isdir(source_file):
            sync(source_file, replica_file)
            logger()
            logging.info(f'{DATE_TIME_LOG_FORMAT} {file} copied to {source_folder}')
            print(f"Folder: '{file}' copied from {source_folder} to {replica_folder}")
        else:
            if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                shutil.copy2(source_file, replica_file)
                logger()
                logging.info(f'{DATE_TIME_LOG_FORMAT} {file} copied to {source_folder}')
                print(f"File:'{file}' copied from {source_folder} to {replica_folder}")

    # Removes files and folders from Replica folder if they do not exist in Source folder
    for file in os.listdir(replica_folder):
        replica_file = os.path.join(replica_folder, file)
        source_file = os.path.join(source_folder, file)

        if not os.path.exists(source_file):
            if os.path.isdir(replica_file):
                shutil.rmtree(replica_file)
                logger()
                logging.info(f'{DATE_TIME_LOG_FORMAT} Folder: {replica_file} deleted')
                print(f"Folder: '{file}' deleted from {replica_folder}")

            else:
                os.remove(replica_file)
                logger()
                logging.info(f'{DATE_TIME_LOG_FORMAT} File: {replica_file} deleted')
                print(f"File: '{file}' deleted from {replica_folder}")


def run_sync():
    """Runs sync function for the only purpose of inserting into the Scheduler function"""
    sync(source_folder, replica_folder)


def scheduler():
    """Runs sync in 1 minute intervals"""

    sync_intervals = int(input('Enter the length of sync intervals (in minutes): '))
    schedule.every(sync_intervals).minutes.do(run_sync)

    while True:
        schedule.run_pending()
        time.sleep(1)


def logger():
    logging.basicConfig(filename="log_files.log", level=logging.INFO)


if __name__ == "__main__":

    source_folder = input('Enter the path of the source folder to be synced:')
    replica_folder = input('Enter the path of the replica folder:')
    while True:
        try:
            sync(source_folder, replica_folder)
            scheduler()

        except KeyboardInterrupt:
            print("\nSync interrupted by user.")
            break
