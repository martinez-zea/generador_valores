/*
  envia caracteres a la maquina de escribir usando 1 solo
  shift register 74hc595 y  2 switches bolaterales 4066
 */


//Pin connected to clock pin (SH_CP) of 74HC595 (pin 11)
const int clock = 5;
//Pin connected to latch pin (ST_CP) of 74HC595 (pin 12)
const int latch = 6;
//Pin connected to Data in (DS) of 74HC595 (pin 14)
const int data = 7;

boolean dowrite;

int disabled = 0;
int bitToSet;

void setup() {
  //set pins to output because they are addressed in the main loop
  pinMode(latch, OUTPUT);
  pinMode(data, OUTPUT);  
  pinMode(clock, OUTPUT);
  Serial.begin(9600);
  Serial.println("reset");
}

void loop() {
  if (Serial.available() > 0) {
    // ASCII '0' through '9' characters are
    // represented by the values 48 through 57.
    // so if the user types a number from 0 through 9 in ASCII, 
    // you can subtract 48 to get the actual value:
    int inval = Serial.read();
    setBit(inval);
    dowrite = true;

  // write to the shift register with the correct bit set high:

  }
  if(dowrite){
    
    registerWrite(bitToSet, HIGH);
    dowrite = false;
  }
}

// This method sends bits to the shift register:

void registerWrite(int whichPin, int whichState) {
// the bits you want to send
  byte bitsToSend = 0;
  // turn off the output so the pins don't light up
  // while you're shifting bits:
  digitalWrite(latch, LOW);

  // turn on the next highest bit in bitsToSend:
  bitWrite(bitsToSend, whichPin, whichState);

  shiftOut(data, clock, MSBFIRST, bitsToSend);

  digitalWrite(latch, HIGH);
  delay(1000);
  digitalWrite(latch, LOW);
  shiftOut(data, clock, MSBFIRST, disabled);
  digitalWrite(latch, HIGH);
}

void setBit(int val){
  switch(val){
    
    case 0: //NULL -> apaga todos los siwtches
      bitToSet = 9;
    
    case 64: // @ -> super a, asignado por ahora a superindice a. 
      bitToSet = 0;
      break;
      
    case 59: // ; -> ;
      bitToSet = 1;
      break;
      
    case 78: // N -> ñ, por ahora
      bitToSet = 2;
      break;
      
    case 46:
      bitToSet = 3; // . -> .
      break;
      
    case 44:
      bitToSet = 4; // , -> ,
      break;
      
    case 47:
      bitToSet = 5; // / -> /
      break;
      
    case 8:
      bitToSet = 6; // backspace -> backspace
      break;
      
    case 32: // space -> space
      bitToSet = 7;
      break;
      
    default:
      bitToSet = 9;
  }
}
