import subprocess
import time

# Install required libraries
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

from resource_monitoring import SLACK

restart_cnt = 0

while True:   
    # Start your Python script as a subprocess
    process = subprocess.Popen(['pythonw', 'resource_monitoring.py'])
    
    while True:
        # Wait for the subprocess to complete or crash
        return_code = process
        
        # Check if the stderr output contains any errors or exceptions
        errors = process.poll()

        if errors is not None:
            time.sleep(60)
            break
        else:
            pass

    if restart_cnt > 10:
        SLACK.dead("final")
        break
    
    restart_cnt += 1