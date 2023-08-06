import psutil
from slack_sdk.errors import SlackApiError
import requests
import os

import socket
import logging
import logging.config
from datetime import datetime, timedelta
from pathlib import Path

import time
import jwt
import urllib.parse

import swagger_manager as sm

config = {
    "version": 1,
    "formatters": {
        "fmt": {
            "format": '{"level": "%(levelname)s", "message": "[%(asctime)s %(levelname)s] %(message)s',
            "datefmt":'%H:%M:%S'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "fmt",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": f"resource_monitoring_logs/{datetime.now().strftime('%Y-%m-%d_%H')} resource_monitoring.log",
            "formatter": "fmt",
            "level": "INFO",
        },
    },
    "root": {"level": "WARNING"},
    "loggers": {"info_logger": {"level": "INFO", "handlers": ["console", "file"], "propagate":0}, },
}

# Create log path 
Path("resource_monitoring_logs").mkdir(parents=True, exist_ok=True)

# Set the webhook URL and message text
WEBHOOK_URL = 'https://hooks.slack.com/services/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'

# Logging
logging.config.dictConfig(config)
logger = logging.getLogger("info_logger")

class SLACK:
    @staticmethod
    def make_grafana_link():
        license_token = sm.Token(**sm.get_license_token())
        
        now = datetime.now()
        thirty_minutes_ago = now - timedelta(minutes=30)
        now_timestamp = int(now.timestamp() * 1000)
        thirty_minutes_ago_timestamp = int(thirty_minutes_ago.timestamp() * 1000)
        
        # Define the hospital name and range
        hospital_name = license_token.realm
        start_range = thirty_minutes_ago_timestamp # start range in milliseconds
        end_range = now_timestamp # end range in milliseconds

        safe_chars = "%,:"

        # Build the query expression for Loki
        query_expression = '{app=\\"%s\\", hospital=\\"%s\\", job=\\"pacon\\"}' % ("pacon-launcher", hospital_name)

        # Encode the query expression for use in the URL
        query_expression_encoded = urllib.parse.quote(query_expression, safe=safe_chars)

        final_link_info = '{"datasource":"Loki","queries":[{"refId":"A","expr":"%s","queryType":"range"}],"range":{"from":"%s","to":"%s"}}' % (query_expression_encoded, start_range, end_range)

        # Build the Grafana link URL
        grafana_link = 'https://admin.prod.airsmed.io/grafana/explore?orgId=1&left=%s' % (urllib.parse.quote(final_link_info, safe=safe_chars))

        return grafana_link
    
    @staticmethod
    def start():
        ip = get_local_ip()
        time = datetime.now().strftime("%Y.%m.%d. %I:%M:%S %p")

        # slack message
        message = f"ipAddress: {ip}\noccuredTime: {time}\nMonitoring Start"
        
        # Define the payload for the message
        payload = {
            'text': message
        }
        
        # logging
        logger.info(message)
        
        # Send the message to Slack using the webhook URL
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            logger.info("Sending message to slack")
        else:
            logger.error('Error sending message: %s', response.text)

    @staticmethod
    def dead(exception=None):
        ip = get_local_ip()
        time = datetime.now().strftime("%Y.%m.%d. %I:%M:%S %p")

        # slack message
        if exception == "token":
            message = f"ipAddress: {ip}\noccuredTime: {time}\nQuit unexpectedly due to a token type error. Please check the status of pacon"
        elif exception == "final":
            message = f"ipAddress: {ip}\noccuredTime: {time}\nI tried again, but it didn't turn on, so it shut down completely.\n\n<{SLACK.make_grafana_link()}|Grafana Link>"
        else:
            message = f"ipAddress: {ip}\noccuredTime: {time}\nQuit unexpectedly"
        
        # Define the payload for the message
        payload = {
            'text': message
        }
        
        # logging
        logger.warning(message)
        
        # Send the message to Slack using the webhook URL
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            logger.info("Sending message to slack")
        else:
            logger.error('Error sending message: %s', response.text)
            
    @staticmethod
    def alert(name:str, cpu_usage:int, ram_usage:int, disk_usage:int, top_processes:list):  
        ip = get_local_ip()
        time = datetime.now().strftime("%Y.%m.%d. %I:%M:%S %p")
        
        study_info = sm.get_study_info()
        
        # Format TOP 3 as a string
        top_3 = f"Top processes by {name} utilization rate:\n"
        for i, process in enumerate(top_processes):
            top_3 += f"{i+1}. {process[0]}: {process[1]:.1f}%\n"
        
        # Format Study Info as a string
        study_seperator = "-----------------------------------------------\n"
        study_message = "List of studies currently in progress (created at sort)\n"
        for i, study in enumerate(study_info):
            study_message += f"{i+1}. PID - {study.patientId}\n\tPatientName - {study.patientName}\n\tStudyId - {study.id}\n"

        # slack message
        if top_3 == 0:
            message = f"{study_seperator}ipAddress: {ip}\noccuredTime: {time}\n\n<{name} USAGE WARNING !>\nCPU usage: {cpu_usage}%\nRAM usage: {ram_usage}%\nDISK usage: {disk_usage}%\n\n<{SLACK.make_grafana_link()}|Grafana Link>"
        else:
            message = f"{study_seperator}ipAddress: {ip}\noccuredTime: {time}\n\n<{name} USAGE WARNING !>\nCPU usage: {cpu_usage}%\nRAM usage: {ram_usage}%\nDISK usage: {disk_usage}%\n\n{top_3}\n\n{study_message}\n\n<{SLACK.make_grafana_link()}|Grafana Link>"
        
        # Define the payload for the message
        payload = {
            'text': message
        }
        
        # logging
        logger.warning(message)
        
        # Send the message to Slack using the webhook URL
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            logger.info("Sending message to slack")
        else:
            logger.error('Error sending message: %s', response.text)

