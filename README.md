# Sonoff Wifi Switch

The sonoff switch platform allows you to toggle Sonoff switches. Switches are modified to run ESPEasy or Tasmota firmware to provide a HTTP API. 

To enable it, add the following lines to your configuration.yaml:

# Example configuration.yaml entry for ESPEasy
```
switch:
  platform: sonoff_espeasy
  switches:
    bedroom_heating:
      host: hostname_or_ipaddr
```

# Example configuration.yaml entry for Tasmota
```
switch:
  platform: sonoff_tasmota
  switches:
    bedroom_heating:
      host: hostname_or_ipaddr
```

# Configuration variables:

* switches (Required): The array that contains all Sonoff switches.
* identifier (Required): Name of the Sonoff switch as slug. Multiple entries are possible.
* host (Required): Hostname or IP address of the switch on the local network.
* name (Optional): Friendly name of the switch.
* username (Optional): Username for basic authentication.
* password (Optional): Password for basic authentication.
