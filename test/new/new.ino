/*


#include <SoftwareSerial.h>
#include <math.h>

/*Declare your sensor pins as variables. I'm using Analog In pins 0 and 1. Change the names and numbers as needed
Pro tip: If you're pressed for memory, use #define to declare your sensor pins without using any memory. Just be careful that your pin name shows up NOWHERE ELSE in your sketch!
for more info, see: http://arduino.cc/en/Reference/Define
*/

double maxi(double a[])
{
  double maximum=a[0];
  for (int i=1;i<5;i++)
  {
    if (a[i]>maximum)
    maximum=a[i];
  }
  return maximum;
}
int sensor1Pin = 0;
int sensor2Pin = A2;// sensor 1
int sensor3Pin = A3;// sensor 2

int v=150; //number of samples in a window of (0.1 second)

/*Create an array to store sensor values. I'm using floats. Floats use 4 bytes to represent numbers in exponential notation. Use int if you are representing whole numbers from -32,768 to 32,767.
For more info on the appropriate data type for your sensor values, check out the language reference on data type: http://arduino.cc/en/Reference/HomePage
Customize the array's size to be equal to your number of sensors.
*/
float sensorVal[] = {0,0,0};

/*Pro tip: if you have a larger number of sensors, you can use a for loop to initialize your sensor value array. Here's sample code (assuming you have 6 sensor values):
float sensorVals[6];
int i;
for (i=0; i&lt;6; i++)
{
sensorVals[i] = 0;
}
*/
 int count=0;
 
void setup(){
Serial.begin(9600); //This line tells the Serial port to begin communicating at 9600 bauds
}

//
void loop(){
//read each sensor value. We are assuming analog values. Customize as nessary to read all of your sensor values into the array. Remember to replace "sensor1Pin" and "sensor2Pin" with your actual pin names from above!
//sensorVal[0] = analogRead(sensor1Pin);
//

if(count==600) // loop control for 1 minute of measurement
while(1)
;
count++;
/*If you are reading digital values, use digitalRead() instead. Here's an example:
sensorVal[0] = digitalRead(sensor1Pin);
*/
 double array1[5],array2[5];
  int counter=0,counter2=0;
  double rms1=0.0,rms2=0.0, sum1=0.0,sum2=0.0, val1=0.0,val2=0.0,log_rms1=0.0,log_rms2=0.0,log_rmsa=0.0,log_rmsb=0.0,rms_1=0.0,rms_2=0.0;
//print over the serial line to send to Processing. To work with the processisng sketch we provide, follow this easy convention: separate each sensor value with a comma, and separate each cycle of loop with a newline character.
//Remember to separate each sensor value with a comma. Print every value and comma using Serial.print(), except the last sensor value. For the last sensor value, use Serial.println()
 // Serial.print(400);
 // Serial.print("\t");
 // Serial.print(700);
 // Serial.print("\t");
  //unsigned long elapsed;
  //unsigned long startTime=micros();
  while(counter2<5)
  {
    sum1=0.0;
    sum2=0.0;
    while (counter<v)
    {
     
        sensorVal[1] = analogRead(sensor2Pin);
        sum1 = sum1 + sensorVal[1]*sensorVal[1];
        sensorVal[2] = analogRead(sensor3Pin)  ;
        sum2 = sum2 + sensorVal[2]*sensorVal[2];
    //Serial.print(counter);
    //Serial.print("\t");  
    
        delay(0.5); //total delay of .5 millisecond of 2000 samples a second 
        counter=counter + 1;
    
  }
  counter = 0;
  
  //unsigned long currentTime=micros();
   //  elapsed=currentTime-startTime;
  //Serial.print(elapsed);
 // Serial.print("\t");
  //log_rms1=0.5*(log(sum1)-log(v));
  //log_rms2=0.5*(log(sum2)-log(v));
  val1=sum1/v;
  val2=sum2/v;
  rms1=sqrt(val1);
  rms2=sqrt(val2);
  array1[counter2]=rms1;
  array2[counter2]=rms2;
  //max1=max(array1[counter2],array[counter2-1])
  counter2=counter2+1;

  }

  rms_1=maxi(array1);
  rms_2=maxi(array2);
  
  log_rmsa=log(rms_1);
  log_rmsb=log(rms_2);
  Serial.print(rms_1);
  Serial.print(",");
  Serial.println(rms_2);
  //Serial.print(",");
  //Serial.print(log_rmsa);
  //Serial.print(",");
  //Serial.println(log_rmsb);
  //Serial.print(",");
  //Serial.print(log_rmsa);
  //Serial.print(",");
  //Serial.println(log_rmsb);
  
  //Serial.print("rms value:");
  //Serial.println(rms);
}


