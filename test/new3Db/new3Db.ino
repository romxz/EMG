/*
  #include <SoftwareSerial.h>
  #include <math.h>
  /*Declare your sensor pins as variables. I'm using Analog In pins 0 and 1. Change the names and numbers as needed
  Pro tip: If you're pressed for memory, use #define to declare your sensor pins without using any memory. Just be careful that your pin name shows up NOWHERE ELSE in your sketch!
  for more info, see: http://arduino.cc/en/Reference/Define
*/
int sensor1Pin = A2; // sensor 1
#define sensor2Pin A3 // sensor 2
#define sensor3Pin A4 // sensor 3
#define sensor4Pin A5 // sensor 4

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
float sensorVal[] = {0, 0, 0, 0};
// Window and sampling variables
#define numWindow 50
double arrayRMS1[numWindow], arrayRMS2[numWindow], arrayRMS3[numWindow], arrayRMS4[numWindow];
#define numSamples 150 //number of samples in a window of (0.1 second)
#define averageConstantFactor 0
#define averageLinearFactor 0
#define averageSquaredFactor 1
#define averageRootFactor 1
#define delayTime 0.1
#define numSensors 4
// Variables when using 3 sensors
#define amplifier3 2
// Variables when using 4 sensors
#define modulator4 0.3
#define amplifier4 10
// Print Modes
#define printnewNormal true
#define printnewLog false
#define printrms false
#define printrmsavg false
#define printrmsRAW false
// Parameteters for modifying 4-sensors signal
double radius4, rem_a4, rem_b4, rem_c4, rem_d4,
       rmsDIF_a4, rmsDIF_b4, rmsDIF_c4, rmsDIF_d4,
       rmsDIF_norm, rmsAMP_a4, rmsAMP_b4, rmsAMP_c4, rmsAMP_d4,
       rmsMOD_a4, rmsMOD_b4, rmsMOD_c4, rmsMOD_d4;
#define rmsDIF_scale 4
double logrmsMOD_a4, logrmsMOD_b4, logrmsMOD_c4, logrmsMOD_d4;

double avgW(double a[], int index) {
  double averageW;
  averageW = (numWindow + averageConstantFactor) * a[index];
  for (int ishift = 1; ishift < numWindow; ishift++) {
    index = index - 1;
    if (index < 0) {
      index = numWindow - 1;
    }
    averageW = averageW + (averageConstantFactor + averageRootFactor * sqrt(numWindow - ishift) + averageLinearFactor * (numWindow - ishift) + averageSquaredFactor * (numWindow - ishift) * (numWindow - ishift)) * a[index];
  }
  averageW = averageW / ((numWindow + averageConstantFactor) * (numWindow + averageConstantFactor));
  return averageW;
}

