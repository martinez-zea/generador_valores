int ser = 0;
int inpin = 26;
int outpin = 33;
int led = 13;
int prev = 1;
//int count;
long time;
//long lowtime;
boolean dowrite;
boolean off;
int state = 1;
int count = 0;

void setup(){
  pinMode(inpin, INPUT);
  digitalWrite(inpin, HIGH);
  pinMode(outpin, OUTPUT);
  pinMode(led, OUTPUT);
  Serial.begin(115200);
  time = millis();
  //lowtime = millis();
  //off = false;
  dowrite = false;
}

void loop(){
  ser = digitalRead(inpin);
  if(Serial.available() > 0){
    int val = Serial.read();
    dowrite = true;
    time = millis();
  }

 
  if(ser == 0 && prev == 1){
    //digitalWrite(led, HIGH);
    //count++;
    //lowtime = millis();
    off = true;
    Serial.println("on");
    
  }else if(ser == 1 && prev == 0){
    //digitalWrite(led, LOW);
    //long result = millis() - lowtime; 
    //Serial.print("time low: ");
    //Serial.println(result);
    off = false;
    Serial.println("off");
  } 
  
  if(dowrite){
    count++;
    Serial.println(count);
    if(millis() - time < 1000){
      
      if(off){
        Serial.println("low");
        digitalWrite(outpin, LOW);
      }else{
        Serial.println("high");
        digitalWrite(outpin, HIGH);
      }
      
      //digitalWrite(outpin, LOW);
    }else{
      Serial.println("time is up");
      dowrite = false;  
    }
  }else{
    count = 0;
    digitalWrite(outpin, HIGH);
  }
  /*
  if(micros() - time > 1000000){
    Serial.println(count);
    count = 0;
    time = micros();
  } 
  */
  prev = ser;
}
