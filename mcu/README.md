MCU:
=============
_Microcontroller unit (Flight Control MCU/ Ground Control MCU)_

##### Features
- Receives commands over serial/TTY to turn on/off relays
    - Error checking CRC-8 to handle bad commands or corrupted payloads

##### Planned
- [ ] Standalone Arduino/ATMega circuitboard with FTDI usb-uart chip
- [ ] Safe modes for resetting to default states after a timeout
- [ ] Delayed commands/task scheduler
- [ ] Store relay pin mapping and address to EEPROM
    - [ ] Commands to update mapping and address over serial
