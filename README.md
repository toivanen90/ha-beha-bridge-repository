# BEHA SmartHeater Home Assistant Add-on Repository

Home Assistant add-on repository packaging the BEHA SmartHeater MQTT bridge by maxd2s.

Upstream project: https://github.com/maxd2s/ha-beha-bridge

The add-on downloads the upstream bridge sources from a pinned upstream commit during the Home Assistant build. BEHA credentials are entered only in the Home Assistant add-on configuration and are not stored in this repository.

> This is an unofficial add-on and is not affiliated with BEHA. It logs in to the BEHA cloud with your BEHA account, so it needs internet access and may stop working if BEHA changes its service.

## What you get

Each heater in your BEHA account appears in Home Assistant as a climate entity through MQTT discovery, with:

- on/off
- target temperature
- the heater's own measured temperature (falls back to the room temperature if the heater does not report one)

The bridge syncs with the BEHA cloud every 60 seconds. Changes made in the BEHA app, in Home Assistant or through the API are picked up. A change made on the heater's physical dial is not reported to Home Assistant.

## Requirements

- Home Assistant OS or Supervised (the add-on store is needed).
- The **Mosquitto broker** app installed and running, and the **MQTT** integration set up (Settings → Devices & services). The add-on finds the broker by itself; you do not enter any MQTT settings.
- A BEHA account with your heaters already added in the BEHA app.
- A supported architecture: `aarch64`, `amd64` or `armv7`.

## Installation

1. In Home Assistant, go to **Settings → Apps → App store**.
2. Open the **⋮** menu (top right) → **Repositories**.
3. Paste `https://github.com/toivanen90/ha-beha-bridge-repository`, click **Add**, then **Close**. Refresh the page if the new apps do not appear.
4. Open **BEHA SmartHeater Bridge** and click **Install**. The first build takes a minute or two on a Raspberry Pi.
5. On the **Configuration** tab, enter `beha_email` and `beha_password` (the same login as in the BEHA app) and click **Save**.
6. On the **Info** tab, turn on **Start on boot** and **Watchdog**, then click **Start**.

## Check that it works

Open the **Log** tab. A healthy start looks like this, with one "New heater discovered" line per heater:

```
INFO: ========== BEHA Bridge Starting ==========
INFO: MQTT: Using HA service discovery credentials
INFO: No tokens found. Attempting login...
Logged in! Token expires in 3600s
Connected to MQTT Broker!
Publishing Home Assistant Auto-Discovery config...
New heater discovered: <heater name> (<heater id>)
Sync complete (1 heaters)
```

The heaters then show up under **Settings → Devices & services → MQTT → Devices**.

## Configuration

| Option | Description |
|---|---|
| `beha_email` | Email address of your BEHA account |
| `beha_password` | Password of your BEHA account |

## Troubleshooting

- **The app does not appear in the store:** make sure the repository was added in step 3 and refresh the page.
- **Login fails:** check that the email and password work in the BEHA app, then restart the add-on.
- **No heaters appear:** check the log for MQTT errors, and confirm the Mosquitto broker is running and the MQTT integration is set up.
- **A heater shows as unavailable:** it is probably offline; check it in the BEHA app.
- **Temperatures do not update:** the bridge syncs once a minute. Look in the log for API errors.
