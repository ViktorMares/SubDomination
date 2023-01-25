#!/usr/bin/env python3

import subprocess
import requests
import argparse
from colorama import Fore

parser = argparse.ArgumentParser(description='A simple script to enumerate & probe subdomains')

#Add a required command-line argument. -C 'city name' to specify the city we want to scrape
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-d','--domain', help='Specify a domain that you would like to enumerate',type=str, required=True)
args = parser.parse_args()

#Store the sys argument 0 as a variable
domain = args.domain

print(f'\n[+] Enumerating subdomains of {domain}\n')
cmd = f'assetfinder {domain} | grep "{domain}" | sort | uniq '
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]

subdomains = []
count = 0

for subd in output.decode('utf-8').split('\n'):
    subdomains.append(subd)
    count+=1

print(f'[+] Found {count} subdomain(s) for {domain}')
    
print(f'''
[+] Testing the connection to each subdomain \n
[+] Listing alive subdomains only (This will take some time...)
	''')

for s in subdomains:
	try:
		response = requests.get(f'https://{s}', timeout=3)
		if response.status_code == 200:
			print(f'{Fore.GREEN}{s} [{response.status_code} {response.reason}]')
		elif str(response.status_code).startswith('40'):
			print(f'{Fore.YELLOW}{s} [{response.status_code} {response.reason}]')
		elif str(response.status_code).startswith('30'):
			print(f'{Fore.BLUE}{s} [{response.status_code} {response.reason}]')
		elif str(response.status_code).startswith('50'):
			print(f'{Fore.RED}{s} [{response.status_code} {response.reason}]')
	except:
		pass
