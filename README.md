# ares-control
Control systems for the Ares rocket

### MCU Command Requests

This is gonna change, we're using CRC's now

Command requests are sent over Serial in 4-byte packets

| Byte 1             |   Byte 2       |   Byte 3     |   Byte 4  |
|--------------------|----------------|--------------|-----------|
|   Target Address   | Operation Code | Data/Payload | Stop Byte |
|   `0x01`           |  `0xC1`        | `0x00`       |  `0xFF`   |

#### Target Address

| Value | Target   |
|-------|----------|
| `0xA1` | FCM |
| `0xA2` | GCM |
| `0xAC` | CDH |

#### Operation Code

| Value | Command   |
|-------|----------|
| `0xC0` | Turn off relay  |
| `0xC1` | Turn on relay   |
| `0xC3` | Get relay state |

#### Data byte
1-byte representation of the Relay ID

#### Stop byte
All data transmissions end with the stop byte, `0xFF`

### MCU Response

Possible responses:

| Byte 1             |   Byte 2       |   Byte 3     |   Byte 4  |
|--------------------|----------------|--------------|-----------|
|   Target Address   | Operation Code | Data/Payload | Stop Byte |
|   Target Address   | Operation Code | Error Code   | Stop Byte |
|   Target Address   | Error Code     | Error Code   | Stop Byte |

#### Return values
Successful operations return a 4-byte packet, with the same opcode that was received
in addition to the relay's current state (0 or 1)

#### Errors
If an error occurs, an error code is returned in Byte 3. Additionally, if the opcode is invalid then the same error code is also returned in byte 2.

| Value | Command   |
|-------|----------|
| `0xE0` | Unknown error/incorrectly formatted request  |
| `0xEC` | Invalid opcode   |
| `0xE1` | Invalid parameter/data byte |
