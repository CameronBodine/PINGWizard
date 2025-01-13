

import subprocess
import sys
import json

def check(name):

    latest_pip = (subprocess.run([sys.executable, '-m', 'pip', 'list', '-o', '--format=json'], capture_output=True, text=True)).stdout
    latest_pip = json.loads(latest_pip)

    ping_packages = []
    for i in latest_pip:
        if 'ping' in i['name']:
            ping_packages.append(i)

    return latest_pip