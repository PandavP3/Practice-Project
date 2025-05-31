# HTTP Packet Sniffer

This is a Python-based HTTP packet sniffer using [Scapy](https://scapy.net/). It captures HTTP requests on a specified network interface, extracts URLs being accessed, and attempts to identify potential login credentials in plain-text data.

⚠️ **This tool is intended strictly for ethical hacking, cybersecurity research, and educational purposes. Never use it on unauthorized networks.**

## Features

- Sniffs HTTP requests in real-time
- Extracts and displays accessed URLs
- Detects and prints possible login information (e.g., usernames, passwords)
- Simple, modular design using Scapy

## Requirements

- Python 3.x
- Scapy
- Run with root privileges

Install dependencies with:

```bash
pip install scapy
