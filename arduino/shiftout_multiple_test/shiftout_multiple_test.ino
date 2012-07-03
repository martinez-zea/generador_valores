//controlar 8 shift 595 registers conectados a 16 bilateral awitches 4066
// en esta version solo se controlan 2 shift y 4 siwtches

//numero de bits a escribir = numero de shift regs
int numbits = 2; 

//numero de pines usados en el arduino
int numpins = 6;

long limit;
long past;

int bits[2]; //bits a enviar a la maquina
int states[2]; //estados de los pines, asociados a los bits
//uint8_t bits[1];
int pins[6];
int inval;
boolean dowrite;
int firstpin;

void setup(){
  Serial.begin (9600);

  for(int i = 0; i < numbits; i++){
    bits[i] = 9;
    states[i] = 0;
  }

  //inicializa los pines
  for(int i = 0; i < numpins; i ++){
    int pin = i + 22; // se usan los pines del 22 en adelante
    pins[i] = pin;
    pinMode(pins[i], OUTPUT);
    Serial.println(pins[i]);
  }

  dowrite = false;
  limit = 200;
  past = millis();
}

void loop(){

  //serial input

  if(Serial.available() > 0){
    inval = Serial.read();
    Serial.print("inval: ");
    Serial.println(inval);
    setBit(inval);
    dowrite = true;
  }

  if( millis() - past > limit){
    if(dowrite){
      Serial.println("write!");
      writeBits();
    }else{
      setBit(0);
      writeBits();
    }
    dowrite = false;
    past = millis();
  }
}

void writeBits(){
  //bits[0] = 1;
  int counter = 0;
  for(int i = 0; i < numpins; i += 3){
    int data = i + 2;
    int latch = i + 1;
    int clock = i;
    byte bitToSend = 0;
    digitalWrite(pins[latch], LOW);
    bitWrite(bitToSend, bits[counter], states[counter]);
    shiftOut(pins[data], pins[clock], MSBFIRST, bitToSend);
    //shiftOut(pins[data], pins[clock], MSBFIRST, bits[counter]);
    digitalWrite(pins[latch], HIGH);
    
    Serial.print("bit ");
    Serial.print(counter);
    Serial.print(": ");
    Serial.println(bits[counter]);
    Serial.print("state ");
    Serial.print(counter);
    Serial.print(": ");
    Serial.println(states[counter]);

    /*
    Serial.print("clock: ");
    Serial.println(pins[clock]);
    Serial.print("latch: ");
    Serial.println(pins[latch]);
    Serial.print("data: ");
    Serial.println(pins[data]);
    */
    
    counter++;
    //delay(200);
  }
}

/*
  switch case es provisional, 
  en el futuro cambiara por un array 
  con los valores de los estados y los bits
*/

void setBit(int val){
  switch(val){
    
    case 0: //NULL -> apaga todos los siwtches

      for(int i = 0; i < numbits; i++){
        bits[i] = 0;
        states[i] = 0;
      }
      break;
      
    ////shift 0, bit 0 
    case 64: // @ -> super a, asignado por ahora a superindice a. 
      bits[0] = 0;
      states[0] = 1;
      break;
      
    case 59: // ; -> ;
      bits[0] = 1;
      states[0] = 1;
      break;
      
    case 78: // N -> ñ, por ahora
      bits[0] = 2;
      states[0] = 1;
      break;
      
    case 46:
      bits[0] = 3; // . -> .
      states[0] = 1;
      break;
      
    case 44:
      bits[0] = 4; // , -> ,
      states[0] = 1;
      break;
      
    case 47:
      bits[0] = 5; // / -> /
      states[0] = 1;
      break;
      
    case 8:
      bits[0] = 6; // backspace -> backspace
      states[0] = 1;
      break;
      
    case 32: // space -> space
      bits[0] = 7;
      states[0] = 1;
      break;
      
     ////shift 1, bit 1
    case 96: // tilde izquierda -> tilde, asignado por ahora. 
      bits[1] = 0;
      states[1] = 1;
      break;
      
    case 49: // 1 -> 1
      bits[1] = 1;
      states[1] = 1;
      break;
      
    case 117: // u -> u, por ahora
      bits[1] = 2;
      states[1] = 1;
      break;
      
    case 104:
      bits[1] = 3; // h -> h
      states[1] = 1;
      break;
      
    case 98:
      bits[1] = 4; // b -> b
      states[1] = 1;
      break;
      
    case 105:
      bits[1] = 5; // i -> i
      states[1] = 1;
      break;
      
    case 17:
      bits[1] = 6; // DC1 -> arrow up, por ahora
      states[1] = 1;
      break;
      
    case 31: // US -> alt
      bits[1] = 7;
      states[1] = 1;
      break;
      
    default:
      for(int i = 0; i < numbits; i++){
        states[i] = 0;
        bits[i] = 0;
      }
      break;
  }
}

