#!/usr/bin/env python

import subprocess
import optparse
import re

def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC address")
    parser.add_option("-m","--mac",dest="new_mac",help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help foe more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help foe more info.")
    return options

def change_mac(interface,new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])  # fixed "either" -> "ether"
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface]).decode("utf-8")
    """We can use regax rules to filter out output using pythex.org,
    we can use this in any language difference is only of syntax"""
    mac_address_search_result = re.search(r"(\w\w:){5}\w\w", str(ifconfig_result))
    #here '\w\w:\w\w:\w\w:\w\w:\w\w:\w\w' is a regax text for our mac address
    if mac_address_search_result:
        return mac_address_search_result.group(0) # group(0) bcoz we wat first occurance which will be out mac address
    else:
        print("[-] Could not read MAC address")

options = get_argument()
current_mac = get_current_mac(options.interface)
print("Current MAC = "+ str(current_mac))

change_mac(options.interface,options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC did not get changed.")