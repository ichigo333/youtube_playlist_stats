import re
from datetime import timedelta

def parse_duration(duration_str):
    match = re.match(r'(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        raise ValueError("Invalid duration format")
    
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
