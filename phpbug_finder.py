#!/usr/bin/python  
# -*- coding: utf-8 -*-

# Finding Bug on PHP Scripts

import os
from os import name
import subprocess

print """
#######################################
#                                     #
#        Simple PhpBug Finder         #  
#         Coded by CodeNinja          # 
#      http://illegalsecurity.com     #
#                                     #
#######################################
"""

if name != "posix":
	print "Bu program sadece Linux isletim sisteminde calismaktadir"
else:
	print "Merhaba Linux Kullanicisi, bu program senin icin! :)\n"

dizin = raw_input("""Taranacak dizin yolunu giriniz:
""")

def xss():
	print "\n\nPotansiyel XSS zafiyeti arastiriliyor...\n"
	print "----------------------------------------\nXSS Test 1:\n"
	subprocess.call("grep -i -n -r '\$_GET' %s"%(dizin), shell=True)
	print "----------------------------------------\nXSS Test 2:\n"
	subprocess.call("grep -i -n -r '\$_' %s | grep 'echo'"%(dizin), shell=True)
	print "----------------------------------------\nXSS Test 3:\n"
	subprocess.call("grep -i -n -r '\$_GET' %s | grep 'echo'"%(dizin), shell=True)
	print "----------------------------------------\nXSS Test 4:\n"
	subprocess.call("grep -i -n -r '\$_POST' %s | grep 'echo'"%(dizin), shell=True)
	print "----------------------------------------\nXSS Test 5:\n"
	subprocess.call("grep -i -n -r '\$_REQUEST' %s | grep 'echo'"%(dizin), shell=True)

def sqli():
	print "\n\nPotansiyel SQL Injection zafiyeti arastiriliyor...\n"
	print "----------------------------------------\nSQLi Test 1:\n"
	subprocess.call("grep -i -n -r '\$sql' %s"%(dizin), shell=True)
	print "----------------------------------------\nSQLi Test 2:\n"
	subprocess.call("grep -i -n -r '\$sql' %s | grep '\$_'"%(dizin), shell=True)

def cmdexec():
	print "\n\nPotansiyel Command Execution zafiyeti arastiriliyor...\n"
	print "----------------------------------------\nCommand Execution Test 1:\n"
	subprocess.call("grep -i -n -r 'shell_exec(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCommand Execution Test 2:\n"
	subprocess.call("grep -i -n -r 'system(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCommand Execution Test 3:\n"
	subprocess.call("grep -i -n -r 'exec(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCommand Execution Test 4:\n"
	subprocess.call("grep -i -n -r 'passthru(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCommand Execution Test 5:\n"
	subprocess.call("grep -i -n -r 'proc_open(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCommand Execution Test 6:\n"
	subprocess.call("grep -i -n -r 'pcntl_exec(' %s"%(dizin), shell=True)

def codexec():
	print "\n\nPotansiyel Code Execution zafiyeti arastiriliyor...\n"
	print "----------------------------------------\nCode Execution Test 1:\n"
	subprocess.call("grep -i -n -r 'eval(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCode Execution Test 2:\n"
	subprocess.call("grep -i -n -r 'assert(' %s"%(dizin), shell=True)
	print "----------------------------------------\nCode Execution Test 3:\n"
	subprocess.call("grep -i -n -r 'preg_replace' %s | grep '/e'"%(dizin), shell=True)
	print "----------------------------------------\nCode Execution Test 4:\n"
	subprocess.call("grep -i -n -r 'create_function(' %s"%(dizin), shell=True)

def infodisclosure():
	print "\n\nPotansiyel Information Disclosure zafiyeti arastiriliyor...\n"
	print "----------------------------------------\nInfo Disclosure Test 1:\n"
	subprocess.call("grep -i -n -r 'phpinfo' %s"%(dizin), shell=True)

def fileinclusion():
	print "\n\nPotansiyel File Inclusion zafiyeti arastiriliyor...\n"
	print "----------------------------------------\nFile Inclusion Test 1:\n"
	subprocess.call("grep -i -n -r 'file_include' %s"%(dizin), shell=True)
	print "----------------------------------------\nFile Inclusion Test 2:\n"
	subprocess.call("grep -i -n -r 'include(' %s"%(dizin), shell=True)
	print "----------------------------------------\nFile Inclusion Test 3:\n"
	subprocess.call("grep -i -n -r 'require(' %s"%(dizin), shell=True)
	print "----------------------------------------\nFile Inclusion Test 4:\n"
	subprocess.call("grep -i -n -r 'require(\$file)' %s"%(dizin), shell=True)
	print "----------------------------------------\nFile Inclusion Test 5:\n"
	subprocess.call("grep -i -n -r 'include_once(' %s"%(dizin), shell=True)
	print "----------------------------------------\nFile Inclusion Test 6:\n"
	subprocess.call("grep -i -n -r 'require_once(' %s"%(dizin), shell=True)
	print "----------------------------------------\nFile Inclusion Test 7:\n"
	subprocess.call("grep -i -n -r 'require_once(' %s | grep '\$_'"%(dizin), shell=True)

#def header():
#	print "\n\nHeader bolgesinde potansiyel zafiyetler arastiriliyor...\n"
#	print "----------------------------------------\nHeader Test 1:\n"
#	subprocess.call("grep -i -n -r 'header(' %s | grep '\$_'"%(dizin), shell=True)

xss()
sqli()
cmdexec()
codexec()
infodisclosure()
fileinclusion()
#header()