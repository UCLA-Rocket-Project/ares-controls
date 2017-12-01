CDH:
=============
_**C**ommand and **D**ata **H**andling_

##### Usage

```bash
$> make cdh # Build source into executable (bin/moist)
$> make cdh-deploy # Copy executable into /deploy/ (requires sudo)
$> make cdh-service-setup # Sets up a systemd service for moist to auto-run on a pi (requires sudo)

$> systemctl status cdhserv # Check if service running
$> sudo systemctl stop cdhserv # Stop running service
$> sudo systemctl start cdhserv # Start service
$> sudo systemctl enable cdhserv # Start service every time we boot up
$> sudo systemctl disable cdhserv # Disable auto-run of service on startup
```
> Currently, the systemd service implementation does not support printing to the console or a log file. To run the program with console output, run either `/deploy/cdhserv` or `ares-controls/bin/cdhserv` or `ares-controls/cdh/__main__.py`

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
