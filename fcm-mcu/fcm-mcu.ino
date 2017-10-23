#define ADDRESS 0x01
#define STOPCODE 0xff
#define BBSIZE 10
#define BYTES_TO_PROCESS 3

#define OPCODE_ON 0xc1
#define OPCODE_OFF 0xc0
#define OPCODE_GET 0xc3

#define Relay0 12
#define Relay1 11
#define Relay2 10
#define Relay3 9
#define Relay4 8
#define Relay5 7
#define Relay6 6
#define Relay7 5

int relays[] = {Relay0, Relay1, Relay2, Relay3, Relay4, Relay5, Relay6, Relay7};

byte byte_buffer[BBSIZE];

void processBytes();
bool setRelay(int, int);
byte getRelay(int);
 
void setup() {
   Serial.begin(9600);
  
  for (int i = 0; i < 8; i++) {
    digitalWrite(relays[i], HIGH);
    pinMode(relays[i], OUTPUT);
  }
}

byte incoming_byte;


void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    incoming_byte = Serial.read();
    if(incoming_byte == ADDRESS) {
      int len = Serial.readBytesUntil(STOPCODE, byte_buffer, BBSIZE);
      if(len == BYTES_TO_PROCESS){
        processBytes(byte_buffer);
      }
    }
  }
}

void processBytes(byte b_buffer[10]) {
    Serial.write(0xc4);
    byte opcode = b_buffer[0];
    
    if (b_buffer[2] != STOPCODE) {
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

