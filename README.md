ares-controls :rocket:
=============
Control systems software for the Ares rocket

MOIST:
------
_**M**ission **O**perator **I**nterface: **S**witch **T**erminal_

##### Usage

```bash
$> make moist-client # Build source into executable (bin/moist)
$> make moist-deploy # Copy executable into /deploy/ (requires sudo)
$> make moist-service-setup # Sets up a systemd service for moist to auto-run on a pi (requires sudo)

$> systemctl status moist.service # Check if service running
$> sudo systemctl stop moist.service # Stop running service
$> sudo systemctl start moist.service # Start service
$> sudo systemctl enable moist.service # Start service every time we boot up
$> sudo systemctl disable moist.service # Disable auto-run of service on startup
```

Reading Logs:
```bash
$> sudo journalctl -u moist.service
```

Debugging/Development:
> Aside from using services, there are several ways to manually run the program. To run the deployment version, run `/deploy/moist`. Otherwise, run either `ares-controls/bin/moist` or `ares-controls/moist/__main__.py`

##### Features
- Switch board, with switches for each valve
- Ignition and ignition safety digital inputs
- MOIST Enable digital input/switch
- LED indicator for network status and arming
- Ethernet port, internal power (power bank)

##### Software Features
- Callback function to handle GPIO (switch) events
- TCP Client connecting to CDH controls server
    - Socket client running asynchronously, on a separate thread
- Systemd service to run script on startup

##### Planned
- [ ] Clean logging and debug output
- [ ] Exception handling software (restart MOIST on error)
- [ ] Built-in battery charging port
- [ ] Field debugging/visualization output
- [ ] Heartbeat between CDH and MOIST

CDH-server:
------------------
_**C**ommand and **D**ata **H**andling server_

##### Usage

```bash
$> make cdhserv # Build source into executable (bin/cdhserv)
$> make cdhserv-deploy # Copy executable into /deploy/ (requires sudo)
$> make cdhserv-service-setup # Sets up a systemd service for moist to auto-run on a pi (requires sudo)

$> systemctl status cdhserv.service # Check if service running
$> sudo systemctl stop cdhserv.service # Stop running service
$> sudo systemctl start cdhserv.service # Start service
$> sudo systemctl enable cdhserv.service # Start service every time we boot up
$> sudo systemctl disable cdhserv.service # Disable auto-run of service on startup
```

Reading Logs:
```bash
$> sudo journalctl -u cdhserv.service
```

Debugging/Development:
> Aside from using services, there are several ways to manually run the program. To run the deployment version, run `/deploy/cdhserv`. Otherwise, run either `ares-controls/bin/cdhserv` or `ares-controls/cdh-server/__main__.py`

##### Features
- TCP Server for receiving commands
    - Handles MCU and Maintenance commands (connect to serial device, list serial devices, etc)
- Serial Master functionality to translate and send commands to FCM/GCM
    - Supports multiple device connections with addressing, on 1+ serial buses
    - Connects to devices by physical port location, not dynamically assigned IDs

##### Planned
- [ ] Handle multiple concurrent connections on separate threads, test current functionality
- [ ] Exception handling software and hardware watchdog (restart CDH on error)
- [ ] Error code and TCP response standardization
- [ ] Field debugging/visualization output
- [ ] Basic maintenance commands for serial connections/listing
- [ ] Expansion of Maintenance commands (restart server, etc)
- [ ] Heartbeat between CDH and MOIST

FCM-mcu:
-----------------
_**F**light **C**ontrol **M**odule - microcontroller unit_

##### Features
- Receives commands over serial/TTY to turn on/off relays
    - Error checking CRC-8 to handle bad commands or corrupted payloads

##### Planned
- [ ] Standalone Arduino/ATMega circuitboard with FTDI usb-uart chip
- [ ] Safe modes for resetting to default states after a timeout
- [ ] Delayed commands/task scheduler
- [ ] Store relay pin mapping and address to EEPROM
    - [ ] Commands to update mapping and address over serial
