//controlar 8 shift 595 registers conectados a 16 bilateral awitches 4066
// en esta version solo se controlan 2 shift y 4 siwtches

int char_table[] = {
  //0, //resetea todos los bits y states        
  ////shift 0, bit 0, fila 1 
  64, //0 // @ -> super a, asignado por ahora a superindice a. 
  59, //1 // ; -> ;
  78, //2 // N -> ñ, por ahora
  46, //3 // . -> 
  44, //4 // , -> ,
  47, //5 // / -> /
  8,  //6 // backspace -> backspace
  32, //7 // space -> space
  ////shift 1, bit 1, fila 2
  96, //8 // tilde izquierda -> tilde, asignado por ahora.       
  49, //9// 1 -> 1      
  117,//10 // u -> u, por ahora
  104,//11// h -> h
  98, //12// b -> b      
  105, //13// i -> i
  17, //14// DC1 -> arrow up, por ahora      
  31, //15// US -> alt
  //shift 2, bit 2, fila 3
  50, //16//2 -> 2
  30, //17//RS -> abre admiracion, temporal  
  101, //18// e -> e
  102, //19//f -> f
  99, //20// c -> c
  114, //21//r -> r
  29, //22//GS -> cubierta abierta
  28, //23//FS -> code
  //shift 3, bit 3, fila 4
  52, //24// 4 -> 4
  51, //25// 3 -> 3
  116,//26// t -> t
  103, //27//  g -> g
  118, //28// v -> v
  121, //29// y -> y
  15, //30// EM -> index
  26, //31// SUB -> replace
  //shift 4, bit 4, fila 5
  54, //32// 6 -> 6
  53, //33// 5 -> 5
  113, //34// q -> q
  100, //35// d -> d
  120, //36// x -> x
  119, //37// w -> w
  20, //38// DC4 -> rigth arrow
  24, //39// CANCEL -> word out
  //shift 5, bit 5, fila 6
  45, //40// - -> -
  61, //41// = -> =
  111, //42// o -> o
  97, //43//a -> a
  110, //44// n -> n
  112, //45// p -> p
  18, //46// DC2 -> arrow down
  13, //47// CR -> enter
  //shift 6, bit 6, fila 7
  48, //48// 0 -> 0
  57, //49// 9 -> 9
  108, //50// l -> l
  115, //51// s -> s
  122, //52// z -> z
  23, //53// ETB -> caps lock
  22, //54// SYN -> insercion de papel (flecha blanca en suggestion key)
  21, //55// NAK -> tw/wp
  //shift 7, bit 7, fila 8
  56, //56// 8 -> 8
  55, //57// 7 -> 7
  107, //58// k -> k
  106, //59// j -> j
  109, //60// m -> m
  9, //61// TAB -> tab
  19, //62// DC3 -> left arrow
  127, //63// DEL -> delete
};

//numero de bits a escribir = numero de shift regs
int numbits = 8; 

//numero de pines usados en el arduino
int numpins = 24;

long limit;
long past;

int bits[8]; //bits a enviar a la maquina
int states[8]; //estados de los pines, asociados a los bits
//uint8_t bits[1];
//int pins[24];
int pins[] = {
  22, 23, 24, 
  25, 26, 27, 
  31, 32, 33,
  34, 35, 36,
  37, 38, 39, 
  40, 41, 42, 
  43, 44, 45, 
  46, 47, 48 
};

int inval;
boolean dowrite;
int firstpin;

