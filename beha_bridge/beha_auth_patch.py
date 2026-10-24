#!/usr/bin/env python3
"""Runtime patch for upstream beha_auth.py.
Preserves per-heater Gen1 temperature readings exposed by BEHA Cloud.
"""
from pathlib import Path

path = Path('/beha_auth.py')
s = path.read_text()
old = '''                        "name": heater["name"],
                        "is_offline": heater.get("is_offline", False),
                        "is_enabled": heater.get("is_enabled", True)
'''
new = '''                        "name": heater["name"],
                        "is_offline": heater.get("is_offline", False),
                        "is_enabled": heater.get("is_enabled", True),
                        "latest_reading_temperature": heater.get("latest_reading_temperature"),
                        "latest_reading_timestamp": heater.get("latest_reading_timestamp")
'''
if old not in s:
    raise SystemExit('Expected beha_auth.py block not found; upstream source may have changed')
path.write_text(s.replace(old, new, 1))
print('Patched beha_auth.py: preserving per-heater temperature readings')