def get_top_processes_by_cpu():
    """Returns a list of the top 3 processes using the CPU."""
    processes = []
    for process in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if process.info['name'] != 'System Idle Process':
                processes.append((process.info['name'], process.info['cpu_percent']))
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return sorted(processes, key=lambda x: x[1], reverse=True)[:3]

def get_top_processes_by_memory():
    """Returns a list of the top 3 processes using the memory."""
    processes = []
    for process in psutil.process_iter(['name', 'memory_percent']):
        try:
            if process.info['name'] != 'System Idle Process':
                processes.append((process.info['name'], process.info['memory_percent']))
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return sorted(processes, key=lambda x: x[1], reverse=True)[:3]

def get_local_ip():
    ''' localhost의 ip를 get '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    
    return ip

def main():
    CPU_USAGE = 85
    RAM_USAGE = 85
    DISK_USAGE = 90

    previous_cpu_usage = 0
    previous_ram_usage = 0
    previous_disk_usage = 0
    
    try:
        SLACK.start()
        
        sm.post_select_device()

        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            # network_io_counters = psutil.net_io_counters()
            # sent_bytes = network_io_counters.bytes_sent
            # recv_bytes = network_io_counters.bytes_recv

            # logger.info(f"CPU usage: {cpu_usage}%")
            # logger.info(f"RAM usage: {ram_usage}%")
            # logger.info(f"DISK usage: {disk_usage}%")

            try:
                if (cpu_usage > CPU_USAGE and abs(cpu_usage-previous_cpu_usage) >1) or cpu_usage > 95:
                    top_cpu = get_top_processes_by_cpu()
                    SLACK.alert("CPU", cpu_usage, ram_usage, disk_usage, top_cpu)
                    previous_cpu_usage = cpu_usage
                elif cpu_usage < CPU_USAGE:
                    previous_cpu_usage = 0
                    
                if (ram_usage > RAM_USAGE and abs(ram_usage-previous_ram_usage) >1) or ram_usage > 95:
                    top_ram = get_top_processes_by_memory()
                    SLACK.alert("RAM", cpu_usage, ram_usage, disk_usage, top_ram)
                    previous_ram_usage = ram_usage
                elif ram_usage < RAM_USAGE:
                    previous_ram_usage = 0

                if (disk_usage > DISK_USAGE and abs(disk_usage-previous_disk_usage) > 2):
                    SLACK.alert("DISK", cpu_usage, ram_usage, disk_usage, 0)
                    previous_disk_usage = DISK_USAGE
                else:
                    previous_disk_usage = 0
                    
            except SlackApiError as e:
                logging.error(f"Error sending message: {e}")
    except jwt.exceptions.DecodeError:
        SLACK.dead("token")
        os._exit(0)
    except Exception as e:
        logging.error(e)
        SLACK.dead()
        os._exit(0)

if __name__ == "__main__":
    main()
