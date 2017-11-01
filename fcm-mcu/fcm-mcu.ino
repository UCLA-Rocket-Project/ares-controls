#define ADDRESS 0xc0
#define BBSIZE 2
#define MAXDATA 10

#define numOpCodes 15 //13 + continue and stop codes

#define Relay0 12
#define Relay1 11
#define Relay2 10
#define Relay3 9
#define Relay4 8
#define Relay5 7
#define Relay6 6
#define Relay7 5

int relays[] = {Relay0, Relay1, Relay2, Relay3, Relay4, Relay5, Relay6, Relay7};

constexpr byte opCodeList[] = {0x00,0x01,0x02,0x03,0x04,0x05,0x06,0xff,0xff,0xff,0xff,0xff,0xff,0x3e,0x3f}; /*all the op codes including continue and stop as the last two*/ // still need to set op codes
constexpr int opCodeLengths[] = {1,1,1,1,1,1,8,4,1,1,1,8,1,-1,-1}; /*corresponding expected data lengths for each op code (ORDER MATTERS)*/

byte byte_buffer[BBSIZE];
byte storedData[MAXDATA];
int currentDataIdx;
int expectedDataLength;
byte currentCRC;

void processBytes();
bool setRelay(int, int);
byte getRelay(int);

void setup() {
   Serial.begin(9600);

  for (int i = 0; i < 8; i++) {
    digitalWrite(relays[i], HIGH);
    pinMode(relays[i], OUTPUT);
  }

  currentDataIdx = 0;
}

byte incoming_byte;
byte nextOpCode;

void loop () {
  if (Serial.available()) {
    Serial.readBytes(byte_buffer, 2);
    if (byte_buffer[0] & 0xc0 == ADDRESS) {
      nextOpCode = byte_buffer[0] & 0x3f;
      int opCodeResult = processOpCode(nextOpCode);
      if (opCodeResult == 0) {
        /*New Op Code -> RESET*/
        currentDataIdx = 0;
        for (int i = 0; i < MAXDATA; i++) {
          storedData[i] = 0;
        }
        storedData[currentDataIdx] = byte_buffer[0];
        currentDataIdx++;
        storedData[currentDataIdx] = byte_buffer[1];
        currentDataIdx++;
      }
      else if (opCodeResult == 1) {
        /*Continue Code*/
        storedData[currentDataIdx] = byte_buffer[1];
        currentDataIdx++;
      }
      else if (opCodeResult == 2) {
        /*Stop Code*/
        currentCRC = byte_buffer[1];
        byte assembledCommand[currentDataIdx];
        for (int i = 0; i < currentDataIdx; i++) {
          assembledCommand[i] = storedData[i];
        }
        if (CRC8(assembledCommand, currentDataIdx) == currentCRC && currentDataIdx == expectedDataLength) {
          processCommand(assembledCommand);
        }
      }
      else if (opCodeResult == 3) {
        /*Invalid code -> RESET*/
        currentDataIdx = 0;
        for (int i = 0; i < MAXDATA; i++) {
          storedData[i] = 0;
        }
      }
    }
  }
}

/*
void processBytes(byte b_buffer[2]) {
    Serial.write(0xc4);
    byte opcode = b_buffer[0];

     if (CRC8(b_buffer) == crcByte) {
      
    } else if (b_buffer[2] != STOPCODE) {
      Serial.write(0xe0);
      Serial.write(0xe0);
    } else if (opcode == OPCODE_ON || opcode == OPCODE_OFF) {
      setRelay(b_buffer[1], opcode == OPCODE_OFF);
      Serial.write(opcode);
      Serial.write(getRelay(b_buffer[1]));
    } else if (opcode == OPCODE_GET) {
      Serial.write(opcode);
      Serial.write(getRelay(b_buffer[1]));
    } else {
      Serial.write(0xec);
      Serial.write(0xec);
    }

    Serial.write(0xff);
}
*/

byte getRelay(int relay)
{
  if(relay < 0 || relay > 7) return 0xe1;
  return digitalRead(relays[relay]);
}

