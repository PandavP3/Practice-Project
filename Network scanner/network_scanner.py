#!/usr/bin/env python
import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range to scan")
    options, arguments = parser.parse_args()
    return options



def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_broadcast, timeout =1, verbose=False )[0]
    #scapy.srp is going to return two sets of packets, answered and unanswered

    
    
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        #psrc prints Ip ADDress and hwsrc prints MAC Address

        client_list.append(client_dict)
    return client_list

def print_result(results_list):
    print("IP\t\t\tMac Address\n------------------------------------")
    #\t\t\t is used to add tab space
    #\n is end line character
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_results = scan(options.target)
print_result(scan_results)