void loop() {
  double rmsRAW1 = 0.0, rmsRAW2 = 0.0, rmsRAW3 = 0.0, rmsRAW4 = 0.0,
         rmsAVG1 = 0.0, rmsAVG2 = 0.0, rmsAVG3 = 0.0, rmsAVG4 = 0.0,
         logrmsAVG1 = 0.0, logrmsAVG2 = 0.0, logrmsAVG3 = 0.0, logrmsAVG4 = 0.0,
         sumSquares1 = 0.0, sumSquares2 = 0.0, sumSquares3 = 0.0, sumSquares4 = 0.0;
  double pa3, pb3, pc3, a3, b3, c3, r3, d3,
         aa3, bb3, cc3, modulator3;
  for (int counterRMS=0; counterRMS < numSamples; counterRMS++)
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
  }

  // unsigned long currentTime=micros();
  // elapsed=currentTime-startTime;
  rmsRAW1 = sqrt(sumSquares1 / numSamples);
  rmsRAW2 = sqrt(sumSquares2 / numSamples);
  rmsRAW3 = sqrt(sumSquares3 / numSamples);
  rmsRAW4 = sqrt(sumSquares4 / numSamples);
  
  if (printrmsRAW == true) {
    Serial.print(rmsRAW1); //a2
    Serial.print(",");
    Serial.print(rmsRAW2); //a3
    Serial.print(",");
    Serial.print(rmsRAW3); //a4
    Serial.print(",");
    Serial.println(rmsRAW4); //a5
  }
  
  arrayRMS1[counterArray] = rmsRAW1;
  arrayRMS2[counterArray] = rmsRAW2;
  arrayRMS3[counterArray] = rmsRAW3;
  arrayRMS4[counterArray] = rmsRAW4;
  rmsAVG1 = avgW(arrayRMS1, counterArray);
  rmsAVG2 = avgW(arrayRMS2, counterArray);
  rmsAVG3 = avgW(arrayRMS3, counterArray);
  rmsAVG4 = avgW(arrayRMS4, counterArray);
  
  if (printrmsavg == true) {
    Serial.print(rmsAVG1); //a2
    Serial.print(",");
    Serial.print(rmsAVG2); //a3
    Serial.print(",");
    Serial.print(rmsAVG3); //a4
    Serial.print(",");
    Serial.println(rmsAVG4); //a5
  }

  
  // Manipulating 4-sensor signal
  radius4 = sqrt(rmsAVG1 * rmsAVG1 + rmsAVG2 * rmsAVG2 + rmsAVG3 * rmsAVG3 + rmsAVG4 * rmsAVG4);
  rem_a4 = sqrt(rmsAVG2 * rmsAVG2 + rmsAVG3 * rmsAVG3 + rmsAVG4 * rmsAVG4);
  rem_b4 = sqrt(rmsAVG1 * rmsAVG1 + rmsAVG3 * rmsAVG3 + rmsAVG4 * rmsAVG4);
  rem_c4 = sqrt(rmsAVG2 * rmsAVG2 + rmsAVG1 * rmsAVG1 + rmsAVG4 * rmsAVG4);
  rem_d4 = sqrt(rmsAVG2 * rmsAVG2 + rmsAVG3 * rmsAVG3 + rmsAVG1 * rmsAVG1);
  rmsDIF_a4 = rmsDIF_scale * rmsAVG1 - rem_a4;
  rmsDIF_b4 = rmsDIF_scale * rmsAVG2 - rem_b4;
  rmsDIF_c4 = rmsDIF_scale * rmsAVG3 - rem_c4;
  rmsDIF_d4 = rmsDIF_scale * rmsAVG4 - rem_d4;
  rmsDIF_norm = rem_a4 + rem_b4 + rem_c4 + rem_d4 + 1;
  rmsAMP_a4 = radius4 * amplifier4 * (1 + rmsDIF_a4 / rmsDIF_norm );
  rmsAMP_b4 = radius4 * amplifier4 * (1 + rmsDIF_b4 / rmsDIF_norm );
  rmsAMP_c4 = radius4 * amplifier4 * (1 + rmsDIF_c4 / rmsDIF_norm );
  rmsAMP_d4 = radius4 * amplifier4 * (1 + rmsDIF_d4 / rmsDIF_norm );
  rmsMOD_a4 = modulator4 * logrmsAVG1 + (1 - modulator4) * rmsAMP_a4;
  rmsMOD_b4 = modulator4 * logrmsAVG2 + (1 - modulator4) * rmsAMP_b4;
  rmsMOD_c4 = modulator4 * logrmsAVG3 + (1 - modulator4) * rmsAMP_c4;
  rmsMOD_d4 = modulator4 * logrmsAVG4 + (1 - modulator4) * rmsAMP_d4;
  if (printrms == true) {
    Serial.print(logrmsAVG1); //a2
    Serial.print(",");
    Serial.print(logrmsAVG2); //a3
    Serial.print(",");
    Serial.print(logrmsAVG3); //a4
    Serial.print(",");
    Serial.println(logrmsAVG4); //a5
  }
  // Avoidig zero-input errors
  if (rmsMOD_a4 < 0.001) {
    rmsMOD_a4 = 0.001;
  }
  if (rmsMOD_b4 < 0.001) {
    rmsMOD_b4 = 0.001;
  }
  if (rmsMOD_c4 < 0.001) {
    rmsMOD_c4 = 0.001;
  }
  if (rmsMOD_d4 < 0.001) {
    rmsMOD_d4 = 0.001;
  }
  if (printnewNormal == true) {
    Serial.print(rmsMOD_a4);
    Serial.print(",");
    Serial.print(rmsMOD_b4);
    Serial.print(",");
    Serial.print(rmsMOD_c4);
    Serial.print(",");
    Serial.println(rmsMOD_d4);
  }
  // Get log of signal
  logrmsMOD_a4 = log(rmsMOD_a4);
  logrmsMOD_b4 = log(rmsMOD_b4);
  logrmsMOD_c4 = log(rmsMOD_c4);
  logrmsMOD_d4 = log(rmsMOD_d4);
  if (logrmsMOD_a4 < -3) {
    logrmsMOD_a4 = -3;
  }
  if (logrmsMOD_b4 < -3) {
    logrmsMOD_b4 = -3;
  }
  if (logrmsMOD_c4 < -3) {
    logrmsMOD_c4 = -3;
  }
  if (logrmsMOD_d4 < -3) {
    logrmsMOD_d4 = -3;
  }
  if (printnewLog == true) {
    Serial.print(logrmsMOD_a4);
    Serial.print(",");
    Serial.print(logrmsMOD_b4);
    Serial.print(",");
    Serial.print(logrmsMOD_c4);
    Serial.print(",");
    Serial.println(logrmsMOD_d4);
  }

  counterArray++;
  if (counterArray >= numWindow) {
    counterArray = 0;
  }
}

// For 3 sensos:
/*
  r3 = sqrt(logrmsAVG2 * logrmsAVG2 + logrmsAVG3 * logrmsAVG3 + logrmsAVG4 * logrmsAVG4);
  a3 = logrmsAVG2 - logrmsAVG3;
  b3 = logrmsAVG3 - logrmsAVG4;
  c3 = logrmsAVG4 - logrmsAVG2;
  d3 = abs(a3) + abs(d3) + abs(c3) + 1;
  pa3 = r3 * (1 + amplifier3 * a3 / d3);
  pb3 = r3 * (1 + amplifier3 * b3 / d3);
  pc3 = r3 * (1 + amplifier3 * c3 / d3);
  modulator3 = 0.8;
  aa3 = modulator3 * logrmsAVG2 + (1-modulator) * pa3;
  bb3 = modulator3 * logrmsAVG3 + (1-modulator) * pb3;
  cc3 = modulator3 * logrmsAVG4 + (1-modulator) * pc3;
*/


/*
  rmsAVG1 = 0.8 * maxi(arrayRMS1) + 0.1 * mini(arrayRMS1) + 0.3 * arrayRMS1[counterArray];
  rmsAVG2 = 0.8 * maxi(arrayRMS2) + 0.2 * arrayRMS2[counterArray];
  rmsAVG3 = 0.8 * maxi(arrayRMS3) + 0.2 * arrayRMS3[counterArray];
*/

/*
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
*/
