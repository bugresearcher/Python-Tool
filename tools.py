#!/usr/bin/env python
from urllib2 import *
from platform import system
import sys
def clear():
    if system() == 'Linux':
        os.system("clear")
    if system() == 'Windows':
        os.system('cls')
        os.system('color a')
    else:
        pass
def slowprint(s):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(4. / 100)
banner = '''
\033[91m
         ____     __   ______       _____ 
        / ___| _ _\ \ / /  _ \  ___|  ___|
        \___ \| '_ \ V /| | | |/ _ \ |_   
\033[92m \033[96m         ___) | |_) | | | |_| |  __/  _|  
        |____/| .__/|_| |____/ \___|_|    
              |_|                                        
                   \033[96m                                                                                        
==[[ .:: TerroristCrew Def. Tool ::.]]==\033[91m
==[[ .::  Coded By: TerroristCrew  ::.]]==\033[92m
'''
print banner
def menu():
   print'''
\033[91m 1 \033[92m)\033[96m -DNS Bak
 
\033[91m 2 \033[92m)\033[96m --Whois Bak
 
\033[91m 3 \033[92m)\033[96m -Revrse IP Bak
 
\033[91m 4 \033[92m)\033[96m --GeoIP Bak
 
\033[91m 5 \033[92m)\033[96m -subnet Bak
 
\033[91m 6 \033[92m)\033[96m --Port Tarayici
 
\033[91m 7 \033[92m)\033[96m -Extract Links 
 
\033[91m 8 \033[92m)\033[96m --Zone Transfer
 
\033[91m 9 \033[92m)\033[96m -HTTP Header
 
\033[91m 10\033[92m)\033[96m --Host Ip Bulucu
 
\033[91m 11\033[92m)\033[96m -Hakkinda
 
\033[91m 0 \033[92m)\033[96m Cikis
'''
slowprint("\033[1;91mh4ck1n9 n0t 4 cr1m3. " + "\n #TerroristCrew;")
 
menu()
def ext():
    ex = raw_input ('\033[92mDevam/Cikis -=[D/C]=- -> ')
    if ex[0].upper() == 'C' :
           print 'Cikildi!!!'
           exit()
    else:
           clear()
           print banner
           menu()
           select()
 
def  select():
  try:
    joker = input("\033[96mModul Sec \033[92m0/\033[91m11 -> ->  ")
    if joker == 2:
      dz = raw_input('\033[91mHedef IP Address : \033[91m')
      whois = "http://api.hackertarget.com/whois/?q=" + dz
      dev = urlopen(whois).read()
      print (dev)
      ext()
    elif joker == 3:
      dz = raw_input('\033[92mHedef IP Address : \033[92m')
      revrse = "http://api.hackertarget.com/reverseiplookup/?q=" + dz
      lookup = urlopen(revrse).read()
      print (lookup)
      ext()
    elif joker == 1:
      dz = raw_input('\033[96mHedef Domain :\033[96m')
      dns = "http://api.hackertarget.com/dnslookup/?q=" + dz
      joker = urlopen(dns).read()
      print (joker)
      ext()
    elif joker == 4:
      dz = raw_input('\033[91mHedef IP Address : \033[91m')
      geo = "http://api.hackertarget.com/geoip/?q=" + dz
      ip = urlopen(geo).read()
      print (ip)
      ext()
    elif joker == 5:
      dz = raw_input('\033[92mHedef IP Address : \033[92m')
      sub = "http://api.hackertarget.com/subnetcalc/?q=" + dz
      net = urlopen(sub).read()
      print (net)
      ext()
    elif joker == 6:
      dz = raw_input('\033[96mHedef IP Address : \033[96m')
      port = "http://api.hackertarget.com/nmap/?q=" + dz
      scan = urlopen(port).read()
      print (scan)
      ext()
    elif joker == 7:
      dz = raw_input('\033[91mEntre Your Domain :\033[91m')
      get = "https://api.hackertarget.com/pagelinks/?q=" + dz
      page = urlopen(get).read()
      print(page)
      ext()
    elif joker == 8:
      dz = raw_input('\033[92mHedef Domain :\033[92m')
      zon = "http://api.hackertarget.com/zonetransfer/?q=" + dz
      tran = urlopen(zon).read()
      print (tran)
      ext()
    elif joker == 9:
      dz = raw_input('\033[96mHedef Domain :\033[96m')
      hea = "http://api.hackertarget.com/httpheaders/?q=" + dz
      der =  urlopen(hea).read()
      print (der)
      ext()
    elif joker == 10:
      dz = raw_input('\033[91mHedef Domain :\033[91m')
      host = "http://api.hackertarget.com/hostsearch/?q=" + dz
      finder = urlopen(host).read()
      print (finder)
      ext()
    elif joker == 11:
      slowprint("TerroristCrew Tool. \033[92m")
      slowprint(".....................")
      slowprint("Coded: TerroristCrew \033[96m")
      slowprint(".........................")
      slowprint("Blog : terroristcrew.com \033[91m")
      slowprint("............................")
      slowprint("Zone-H : http://www.zone-h.org/archive/notifier=Terrorist-Crew?zh=1  \033[92m")
      slowprint(".........................................")
      slowprint("Golgeler : http://golgeler.net/shadow!Terrorist-Crew!1 \033[96m")
      slowprint("........................................................")
      ext() 
    elif joker == 0:
      print "94M3 0V3R!"
      ext()
  except(KeyboardInterrupt):
    print "\nCtrl + C -> Bye Bye"
select()