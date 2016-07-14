/*
  #include <SoftwareSerial.h>
  #include <math.h>
  /*Declare your sensor pins as variables. I'm using Analog In pins 0 and 1. Change the names and numbers as needed
  Pro tip: If you're pressed for memory, use #define to declare your sensor pins without using any memory. Just be careful that your pin name shows up NOWHERE ELSE in your sketch!
  for more info, see: http://arduino.cc/en/Reference/Define
*/
int sensor1Pin = A2;// sensor 1
int sensor2Pin = A3;// sensor 2
int sensor3Pin = A4;// sensor 3
int sensor4Pin = A5;
int max1 = 600;
int max2 = 300;


void setup() {

  Serial.begin(9600); //This line tells the Serial port to begin communicating at 9600 bauds
  pinMode(sensor1Pin, INPUT);
  digitalWrite(sensor1Pin, LOW);
  pinMode(sensor2Pin, INPUT);
  digitalWrite(sensor2Pin, LOW);
  pinMode(sensor3Pin, INPUT);
  digitalWrite(sensor3Pin, LOW);
  pinMode(sensor4Pin, INPUT);
  digitalWrite(sensor4Pin, LOW);
}

int counterArray = 0, counterRMS = 0;
int amplifier3 = 2;
float sensorVal[] = {0, 0, 0, 0};
int numSamples = 150; //number of samples in a window of (0.1 second)
const int numWindow = 15;
const double delayTime = .1;
//double arrayRMS1[10], arrayRMS2[10], arrayRMS3[10], arrayRMS4[10];
double arrayRMS1[numWindow], arrayRMS2[numWindow], arrayRMS3[numWindow], arrayRMS4[numWindow];
int numSensors = 4;

double maxi(double a[])
{
  double maximum = a[0];
  for (int i = 0; i < numWindow; i++)
  {
    if (a[i] > maximum)
      maximum = a[i];
  }
  return maximum;
}
double mini(double a[])
{
  double minimum = a[0];
  for (int i = 0; i < numWindow; i++)
  {
    if (a[i] < minimum)
      minimum = a[i];
  }
  return minimum;
}

double avgW(double a[], int index) {
  double averageW = numWindow * a[index];
  for (int i = 1; i < numWindow; i++) {
    index = index - 1;
    if (index < 0) {
      index = numWindow - 1;
    }
    averageW = averageW + (numWindow - i) * a[index];
  }
  averageW = averageW / (numWindow * numWindow);
  return averageW;
}

