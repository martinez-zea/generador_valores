//escanea todos los pines de un teclado matricial

void setup(){
  Serial.begin(115200);
  for(int i = 22; i < 38; i++){
    pinMode(i, INPUT);
    digitalWrite(i, HIGH);
  }
}

void loop(){
  for(int i = 22; i<38; i++){
    int val = digitalRead(i);
    Serial.print(val);  
  }
  Serial.println();
}
