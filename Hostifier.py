#!/usr/bin/env python

# The MIT License (MIT)

# Copyright (c) 2014 Muhammad Adeel

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Coloring:
	def __init__(self):
		self.green = "\033[92m"
		self.bold = "\033[1m"
		self.red = "\033[91m"
		self.die = "\033[0m"

COLOR = Coloring()

try:
	import os, sys, string, socket, time
except IOError:
	print COLOR.bold + "[!] Error:" + COLOR.die + " Can't Import Modules Properly."
	exit()

def banner():
	print COLOR.bold + COLOR.red + '''
    __  __           __  _ _____          
   / / / /___  _____/ /_(_) __(_)__  _____
  / /_/ / __ \/ ___/ __/ / /_/ / _ \/ ___/
 / __  / /_/ (__  ) /_/ / __/ /  __/ /    
/_/ /_/\____/____/\__/_/_/ /_/\___/_/     
==========================================
# Author: Muhammad Adeel                 #
# Blog: http://urdusecurity.blogspot.com #
# Mail: Chaudhary1337@gmail.com          #
# Thanks to: Tyler Borland               #
==========================================''' + COLOR.die
banner()

#Dname = raw_input('\n(Domain Name)> ')
subdomains = raw_input('\n(SubDomains Filename)> ')
global varFile
global var
global varLength
varFile = open(subdomains, 'r')
var = open(subdomains, 'r')
varLength = var.readlines()

def ExecuteFunc():
	get_input = raw_input('\n1. Single URL Scan\n2. Mutiple URLs to Scan\nSelect: ')
	if get_input == '1':
		Dname = raw_input('Enter Domain: ')
		if Dname.startswith('http'):
			exit("[-] Provide Domain Like This: host.com")
		else:
			print COLOR.bold + "\n[+] Starting at: {0}".format(time.ctime()) + COLOR.die + "\n"
			Hostifier(Dname, varFile, varLength)
			print COLOR.bold + "\n[+] Ending at: {0}".format(time.ctime()) + COLOR.die
			raw_input('\nHit ENTER to Exit.')
	elif get_input == '2':
		lst = raw_input('Name of URLs List: ')
		varLst = open(lst).readlines()
		print COLOR.bold + "\n[+] Starting at: {0}".format(time.ctime()) + COLOR.die + "\n"
		for line in varLst:
			varFile2 = open(subdomains, 'r')
			var = open(subdomains, 'r')
			varLength2 = var.readlines()
			Xname = line.strip()
			Dname = Xname
			print COLOR.bold + COLOR.green + "\n[+] Now Trying: " + COLOR.die + COLOR.bold + COLOR.red + "{0}".format(Dname) + COLOR.die
			Hostifier(Dname, varFile2, varLength2)
		print COLOR.bold + "\n[+] Ending at: {0}".format(time.ctime()) + COLOR.die
		raw_input('\nHit ENTER to Exit')
	else:
		exit("[-] Invalid Choice")
	return 0

def Hostifier(Dname, varFile, varLength):
	global a
	global b
	a = 0
	b = 0
	print COLOR.bold + COLOR.green + "[+] Subdomains Loaded: {0}".format(str(len(varLength))) + COLOR.die 
	print COLOR.bold + "\n -- Thanks For Using Hostifier -- " + COLOR.die
	for sd in varFile.read().split('\n'):
		a = a + 1
		varX = chr(27)
		# credits to neuro
		sys.stdout.write(varX + '[2K' + varX + '[G')
		sys.stdout.write('[+] Trying | ' + sd + ' |' + ' --')
		sys.stdout.flush()
		try:
			sock = socket.gethostbyname_ex(sd+"."+Dname)
			print sock
			b = b + 1
		except:
			pass
	sys.stdout.write(varX + '[2K' + varX + '[G')
	print COLOR.green + COLOR.bold + "\n[+] Total Results: {0}".format(b) + COLOR.die

ExecuteFunc()
		
def main():
	if __name__ == '__main__':
		main()
