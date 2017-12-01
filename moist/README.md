MOIST:
=========
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
> Currently, the systemd service implementation does not support printing to the console or a log file. To run the program with console output, run either `/deploy/moist` or `ares-controls/bin/moist` or `ares-controls/moist/__main__.py`

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
