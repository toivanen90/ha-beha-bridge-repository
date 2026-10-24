#!/usr/bin/env python3
"""Runtime patch for upstream beha_mqtt.py.
Uses each Gen1 heater's latest_reading_temperature instead of copying the
room aggregate temperature to every climate entity.
"""
from pathlib import Path

path = Path('/beha_mqtt.py')
s = path.read_text()

old_verify = '''                            "current_temperature": room.get("latest_temperature"),
                            "target_temperature": actual_temp,
'''
new_verify = '''                            "current_temperature": h.get("latest_reading_temperature") if h.get("latest_reading_temperature") is not None else room.get("latest_temperature"),
                            "target_temperature": actual_temp,
'''
if old_verify not in s:
    raise SystemExit('Expected verification temperature block not found')
s = s.replace(old_verify, new_verify, 1)

old_loop = '''                target_temp = room["target_temperature"]
                current_temp = room.get("latest_temperature")

                for h in room["heaters"]:
                    hid = h["device_unique_id"]
'''
new_loop = '''                target_temp = room["target_temperature"]
                room_temp = room.get("latest_temperature")

                for h in room["heaters"]:
                    hid = h["device_unique_id"]
                    current_temp = h.get("latest_reading_temperature")
                    if current_temp is None:
                        current_temp = room_temp
'''
if old_loop not in s:
    raise SystemExit('Expected sync temperature block not found')
s = s.replace(old_loop, new_loop, 1)

path.write_text(s)
print('Patched beha_mqtt.py: climate entities now use per-heater temperatures')
