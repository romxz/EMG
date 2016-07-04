void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);

}

int sensor2Pin = A2;
int sensor3Pin = A3;
float sensorVal[] = {0,0,0};
void loop() {
  // put your main code here, to run repeatedly:
    sensorVal[1] = analogRead(sensor2Pin);
    sensorVal[2] = analogRead(sensor3Pin);
   //Serial.print(400);
 // Serial.print("\t");
  //Serial.print(700);
 
  
Serial.print("\t");
    Serial.print(sensorVal[1]);
     Serial.print("\t");
   Serial.println(sensorVal[2]);
    
//Serial.println("Hello");
delay(0.5);
}