bool setRelay(int relay, int mode) {
  if(relay < 0 || relay > 7)return false;
  digitalWrite(relays[relay], mode);
  return true;
}

unsigned int CRC8 (byte input[], int arrSize) {
unsigned int crc8 = 0x00;
int pos = 0;
int i = 0;

  for (pos = 0; pos < arrSize; pos++) {
    crc8 ^= input[pos];          // XOR byte into crc

    for (i = 8; i != 0; i--) {    // Loop over each bit
      if ((crc8 & 0x01) != 0) {      // If the LSB is set
        crc8 >>= 1;                    // Shift right and XOR 0x8c
        crc8 ^= 0x8c;
      }
      else                            // Else LSB is not set
        crc8 >>= 1;                    // Just shift right
    }
  }
  return crc8;
}

int processOpCode (byte opCode) {
  /*set expectedDataLength based on opCode*/
  /*return: 0 for new start code
   *        1 for continue code
   *        2 for stop code
   *        3 for invalid code
   */
   int idxAtOpCode  = -1;
   bool validOpCode = false;
   for (int i = 0; i < numOpCodes; i++) {
     if (opCode == opCodeList[i]) {
       validOpCode = true;
       idxAtOpCode = i;
     }
   }
   if (idxAtOpCode > -1 && idxAtOpCode < 14) {
    expectedDataLength = opCodeLengths[idxAtOpCode];
   }
   else  if (idxAtOpCode = -1) {
    expectedDataLength == -1;
   }
   
   if (validOpCode) {
    if (opCode == opCodeList[13] && currentDataIdx > 0) {
      return 1;
    }
    else if (opCode == opCodeList[14] && currentDataIdx > 0) {
      return 2;
    }
    else {
      return 0;
    }
   }
   else {
    return 3;
   }
}

// https://docs.google.com/spreadsheets/d/1r0zNM0y-FEgeVTTzpJzNjrXxf3hs2GVzCn1geaSeYOE/edit#gid=1305699077 check for intended responses to op codes
void processCommand (byte currentCommand[]) {
  byte opCode = currentCommand[0] & 0x3f;
  
  switch (opCode) {
    case opCodeList[0]:
    setRelay(currentCommand[1], 1);
    break;
    case opCodeList[1]:
    setRelay(currentCommand[1], 0);
    break;
    case opCodeList[2]:
    //Serial.write(getRelay(currentCommand[1])); // not too sure about how to respond, should implement similar comm system for response
    break;
    case opCodeList[3]:
    int relayStates[8];
    for (int i = 0; i < 8; i++) {
     relayStates[i] = getRelay(i);
    }
    // send back relay states
    break;
    case opCodeList[4]:
    for (int i = 0; i < 8; i++) {
     setRelay(relays[i], 1);
    }
    break;
    case opCodeList[5]:
    for (int i = 0; i < 8; i++) {
     setRelay(relays[i], 0);
    }
    break;
    case opCodeList[6]:
    for (int i = 0; i < 8; i++) {
     setRelay(relays[i], currentCommand[i]);
    }
    break;
    case opCodeList[7]:
    // set delay, amount based on currentCommand[3 and 4], but how?
    // setRelay(currentCommand[1], currentCommand[2]);
    break;
    /*
    case opCodeList[8]:
    // do something
    break;
    case opCodeList[9]:
    // do something
    break;
    case opCodeList[10]:
    // do something
    break;
    case opCodeList[11]:
    // do something
    break;
    case opCodeList[12]:
    // do something
    break;
    */
  }
}

void sendOverSerial (byte dataToSend[], int numBytes) {
  // comm protocol for sending data over serial (address + opCode = byte 1, data = byte 2)
  byte destinationAddress = dataToSend[0] & 0xc0;
  byte opCodeToSend = dataToSend[0] & 0x3f;
  Serial.write(dataToSend[0]);
  Serial.write(dataToSend[1]);
  for (int i = 2; i < numBytes; i++) {
    Serial.write (opCodeList[13]);
    Serial.write (dataToSend[i]);
  }
  Serial.write (opCodeList[14]);
  Serial.write (CRC8(dataToSend, numBytes));
}

