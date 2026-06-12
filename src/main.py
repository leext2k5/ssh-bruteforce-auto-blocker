import time
from src.config import AUTH_LOG_PATH, FAILED_THRESHOLD, CHECK_INTERVAL, WHITELIST_IPS
from src.detector import detect_failed_login
from src.firewall import block_ip, is_whitelisted

def monitor_log():
	print("[+] SSH Brute Force Auto Blocker started")
	print(f"[+] Monitoring: {AUTH_LOG_PATH}")
	print(f"[+] Threshold: {FAILED_THRESHOLD} failed attempts")
	print(f"[+] Whitelist: {WHITELIST_IPS}")

	with open(AUTH_LOG_PATH, "r") as file:
		file.seek(0, 2)

		while True:
			line = file.readline()

			if not line:
				time.sleep(CHECK_INTERVAL)
				continue

			ip, count = detect_failed_login(line)

			if ip:
				print(f"[!] Failed SSH login detected from {ip} | Count: {count}")

				if is_whitelisted(ip):
					print(f"[+] Whitelisted IP detected, skip, blocking: {ip}")
					continue

				if count >= FAILED_THRESHOLD:
					blocked = block_ip(ip)

					if blocked:
						print(f"[+] Blocked IP: {ip}")
					else:
						print(f"[-] IP already blocked or blocking failed: {ip}")

if __name__ == "__main__":
	monitor_log()
