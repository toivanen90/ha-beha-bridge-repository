#!/usr/bin/env python3
"""Safe BEHA API structure diagnostic.

Prints room/heater configuration fields without authentication tokens,
passwords, email addresses, IDs, or other identifier-like values.
Used temporarily to determine whether Gen1 heater objects expose their
own temperature measurements in users/configuration.
"""

import beha_auth

SENSITIVE_PARTS = (
    "id", "token", "email", "password", "secret", "auth", "user",
    "owner", "serial", "mac", "address", "key", "uuid"
)


def safe_key(key):
    k = str(key).lower()
    return not any(part in k for part in SENSITIVE_PARTS)


def describe(value):
    if isinstance(value, dict):
        return "<object>"
    if isinstance(value, list):
        return f"<list:{len(value)}>"
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) or value is None:
        return value
    # Avoid printing arbitrary strings from the cloud response.
    return f"<string:{len(str(value))}>"


def main():
    print("========== BEHA SAFE API DIAGNOSTIC ==========")
    config = beha_auth.api("GET", "users/configuration") or {}
    places = config.get("places", [])
    print(f"places: {len(places)}")

    for p_idx, place in enumerate(places, 1):
        rooms = place.get("rooms", [])
        print(f"place[{p_idx}] rooms: {len(rooms)}")
        for r_idx, room in enumerate(rooms, 1):
            print(f"  room[{r_idx}] fields:")
            for key, value in sorted(room.items()):
                if key == "heaters" or not safe_key(key):
                    continue
                print(f"    {key}: {describe(value)}")

            heaters = room.get("heaters", [])
            print(f"    heaters: {len(heaters)}")
            for h_idx, heater in enumerate(heaters, 1):
                print(f"      heater[{h_idx}] fields:")
                for key, value in sorted(heater.items()):
                    if not safe_key(key):
                        continue
                    print(f"        {key}: {describe(value)}")

    print("========== END BEHA SAFE API DIAGNOSTIC ==========")


if __name__ == "__main__":
    main()
