import re
from collections import defaultdict

failed_attempts = defaultdict(int)

ip_pattern = re.compile(r"Failed password.* from (\d+\.\d+\.\d+\.\d+)")

def detect_failed_login(line):
	match = ip_pattern.search(line)

	if match:
		ip = match.group(1)
		failed_attempts[ip] += 1
		return ip, failed_attempts[ip]

	return None, 0