void setup(){
  Serial.begin (9600);

  for(int i = 0; i < sizeof(bits); i++){
    bits[i] = 0;
    states[i] = 0;
  }

  //inicializa los pines
  for(int i = 0; i < numpins; i ++){
    //int pin = i + 22; // se usan los pines del 22 en adelante
    //pins[i] = pin;
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
      //setBit(0);
      resetBits();
      writeBits();
      //reset();
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

    Serial.print("shift :");
    Serial.print(counter);
    Serial.print(": ");
    Serial.println(bits[counter]);
   
 /* 
    int data = i;
    int latch = i + 1;
    int clock = i + 2;
*/
    byte bitToSend = 0;
    digitalWrite(pins[latch], LOW);
    bitWrite(bitToSend, bits[counter], states[counter]);
    shiftOut(pins[data], pins[clock], MSBFIRST, bitToSend);
    //shiftOut(pins[data], pins[clock], MSBFIRST, bits[counter]);
    digitalWrite(pins[latch], HIGH);

    Serial.print("state ");
    Serial.print(counter);
    Serial.print(": " );
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

void reset(){
  int shiftcount = 0;
  int statecount = 0;
  for(int i = 0; i < numpins; i+= 3){
    //int pincount = 0;
    int data = i + 2;
    int latch = i + 1;
    int clock = i;

    //Serial.print("shift: ");
    //Serial.println(shiftcount);

    for(int j = 0; j < 8; j++){
      byte bitToSend = 0;
      digitalWrite(pins[latch], LOW);
      bitWrite(bitToSend, j, LOW);
      
      shiftOut(pins[data], pins[clock], MSBFIRST, bitToSend);
      //shiftOut(pins[data], pins[clock], MSBFIRST, bits[counter]);

      //Serial.print("pin number: ");
      //Serial.println(j);
      digitalWrite(pins[latch], HIGH);
      states[statecount] = 0;
      statecount++;
    }
    shiftcount++;
  }
}

void setBit(int data){
  int index = 0;
  for(int i = 0; i < sizeof(char_table); i++){
    
    if(data > 0 && data == char_table[i]){

      
      index = i;
      int bitindex = index/8; //encuentra el indice del bit correspondiente
      int bitval = index%8;
      bits[bitindex] = bitval;
      states[bitindex] = 1;
    //}else if(data == 0){
      //resetBits();
    }
  }
}

void resetBits(){
  for(int i = 0; i < sizeof(states); i ++){
    bits[i] = 0;
    states[i] = 0;
  }
}
/*
//table

int char_table[] = {
  0, //resetea todos los bits y states        
  ////shift 0, bit 0, fila 1 
  64, // @ -> super a, asignado por ahora a superindice a. 
  59, // ; -> ;
  78, // N -> ñ, por ahora
  46,// . -> 
  44,// , -> ,
  47,// / -> /
  8, // backspace -> backspace
  32, // space -> space
  ////shift 1, bit 1, fila 2
  96, // tilde izquierda -> tilde, asignado por ahora.       
  49, // 1 -> 1      
  117, // u -> u, por ahora
  104, // h -> h
  98, // b -> b      
  105, // i -> i
  17, // DC1 -> arrow up, por ahora      
  31, // US -> alt
  //shift 2, bit 2, fila 3
  50, //2 -> 2
  30, //RS -> abre admiracion, temporal  
  101, // e -> e
  102, //f -> f
  99, // c -> c
  114, //r -> r
  29, //GS -> cubierta abierta
  28, //FS -> code
  //shift 3, bit 3, fila 4
  52, //4 -> 4
  51, //3 -> 3
  116,//t -> t
  118, // v -> v
  121, // y -> y
  15, // EM -> index
  26, //SUB -> replace
  //shift 4, bit 4, fila 5
  54, //6 -> 6
  53, // 5 -> 5
  113, // q -> q
  100, //d -> d
  120, // x -> x
  119, // w -> w
  20, //DC4 -> rigth arrow
  24, // CANCEL -> word out
  //shift 5, bit 5, fila 6
  45, // - -> -
  61, // = -> =
  111, // o -> o
  97, //a -> a
  110, //n -> n
  112, // p -> p
  18, //DC2 -> arrow down
  13, // CR -> enter
  //shift 6, bit 6, fila 7
  48, // 0 -> 0
  57, // 9 -> 9
  108, // l -> l
  115, // s -> s
  122, // z -> z
  23, // ETB -> caps lock
  22, // SYN -> insercion de papel (flecha blanca en suggestion key)
  21, // NAK -> tw/wp
  //shift 7, bit 7, fila 8
  56, // 8 -> 8
  55, // 7 -> 7
  107, // k -> k
  106, // j -> j
  109, // m -> m
  9, // TAB -> tab
  19, //DC3 -> left arrow
  127, // DEL -> delete
};
*/
