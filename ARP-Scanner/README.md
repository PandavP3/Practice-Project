# ARP Spoofing Tool

This is a Python-based ARP spoofing tool built using the [Scapy](https://scapy.net/) library. It performs a Man-in-the-Middle (MITM) attack by sending forged ARP replies to a target machine and its gateway, redirecting network traffic through the attacker's machine.

⚠️ **This tool is for educational and ethical penetration testing purposes only. Do not use it on networks you do not own or have permission to test.**

## Features

- Spoofs ARP tables of a target and a gateway
- Continuously sends spoofed ARP replies to maintain MITM position
- Automatically restores the ARP tables upon exit (Ctrl+C)
- Uses Scapy for low-level packet crafting

## Requirements

- Python 3.x
- [Scapy](https://scapy.net/)

Install Scapy via pip if you haven't already:

```bash
pip install scapy
