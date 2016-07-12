/*


  #include <SoftwareSerial.h>
  #include <math.h>

  /*Declare your sensor pins as variables. I'm using Analog In pins 0 and 1. Change the names and numbers as needed
  Pro tip: If you're pressed for memory, use #define to declare your sensor pins without using any memory. Just be careful that your pin name shows up NOWHERE ELSE in your sketch!
  for more info, see: http://arduino.cc/en/Reference/Define
*/
int sensor2Pin = A5;// sensor 1
int sensor3Pin = A4;// sensor 2
int sensor4Pin = A0;// sensor 3
int max1 = 600;
int max2 = 300;


void setup() {

  Serial.begin(9600); //This line tells the Serial port to begin communicating at 9600 bauds
  pinMode(A0, INPUT);
  digitalWrite(A0, LOW);
  pinMode(A4, INPUT);
  digitalWrite(A4, LOW);
  pinMode(A5, INPUT);
  digitalWrite(A5, LOW);
}

int counterArray = 0, counterRMS = 0;
float sensorVal[] = {0, 0, 0};
int numSamples = 150; //number of samples in a window of (0.1 second)
double arrayRMS1[30], arrayRMS2[30], arrayRMS3[30];
int numWindow = 30;

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
  double rmsRAW1 = 0.0, rmsRAW2 = 0.0, rmsRAW3 = 0.0,
         rmsMOD1 = 0.0, rmsMOD2 = 0.0, rmsMOD3 = 0.0,
         logrmsMOD1 = 0.0, logrmsMOD2 = 0.0, logrmsMOD3 = 0.0,
         sumSquares1 = 0.0, sumSquares2 = 0.0, sumSquares3 = 0.0;

  while (counterRMS < numSamples)
  {
    sensorVal[0] = analogRead(sensor2Pin);
    //delay(0.1);
    sensorVal[1] = analogRead(sensor3Pin);
    //delay(0.1);
    sensorVal[2] = analogRead(sensor4Pin);
    //delay(0.1);
    sumSquares1 = sumSquares1 + sensorVal[0] * sensorVal[0];
    sumSquares2 = sumSquares2 + sensorVal[1] * sensorVal[1];
    sumSquares3 = sumSquares3 + sensorVal[2] * sensorVal[2];

    delay(0.5); //total delay of .5 millisecond of 2000 samples a second
    counterRMS = counterRMS + 1;
  }
  counterRMS = 0;

  //unsigned long currentTime=micros();
  //  elapsed=currentTime-startTime;
  rmsRAW1 = sqrt(sumSquares1 / numSamples);
  rmsRAW2 = sqrt(sumSquares2 / numSamples);
  rmsRAW3 = sqrt(sumSquares3 / numSamples);
  arrayRMS1[counterArray] = rmsRAW1;
  arrayRMS2[counterArray] = rmsRAW2;
  arrayRMS3[counterArray] = rmsRAW3;

  //rmsMOD1 = 0.8 * maxi(arrayRMS1) + 0.1 * mini(arrayRMS1) + 0.3 * arrayRMS1[counterArray];
  //rmsMOD2 = 0.8 * maxi(arrayRMS2) + 0.2 * arrayRMS2[counterArray];
  //rmsMOD3 = 0.8 * maxi(arrayRMS3) + 0.2 * arrayRMS3[counterArray];
  rmsMOD1 = avgW(arrayRMS1, counterArray);
  rmsMOD2 = avgW(arrayRMS2, counterArray);
  rmsMOD3 = avgW(arrayRMS3, counterArray);

  //if (rmsMOD2 > max2){
  //  rmsMOD2 = max2;
  //}
  //rmsMOD2 = 2 * rmsMOD2;
  //if (rmsMOD3 > max1){
  //  rmsMOD3 = max1;
  //}
  logrmsMOD1 = log(rmsMOD1);
  logrmsMOD2 = log(rmsMOD2);
  logrmsMOD3 = log(rmsMOD3);
  if (logrmsMOD2 < -1) {
    logrmsMOD2 = -1;
  }
  if (logrmsMOD3 < -1) {
    logrmsMOD3 = -1;
  }
  if (logrmsMOD1 < -1) {
    logrmsMOD1 = -1;
  }
  

  //Serial.print(logrmsMOD1);
  //Serial.print(",");
  Serial.print(logrmsMOD2);
  Serial.print(",");
  Serial.println(logrmsMOD3);
  //Serial.println("\t");
  counterArray++;
  if (counterArray >= numWindow) {
    counterArray = 0;
  }
}


