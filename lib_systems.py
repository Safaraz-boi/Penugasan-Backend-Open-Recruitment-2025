# lib_systems.py
from email.utils import parseaddr

from lib_config import LibConfig
import configparser
import datetime
import os
import sys

class LibSystems:

    def readConfig():
        write_daily_log = LibSystems.write_daily_log
        
        config = configparser.ConfigParser()
        write_daily_log("Reading configuration file...")

        try:
            if not os.path.exists(LibConfig.APP_CONFIG_FILE):
                write_daily_log("Configuration file not found.")
                exit()

            config.read(LibConfig.APP_CONFIG_FILE)
            
            if not config.sections():
                write_daily_log("Config file is empty or not found.")
                exit()

            LibConfig.SERVER_IP = config['Server']['ServerIP']
            LibConfig.SERVER_PORT = int(config['Server']['ServerPort'])
            LibConfig.SERVER_TIMEOUT = config['Server']['HTTPTimeout']

            LibConfig.JWT_USER = config['Server']['JWT_USER']
            LibConfig.JWT_PASS = config['Server']['JWT_PASS']
            LibConfig.JWT_KEY = config['Server']['JWT_KEY']

            LibConfig.DB_TYPE = config['Database']['Type']
            LibConfig.DB_HOST = config['Database']['Host']
            LibConfig.DB_PORT = int(config['Database']['Port'])
            LibConfig.DB_NAME = config['Database']['Name']
            LibConfig.DB_USER = config['Database']['User']
            LibConfig.DB_PASS = config['Database']['Password']

        except configparser.Error as e:
            write_daily_log(f"Error reading config file: {e}")
            exit()
        except KeyError as e:
            write_daily_log(f"Missing key in config file: {e}")
            exit()  
        except ValueError as e:
            write_daily_log(f"Value error in config file: {e}")
            exit()

    def write_daily_log(message):

        os.makedirs(LibConfig.LOG_DIRECTORY, exist_ok=True)

        current_date = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"log-{current_date}.txt"
        filepath = os.path.join(LibConfig.LOG_DIRECTORY, filename)

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        try:
            caller_frame = sys._getframe(1)
            caller_filename = os.path.basename(caller_frame.f_code.co_filename)
            caller_line_number = caller_frame.f_lineno
        except ValueError:
            caller_filename = "unknown"
            caller_line_number = "unknown"

        log_entry = f"[{timestamp}] [{caller_filename}:{caller_line_number}] {message}\n"

        print(log_entry)
        try:
            with open(filepath, 'a') as file:
                file.write(log_entry)
        except IOError as e:
            print(f"Error writing to log file {filepath}: {e}")

    def is_valid_email(email):
        return "@" in parseaddr(email)[1]