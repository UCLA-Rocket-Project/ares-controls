/*//////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//    TO DO:
//        Basic Function: DONE
//        Delayed Commands: DONE
//        Memory Writing: Done but needs testing
//                        Need to write addr, isFCMorGCM, and relays to memory on each actual arduino
//                        BE CAREFUL, LIMITED WRITES (DO NOT PUT IN INDEFINITE LOOP!!!!!!!)
//        Safe Mode: Not yet implemented
//
//    https://docs.google.com/spreadsheets/d/1r0zNM0y-FEgeVTTzpJzNjrXxf3hs2GVzCn1geaSeYOE/edit#gid=1305699077 check for intended responses to op codes
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////*/

#include <EEPROM.h>

#define isFCMorGCM 0x00  /* will be written to permanent memory and removed */

#define ADDRESS 0x40  /* will be written to permanent memory and removed */
#define piAddress 0xc0
#define BBSIZE 2
#define MAXDATA 12
#define maxQueued 10

#define opCodeMask 0x3f
#define addressMask 0xc0

#define delayQueueFullError 0xfc
#define opCodeError 0xfd
#define dataLengthError 0xfe
#define crcError 0xff

#define numOpCodes 19 //16 + continue and stop codes

/* will be written to permanent memory and removed */
#define Relay0 2
#define Relay1 3
#define Relay2 4
#define Relay3 5
#define Relay4 6
#define Relay5 7
#define Relay6 8
#define Relay7 9

int relays[] = {Relay0, Relay1, Relay2, Relay3, Relay4, Relay5, Relay6, Relay7};  /* will be written to permanent memory and removed */

constexpr byte opCodeList[] = {0x10,0x11,0x012,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f,0x20,0x3e,0x3f}; /*all the op codes including continue and stop as the last two*/
constexpr int opCodeLengths[] = {2,2,2,2,2,2,9,5,5,5,5,12,9,2,2,2,2,-1,-1}; /*corresponding expected data lengths for each op code (ORDER MATTERS)*/

/* Initialization for Data Collection Vars */
byte byte_buffer[BBSIZE];
byte storedData[MAXDATA];
int currentDataIdx;
int expectedDataLength;

/* For delayed commands */
byte commandCodeQueue[maxQueued];
byte commandDataQueue[maxQueued];
long commandTimeToExecute[maxQueued];

/* declaring methods */
void setRelay(int, int);
byte getRelay(int);

/*  init function
        - delay structures
        - serial
        - relays/pins
        - dataIdx
*/
void setup() {
  /*EEPROM.write (0, isFCMorGCM);
  //EEPROM.write (1, ADDRESS);
  //for (int i = 0; i < 8; i++) {
  //  EEPROM.write(i+2, relays[i]);
  }*/
  
  for (int i = 0; i < maxQueued; i++) {
    commandCodeQueue[i] = 0x00;
    commandDataQueue[i] = 0x00;
    commandTimeToExecute[i] = -1;
  }
  
  Serial.begin(9600);
  
  for (int i = 0; i < 8; i++) {
    digitalWrite(relays[i], HIGH);
  }
  delay(20);
  for (int i = 0; i < 8; i++) {
    pinMode(relays[i], OUTPUT);
  }

  currentDataIdx = 0;
}

/*  LOOP
        - checkTime() for delayed commands
        - reads serial if multiple bytes available
        - interprets what was read, discards if not valid
*/
void loop () {
  checkTime();
  if (Serial.available() > 1) {
    byte_buffer[0] = Serial.read();
    if ((byte_buffer[0] & addressMask) == ADDRESS) {
      byte nextOpCode = byte_buffer[0] & opCodeMask;
      int opCodeResult = processOpCode(nextOpCode);
      if (opCodeResult != 3) { 
        /*if not invalid op code*/
        byte_buffer[1] = Serial.read();
      }
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
        byte currentCRC = byte_buffer[1];
        byte assembledCommand[currentDataIdx];
        for (int i = 0; i < currentDataIdx; i++) {
          assembledCommand[i] = storedData[i];
        }
        if (currentDataIdx == expectedDataLength) {
          if (CRC8(assembledCommand, currentDataIdx) == currentCRC) {
            processCommand(assembledCommand);
          }
          else {
            sendOverSerial2(0x00, crcError);
          }
        }
        else {
          sendOverSerial2(0x00, dataLengthError);
        }
      }
      else if (opCodeResult == 3) {
        /*Invalid code -> RESET*/
        sendOverSerial2(0x00, opCodeError);
        currentDataIdx = 0;
        for (int i = 0; i < MAXDATA; i++) {
          storedData[i] = 0;
        }
      }
    }
    if ((byte_buffer[0] & opCodeMask) == opCodeList[14]) {
      byte_buffer[1] = Serial.peek();
      if (byte_buffer[1] == EEPROM.read(0)) {
        Serial.read();
        sendOverSerial2(0x01, EEPROM.read(1));
      }
    }
  }
}

