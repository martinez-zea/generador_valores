int ser = 0;
int pin = 23;
int led = 13;
int prev = 1;
int count;
long time;
long lowtime;
long cycletime;
int ciclos = 0;

void setup(){
  pinMode(pin, INPUT);
  digitalWrite(pin, HIGH);// esto es importante para obtener la lectura de lines de escaneo
  pinMode(led, OUTPUT);
  Serial.begin(115200);
  time = millis();
  lowtime = millis();
  cycletime = micros();
}

void loop(){
  ser = digitalRead(pin);

  if(ser == 0 && prev == 1){
    digitalWrite(led, HIGH);
    count++;
    //long result = micros() - cycletime;
    //Serial.print("ciclo: ");
    //Serial.println(result);
    //cycletime = micros(); // ±17480 en gx9500
    lowtime = millis();
    
  }else if(ser == 1 && prev == 0){
    digitalWrite(led, LOW);
    long result = millis() - lowtime; 
    Serial.print("time low: "); //toma mas o menos ±2040 micros.
    Serial.println(result);
  }
  
  /*
  cada linea baja 54 a 55 veces por segundo. es decir 0.018 segundos
  */
  /*
  if(micros() - time > 1000000){
    Serial.println(count);
    count = 0;
    //Serial.print("ciclos: ");
    //Serial.println(ciclos);
    time = micros();
  } 
  */
  prev = ser;
}
