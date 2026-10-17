# go2rtc-addon

go2rtc als Home-Assistant-Add-on (aarch64) mit einem kleinen Patch: mDNS (HomeKit) antwortet und sendet nur
in den Netzen aus `/config/go2rtc-mdns.txt` (ein CIDR pro Zeile, z. B. `172.17.0.0/16`).
Ohne diese Datei verhaelt sich go2rtc wie das Original.

Ein taeglicher Workflow baut das neueste go2rtc-Release mit dem Patch und hebt die Add-on-Version an.
Schlaegt der Patch fehl, bricht der Build ab und es erscheint kein Update.
