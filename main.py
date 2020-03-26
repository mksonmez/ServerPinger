#!/usr/bin/env python3
import subprocess
import csv

def ping(target_ip):
    p = subprocess.Popen('ping ' + target_ip, 
			stdout = subprocess.PIPE, 
			stderr = subprocess.PIPE)

    onGoing = 'server-online'

# check console output        
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
        if (output.endswith('unreachable.')):
            onGoing = 'server-unreacheable'
            break
        elif (output.startswith('Ping request could not find host')):
            onGoing = 'server-host-not-found'
            break
        if (output.startswith('Request timed out.')):
            onGoing = 'server-offline'
            break
        else:
            print(target_ip)
    
    return onGoing

# write to file on or off
def on_or_off(target_ip):
    statusOfPing = ping(target_ip)
    if (statusOfPing == 'server-host-not-found'):
        writeToFile('server-not-found.csv', target_ip)
    elif (statusOfPing == 'server-unreacheable'):
       writeToFile('server-unreachable.csv', target_ip)
    elif (statusOfPing == 'server-offline'):
       writeToFile('server-offline.csv', target_ip)
    elif (statusOfPing == 'server-online'):
        writeToFile('server-online.csv', target_ip)
    else:
        print("error on on_or_off")

def writeToFile(filename, data):
    # any existing files with the same name will be erased
    with open(filename, 'w') as output: 
        output.write('header' + '\n' + data + '\n')
'''
1- output on same file
2- use distinctive header
3- let user input of IP list
'''

# source if IPs/server
file = open('list_of_ips.txt')

try:
    reader = csv.reader(file)
    
    for item in reader:
        on_or_off(item[0].strip())
finally:
    file.close()
