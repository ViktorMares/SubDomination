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

# Use Sublist3r to enumerate subdomains
sublist3r_cmd = f'sublist3r -d {domain} | sort -u'
sublist3r_output = subprocess.check_output(sublist3r_cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

# Use Subfinder to enumerate subdomains
subfinder_cmd = f'subfinder -d {domain} | sort -u'
subfinder_output = subprocess.check_output(subfinder_cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

# Use Assetfinder to enumerate subdomains
assetfinder_cmd = f'assetfinder --subs-only {domain} | sort -u'
assetfinder_output = subprocess.check_output(assetfinder_cmd, shell=True, text=True, stderr=subprocess.DEVNULL)

# Combine the results from Sublist3r, Subfinder, and Assetfinder
combined_output = f"{sublist3r_output}{subfinder_output}{assetfinder_output}"

subdomains = []
count = 0

for subd in combined_output.split('\n'):
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
