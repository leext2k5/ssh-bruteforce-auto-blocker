import subprocess
import ipaddress
from datetime import datetime
from src.config import BLOCKED_IPS_LOG, WHITELIST_IPS

blocked_ips = set()

def is_whitelisted(ip):
	ip_addr = ipaddress.ip_address(ip)

	for item in WHITELIST_IPS:
		network = ipaddress.ip_network(item, strict=False)

		if ip_addr in network:
			return True

	return False

def log_blocked_ip(ip):
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:$S")

	with open(BLOCKED_IPS_LOG, "a") as file:
		file.write(f"[{timestamp}] Blocked IP: {ip}\n")

def block_ip(ip):
	if is_whitelisted(ip):
		printf(f"[+] Whitelisted IP, skip blocking: {ip}")
		return False

	if ip in blocked_ips:
		return False

	try:
		subprocess.run(
			["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
			check=True
		)

		blocked_ips.add(ip)
		log_blocked_ip(ip)

		return True

	except subprocess.CallProcessError as e:
		printf(f"[-] Failed to block IP {ip}: {e}")
		return False
