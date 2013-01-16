uint8_t sensors;

struct{
  uint8_t paperin:1;
  uint8_t paperout:1;
}sens;

void setup(){
  Serial.begin(115200);
  DDRL = 0x00; 
}

void loop(){
  sensors = PINL;
  //extrae 1er bit
  uint8_t b = sensors & ( 1 >> 0);
  Serial.println(b, BIN);
  //sens.paperin = sensors >> 1;
  //Serial.println(sens.paperin, BIN);
  //sens.paperout = sensors >> 2;
  //Serial.println(sens.paperout, BIN);

  
}


