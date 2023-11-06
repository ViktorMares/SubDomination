#!/usr/bin/env python3

import subprocess
import requests
import argparse
from colorama import Fore
import threading

parser = argparse.ArgumentParser(description='A simple script to enumerate & probe subdomains')

requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-d', '--domain', help='Specify a domain that you would like to enumerate', type=str, required=True)
args = parser.parse_args()

domain = args.domain

print(f'\n[+] Enumerating subdomains of {domain}\n')
cmd = f'assetfinder {domain} | grep "{domain}" | sort | uniq '
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = ps.communicate()[0]

subdomains = []
count = 0

for subd in output.decode('utf-8').split('\n'):
    subdomains.append(subd)
    count += 1

print(f'[+] Found {count} subdomain(s) for {domain}')

print(f'''
[+] Testing the connection to each subdomain 
[+] Listing alive subdomains only (This will take some time...)
''')

def test_subdomain(subdomain):
    try:
        response = requests.get(f'https://{subdomain}', timeout=3)
        if response.status_code == 200:
            print(f'{Fore.GREEN}{subdomain} [{response.status_code} {response.reason}]')
        elif str(response.status_code).startswith('40'):
            print(f'{Fore.YELLOW}{subdomain} [{response.status_code} {response.reason}]')
        elif str(response.status_code).startswith('30'):
            print(f'{Fore.BLUE}{subdomain} [{response.status_code} {response.reason}]')
        elif str(response.status_code).startswith('50'):
            print(f'{Fore.RED}{subdomain} [{response.status_code} {response.reason}]')
    except:
        pass

# Use multithreading to test subdomains concurrently
threads = []
for subdomain in subdomains:
    t = threading.Thread(target=test_subdomain, args=(subdomain,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print('\n[+] All subdomains tested')
