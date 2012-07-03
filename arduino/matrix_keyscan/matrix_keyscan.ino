

void setup(){
  Serial.begin(115200);
  for(int i = 22; i <= 37; i++){
    pinMode(i, INPUT);
    digitalWrite(i, HIGH);
  }
 /*
  for(int i = 30; i <=37; i++){
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }
  */
}

void loop(){

  for(int i = 22; i <= 37; i ++){
    int val = digitalRead(i);
    Serial.print(val);
  }
  /*
  for(int i = 30; i <= 37; i++){
    digitalWrite(i, HIGH);
  }
  */  
  Serial.println();
  //delay(10);
}

/*
boolean dowrite;

void setup(){
  Serial.begin(115200);
  for(int i = 22; i < 30; i++){
    pinMode(i, OUTPUT);
  }
  dowrite = false;
}

void loop(){
  
  
  if(Serial.available() > 0){
    dowrite = true;

  }
  for(int i = 22; i < 30; i ++ ){
    if(dowrite && i == 25){
      digitalWrite(i, LOW);
      delay(100);
      digitalWrite(i, HIGH);
    }else{
      digitalWrite(i, HIGH);
    }
  }
}
*/