void loop() {
  double rmsRAW1 = 0.0, rmsRAW2 = 0.0, rmsRAW3 = 0.0, rmsRAW4 = 0.0,
         rmsMOD1 = 0.0, rmsMOD2 = 0.0, rmsMOD3 = 0.0, rmsMOD4 = 0.0,
         logrmsMOD1 = 0.0, logrmsMOD2 = 0.0, logrmsMOD3 = 0.0, logrmsMOD4 = 0.0,
         sumSquares1 = 0.0, sumSquares2 = 0.0, sumSquares3 = 0.0, sumSquares4 = 0.0;
  double pa3, pb3, pc3, a3, b3, c3, r3, d3,
         aa3, bb3, cc3, modulator3;

  while (counterRMS < numSamples)
  {
    sensorVal[0] = analogRead(sensor1Pin);
    delay(delayTime);
    sensorVal[1] = analogRead(sensor2Pin);
    delay(delayTime);
    sensorVal[2] = analogRead(sensor3Pin);
    delay(delayTime);
    sensorVal[3] = analogRead(sensor4Pin);
    delay(delayTime);
    sumSquares1 = sumSquares1 + sensorVal[0] * sensorVal[0];
    sumSquares2 = sumSquares2 + sensorVal[1] * sensorVal[1];
    sumSquares3 = sumSquares3 + sensorVal[2] * sensorVal[2];
    sumSquares4 = sumSquares4 + sensorVal[3] * sensorVal[3];

    //delay(0.5); //total delay of .5 millisecond of 2000 samples a second
    counterRMS = counterRMS + 1;
  }
  counterRMS = 0;

  //unsigned long currentTime=micros();
  //  elapsed=currentTime-startTime;
  rmsRAW1 = sqrt(sumSquares1 / numSamples);
  rmsRAW2 = sqrt(sumSquares2 / numSamples);
  rmsRAW3 = sqrt(sumSquares3 / numSamples);
  rmsRAW4 = sqrt(sumSquares4 / numSamples);
  arrayRMS1[counterArray] = rmsRAW1;
  arrayRMS2[counterArray] = rmsRAW2;
  arrayRMS3[counterArray] = rmsRAW3;
  arrayRMS4[counterArray] = rmsRAW4;

  //rmsMOD1 = 0.8 * maxi(arrayRMS1) + 0.1 * mini(arrayRMS1) + 0.3 * arrayRMS1[counterArray];
  //rmsMOD2 = 0.8 * maxi(arrayRMS2) + 0.2 * arrayRMS2[counterArray];
  //rmsMOD3 = 0.8 * maxi(arrayRMS3) + 0.2 * arrayRMS3[counterArray];
  rmsMOD1 = avgW(arrayRMS1, counterArray);
  rmsMOD2 = avgW(arrayRMS2, counterArray);
  rmsMOD3 = avgW(arrayRMS3, counterArray);
  rmsMOD4 = avgW(arrayRMS4, counterArray);

  //if (rmsMOD2 > max2){
  //  rmsMOD2 = max2;
  //}
  //rmsMOD2 = 2 * rmsMOD2;
  //if (rmsMOD3 > max1){
  //  rmsMOD3 = max1;
  //}
  if (rmsMOD1 < 0.001) {
    rmsMOD1 = 0.001;
  }
  if (rmsMOD2 < 0.001) {
    rmsMOD2 = 0.001;
  }
  if (rmsMOD3 < 0.001) {
    rmsMOD3 = 0.001;
  }
  if (rmsMOD4 < 0.001) {
    rmsMOD4 = 0.001;
  }

  logrmsMOD1 = log(rmsMOD1);
  logrmsMOD2 = log(rmsMOD2);
  logrmsMOD3 = log(rmsMOD3);
  logrmsMOD4 = log(rmsMOD4);
  if (logrmsMOD1 < -1) {
    logrmsMOD1 = -1;
  }
  if (logrmsMOD2 < -1) {
    logrmsMOD2 = -1;
  }
  if (logrmsMOD3 < -1) {
    logrmsMOD3 = -1;
  }
  if (logrmsMOD4 < -1) {
    logrmsMOD4 = -1;
  }


  //Serial.print(logrmsMOD1); //a0
  //Serial.print(",");

  // For 3 sensos:
  /*
    r3 = sqrt(logrmsMOD2 * logrmsMOD2 + logrmsMOD3 * logrmsMOD3 + logrmsMOD4 * logrmsMOD4);
    a3 = logrmsMOD2 - logrmsMOD3;
    b3 = logrmsMOD3 - logrmsMOD4;
    c3 = logrmsMOD4 - logrmsMOD2;
    d3 = abs(a3) + abs(d3) + abs(c3) + 1;
    pa3 = r3 * (1 + amplifier3 * a3 / d3);
    pb3 = r3 * (1 + amplifier3 * b3 / d3);
    pc3 = r3 * (1 + amplifier3 * c3 / d3);
    modulator3 = 0.8;
    aa3 = modulator3 * logrmsMOD2 + (1-modulator) * pa3;
    bb3 = modulator3 * logrmsMOD3 + (1-modulator) * pb3;
    cc3 = modulator3 * logrmsMOD4 + (1-modulator) * pc3;
  */
  double r4, ra4, rb4, rc4, rd4,
         da4, db4, dc4, dd4,
         s4, pa4, pb4, pc4, pd4,
         fa4, fb4, fc4, fd4;
  double modulator4 = 0.8;
  double amplifier4 = 2;
  r4 = sqrt(logrmsMOD1 * logrmsMOD1 + logrmsMOD2 * logrmsMOD2 + logrmsMOD3 * logrmsMOD3 + logrmsMOD4 * logrmsMOD4);
  ra4 = sqrt(logrmsMOD2 * logrmsMOD2 + logrmsMOD3 * logrmsMOD3 + logrmsMOD4 * logrmsMOD4);
  rb4 = sqrt(logrmsMOD1 * logrmsMOD1 + logrmsMOD3 * logrmsMOD3 + logrmsMOD4 * logrmsMOD4);
  rc4 = sqrt(logrmsMOD2 * logrmsMOD2 + logrmsMOD1 * logrmsMOD1 + logrmsMOD4 * logrmsMOD4);
  rd4 = sqrt(logrmsMOD2 * logrmsMOD2 + logrmsMOD3 * logrmsMOD3 + logrmsMOD1 * logrmsMOD1);
  da4 = 3 * logrmsMOD1 - ra4;
  db4 = 3 * logrmsMOD2 - rb4;
  dc4 = 3 * logrmsMOD3 - rc4;
  dd4 = 3 * logrmsMOD4 - rd4;
  s4 = abs(da4) + abs(db4) + abs(dc4) + abs(dd4) + 1;
  pa4 = r4 * (1 + amplifier4 * da4 / s4 );
  pb4 = r4 * (1 + amplifier4 * db4 / s4 );
  pc4 = r4 * (1 + amplifier4 * dc4 / s4 );
  pd4 = r4 * (1 + amplifier4 * dd4 / s4 );
  fa4 = modulator4 * logrmsMOD1 + (1 - modulator4) * pa4;
  fb4 = modulator4 * logrmsMOD2 + (1 - modulator4) * pb4;
  fc4 = modulator4 * logrmsMOD3 + (1 - modulator4) * pc4;
  fd4 = modulator4 * logrmsMOD4 + (1 - modulator4) * pd4;

  Serial.print(fa4);
  Serial.print(",");
  Serial.print(fb4);
  Serial.print(",");
  Serial.print(fc4);
  Serial.print(",");
  Serial.println(fd4);


  /*
    Serial.print(pa3); //a3
    Serial.print(",");
    Serial.print(pb3); //a4
    Serial.print(",");
    Serial.print(pc3); //a5
    Serial.print(",");
  */
  /*
    Serial.print(aa3); //a3
    Serial.print(",");
    Serial.print(bb3); //a4
    Serial.print(",");
    Serial.print(cc3); //a5
    Serial.print(",");
    Serial.println((aa3+bb3+cc3)/3); //a5
  */
  /*
    Serial.print(logrmsMOD1); //a2
    Serial.print(",");
    Serial.print(logrmsMOD2); //a3
    Serial.print(",");
    Serial.print(logrmsMOD3); //a4
    Serial.print(",");
    Serial.println(logrmsMOD4); //a5
  */

  counterArray++;
  if (counterArray >= numWindow) {
    counterArray = 0;
  }
}