byte getRelay(int relay)
{
  if(relay < 0 || relay > 7) return 0xe1;
  return digitalRead(relays[relay]);
}

void setRelay(int relay, int mode) {
  if(relay >= 0 || relay <= 7) {
    digitalWrite(relays[relay], mode);
  }
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
   
   if (idxAtOpCode > -1 && idxAtOpCode < (numOpCodes-2)) {
    expectedDataLength = opCodeLengths[idxAtOpCode];
   }
   else  if (idxAtOpCode = -1) {
    expectedDataLength == -1;
   }
   
   if (validOpCode) {
    if (opCode == opCodeList[numOpCodes-2] && currentDataIdx > 0) {
      return 1;
    }
    else if (opCode == opCodeList[numOpCodes-1] && currentDataIdx > 0) {
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
  byte opCode = currentCommand[0] & opCodeMask;
  bool openSpotInQueue;
  int currentSpot;
  long timeDelay;
  byte relayNums[8];
  
  switch (opCode) {
    case opCodeList[0]:
    setRelay(currentCommand[1], 1);
    sendOverSerial2(0x01, 0x00);
    break;
    case opCodeList[1]:
    setRelay(currentCommand[1], 0);
    sendOverSerial2(0x01, 0x00);
    break;
    case opCodeList[2]:
    sendOverSerial2(0x01, getRelay(currentCommand[1]));
    break;
    case opCodeList[3]:
    byte relayStates;
    for (int i = 0; i < 8; i++) {
     relayStates <<= 1;
     relayStates |= getRelay(i);
    }
    sendOverSerial2(0x01, relayStates);
    break;
    case opCodeList[4]:
    for (int i = 0; i < 8; i++) {
     setRelay(i, 1);
    }
    sendOverSerial2(0x01, 0x00);
    break;
    case opCodeList[5]:
    for (int i = 0; i < 8; i++) {
     setRelay(i, 0);
    }
    sendOverSerial2(0x01, 0x00);
    break;
    case opCodeList[6]:
    for (int i = 0; i < 8; i++) {
     setRelay(i, currentCommand[i+1]);
    }
    sendOverSerial2(0x01, 0x00);
    break;
    case opCodeList[7]:
    timeDelay = bytesToLong(currentCommand[2], currentCommand[3], currentCommand[4]);
    openSpotInQueue = false;
    currentSpot = 0;
    while (!openSpotInQueue && currentSpot < maxQueued) {
      if (commandTimeToExecute[currentSpot] == -1) {
        openSpotInQueue = true;
        commandTimeToExecute[currentSpot] = millis() + timeDelay;
        commandCodeQueue[currentSpot] = opCode;
        commandDataQueue[currentSpot] = currentCommand[1];
      }
      currentSpot++; 
    }
    if (!openSpotInQueue) {
      sendOverSerial2(0x00, delayQueueFullError);
    }
    else {
      sendOverSerial2(0x01, 0x00);
    }
    break;
    case opCodeList[8]:
    timeDelay = bytesToLong(currentCommand[2], currentCommand[3], currentCommand[4]);
    openSpotInQueue = false;
    currentSpot = 0;
    while (!openSpotInQueue && currentSpot < maxQueued) {
      if (commandTimeToExecute[currentSpot] == -1) {
        openSpotInQueue = true;
        commandTimeToExecute[currentSpot] = millis() + timeDelay;
        commandCodeQueue[currentSpot] = opCode;
        commandDataQueue[currentSpot] = currentCommand[1];
      }
      currentSpot++; 
    }
    if (!openSpotInQueue) {
      sendOverSerial2(0x00, delayQueueFullError);
    }
    else {
      sendOverSerial2(0x01, 0x00);
    }
    break;
    case opCodeList[9]:
    timeDelay = bytesToLong(currentCommand[2], currentCommand[3], currentCommand[4]);
    openSpotInQueue = false;
    currentSpot = 0;
    while (!openSpotInQueue && currentSpot < maxQueued) {
      if (commandTimeToExecute[currentSpot] == -1) {
        openSpotInQueue = true;
        commandTimeToExecute[currentSpot] = millis() + timeDelay;
        commandCodeQueue[currentSpot] = opCode;
        commandDataQueue[currentSpot] = currentCommand[1];
      }
      currentSpot++; 
    }
    if (!openSpotInQueue) {
      sendOverSerial2(0x00, delayQueueFullError);
    }
    else {
      sendOverSerial2(0x01, 0x00);
    }
    break;
    case opCodeList[10]:
    timeDelay = bytesToLong(currentCommand[2], currentCommand[3], currentCommand[4]);
    openSpotInQueue = false;
    currentSpot = 0;
    while (!openSpotInQueue && currentSpot < maxQueued) {
      if (commandTimeToExecute[currentSpot] == -1) {
        openSpotInQueue = true;
        commandTimeToExecute[currentSpot] = millis() + timeDelay;
        commandCodeQueue[currentSpot] = opCode;
        commandDataQueue[currentSpot] = currentCommand[1];
      }
      currentSpot++; 
    }
    if (!openSpotInQueue) {
      sendOverSerial2(0x00, delayQueueFullError);
    }
    else {
      sendOverSerial2(0x01, 0x00);
    }
    break;
    case opCodeList[11]:
    timeDelay = bytesToLong(currentCommand[9], currentCommand[10], currentCommand[11]);
    openSpotInQueue = false;
    currentSpot = 0;
    byte relayStatesToSet;
    for (int i = 1; i < 9; i++) {
     relayStatesToSet = relayStatesToSet << 1;
     relayStatesToSet |= currentCommand[i];
    }
    while (!openSpotInQueue && currentSpot < maxQueued) {
      if (commandTimeToExecute[currentSpot] == -1) {
        openSpotInQueue = true;
        commandTimeToExecute[currentSpot] = millis() + timeDelay;
        commandCodeQueue[currentSpot] = opCode;
        commandDataQueue[currentSpot] = relayStatesToSet;
      }
      currentSpot++; 
    }
    if (!openSpotInQueue) {
      sendOverSerial2(0x00, delayQueueFullError);
    }
    else {
      sendOverSerial2(0x01, relayStatesToSet);
    }
    break;
    case opCodeList[12]:
    for (int i = 0; i < 8; i++) {
      EEPROM.write(i+2, currentCommand[i+1]);
    }
    break;
    case opCodeList[13]:
    for (int i = 0; i < 8; i++) {
      relayNums[i] = EEPROM.read(i+2);
    }
    sendOverSerial(0x01, relayNums, 8);
    break;
    case opCodeList[14]:
    // do nothing, already handled in loop()
    break;
    case opCodeList[15]:
    EEPROM.write(1, currentCommand[1]);
    break;
    case opCodeList[16]:
    for (int i = 0; i < maxQueued; i++) {
      commandCodeQueue[i] = 0x00;
      commandDataQueue[i] = 0x00;
      commandTimeToExecute[i] = -1;
    }
    break;
  }
}

void sendOverSerial (byte success, byte data[], int dataLen) {
  byte addressSuccess = piAddress | success;
  byte adrSucData[dataLen+1];
  adrSucData[0] = addressSuccess;
  for (int i = 1; i < dataLen+1; i++) {
    adrSucData[i] = data[i-1];
  }
  Serial.write(addressSuccess);
  Serial.write(data[0]);
  for (int i = 1; i < dataLen; i++) {
    Serial.write(opCodeList[numOpCodes-2]);
    Serial.write(data[i]);
  }
  Serial.write(opCodeList[numOpCodes-1]);
  Serial.write(CRC8(adrSucData, dataLen+1));
}

void sendOverSerial2 (byte success, byte data) {
  byte addressSuccessData[] = {piAddress | success, data};
  Serial.write(addressSuccessData[0]);
  Serial.write(addressSuccessData[1]);
  Serial.write(piAddress | opCodeList[numOpCodes-1]);
  Serial.write(CRC8(addressSuccessData, 2));
}

long bytesToLong(long x_high, long x_low)
{
  long combined = 0;
  combined += x_high * 256;
  combined += x_low;
  return combined;
}
long bytesToLong(long x_high, long x_mid, long x_low)
{
  long combined = 0;
  combined += x_high * 256 * 256;
  combined += x_mid * 256;
  combined += x_low;
  return combined;
}

void checkTime() {
  for (int i = 0; i < maxQueued; i++) {
    if (commandTimeToExecute[i] <= millis() && commandTimeToExecute[i] != -1) {
      byte tempCommand[] = {commandCodeQueue[i], commandDataQueue[i]};
      processDelayedCommand(tempCommand);
      commandCodeQueue[i] = 0x00;
      commandDataQueue[i] = 0x00;
      commandTimeToExecute[i] = -1;
    }
  }
}

void processDelayedCommand (byte delComm[]) {
  switch (delComm[0]) {
    case opCodeList[7]:
    setRelay(delComm[1], 1);
    break;
    case opCodeList[8]:
    setRelay(delComm[1], 0);
    break;
    case opCodeList[9]:
    for (int i = 0; i < 8; i++) {
      setRelay(i, 1);
    }
    break;
    case opCodeList[10]:
    for (int i = 0; i < 8; i++) {
      setRelay(i, 0);
    }
    break;
    case opCodeList[11]:
    byte relStates = delComm[1];
    for (int i = 7; i > -1; i--) {
      byte onOff = relStates & 0x01;
      setRelay(i, onOff);
      relStates >>= 1;
    }
    break;
  }
}

