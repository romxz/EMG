/*
  #include <SoftwareSerial.h>
  #include <math.h>
  For more info, see: http://arduino.cc/en/Reference/Define
*/
// Number of Sensors (unused atm)
#define SEE_WAVEFORM false
#define NUM_SENSORS 4

// Sensor Pins
#define SENSOR_1_PIN A2
#define SENSOR_2_PIN A3
#define SENSOR_3_PIN A4
#define SENSOR_4_PIN A5

// Array to store input reads from analog
double sensorVal[] = {0, 0, 0, 0};
#define DELAY_TIME_ANALOG 0.1 // time delay between analog samples

// Windowed Sampling parameters
#define NUM_SAMPLES 150 // number of samples in a window of (0.1 second)
#define AVG_WINDOW_SIZE 50 //
double array_rms_s1[AVG_WINDOW_SIZE], array_rms_s2[AVG_WINDOW_SIZE],
       array_rms_s3[AVG_WINDOW_SIZE], array_rms_s4[AVG_WINDOW_SIZE];
int counterArray = 0;

// Bias for each raw channel
#define BIAS_S1 1
#define BIAS_S2 1
#define BIAS_S3 1
#define BIAS_S4 1

// Averaged window memory shape factors:
#define AVG_CONST_FACTOR 0
#define AVG_LIN_FACTOR 1
#define AVG_SQ_FACTOR 0
#define AVG_ROOT_FACTOR 0

// Variables for 4 sensor signal manipulation:
#define AMPLIFY_DIFF 1
#define AMPLIFY_DIFF_RADIUS 0
#define RMS_AVG_AMP_MOD 0.5

// Print Modes
#define PRINT_RMS_RAW false
#define PRINT_RMS_AVG false
#define PRINT_RMS_DIFF false
#define PRINT_RMS_MOD false
#define PRINT_RMS_LOG true

#define log_max_range 6 // Keep log output between -3 and 6

void setup() {
  Serial.begin(9600); //This line tells the Serial port to begin communicating at 9600 bauds
  pinMode(SENSOR_1_PIN, INPUT);
  digitalWrite(SENSOR_1_PIN, LOW);
  pinMode(SENSOR_2_PIN, INPUT);
  digitalWrite(SENSOR_2_PIN, LOW);
  pinMode(SENSOR_3_PIN, INPUT);
  digitalWrite(SENSOR_3_PIN, LOW);
  pinMode(SENSOR_4_PIN, INPUT);
  digitalWrite(SENSOR_4_PIN, LOW);
}

// Takes weighted average, weight shape depending on factors defined at the top
double window_weighted_avg(double a[], int index) {
  double array_weighted_avg = a[index] * (AVG_WINDOW_SIZE + AVG_CONST_FACTOR + AVG_ROOT_FACTOR * sqrt(AVG_WINDOW_SIZE) + AVG_LIN_FACTOR * AVG_WINDOW_SIZE + AVG_SQ_FACTOR * sq(AVG_WINDOW_SIZE));
  for (int ishift = 1; ishift < AVG_WINDOW_SIZE; ishift++) {
    index = index - 1;
    if (index < 0) {
      index = AVG_WINDOW_SIZE - 1;
    }
    array_weighted_avg = array_weighted_avg + a[index] * (AVG_CONST_FACTOR + AVG_ROOT_FACTOR * sqrt(AVG_WINDOW_SIZE - ishift) + AVG_LIN_FACTOR * (AVG_WINDOW_SIZE - ishift) + AVG_SQ_FACTOR * sq(AVG_WINDOW_SIZE - ishift));
  }
  array_weighted_avg = array_weighted_avg / (AVG_WINDOW_SIZE + AVG_CONST_FACTOR + AVG_ROOT_FACTOR * sqrt(AVG_WINDOW_SIZE) + AVG_LIN_FACTOR * AVG_WINDOW_SIZE + AVG_SQ_FACTOR * sq(AVG_WINDOW_SIZE));
  return array_weighted_avg;
}

void loop() {
  // get rms over a sample window of size NUM_SAMPLES
  double sumSquares_s1 = 0.0, sumSquares_s2 = 0.0, sumSquares_s3 = 0.0, sumSquares_s4 = 0.0;
  for (int counterRMS = 0; counterRMS < NUM_SAMPLES; counterRMS++)
  {
    sensorVal[0] = BIAS_S1 * analogRead(SENSOR_1_PIN);
    sumSquares_s1 = sumSquares_s1 + sq(sensorVal[0]);
    delay(DELAY_TIME_ANALOG);
    sensorVal[1] = BIAS_S2 * analogRead(SENSOR_2_PIN);
    sumSquares_s2 = sumSquares_s2 + sq(sensorVal[1]);
    delay(DELAY_TIME_ANALOG);
    sensorVal[2] = BIAS_S3 * analogRead(SENSOR_3_PIN);
    sumSquares_s3 = sumSquares_s3 + sq(sensorVal[2]);
    delay(DELAY_TIME_ANALOG);
    sensorVal[3] = BIAS_S4 * analogRead(SENSOR_4_PIN);
    sumSquares_s4 = sumSquares_s4 + sq(sensorVal[3]);
    delay(DELAY_TIME_ANALOG);
  }
  // obtain raw rms
  double rms_raw_s1 = sqrt(sumSquares_s1 / NUM_SAMPLES);
  double rms_raw_s2 = sqrt(sumSquares_s2 / NUM_SAMPLES);
  double rms_raw_s3 = sqrt(sumSquares_s3 / NUM_SAMPLES);
  double rms_raw_s4 = sqrt(sumSquares_s4 / NUM_SAMPLES);

  // print raw rms
  if (PRINT_RMS_RAW) {
    if (SEE_WAVEFORM) {
      Serial.print(rms_raw_s1);
      Serial.print(",");
      Serial.print(rms_raw_s2);
      Serial.print(",");
      Serial.print(rms_raw_s3);
      Serial.print(",");
      Serial.println(rms_raw_s4);
    } else {
      String toPrint = String(String(rms_raw_s1, 2) + "," + String(rms_raw_s2, 2) + "," + String(rms_raw_s3, 2) + "," + String(rms_raw_s4, 2));
      Serial.println(toPrint);
    }
  }

  // obtain weighted rms over a time window of size AVG_WINDOW_SIZE
  array_rms_s1[counterArray] = rms_raw_s1;
  array_rms_s2[counterArray] = rms_raw_s2;
  array_rms_s3[counterArray] = rms_raw_s3;
  array_rms_s4[counterArray] = rms_raw_s4;
  double rms_avg_s1 = window_weighted_avg(array_rms_s1, counterArray);
  double rms_avg_s2 = window_weighted_avg(array_rms_s2, counterArray);
  double rms_avg_s3 = window_weighted_avg(array_rms_s3, counterArray);
  double rms_avg_s4 = window_weighted_avg(array_rms_s4, counterArray);

  // print averaged rms
  if (PRINT_RMS_AVG) {
    if (SEE_WAVEFORM) {
      Serial.print(rms_avg_s1);
      Serial.print(",");
      Serial.print(rms_avg_s2);
      Serial.print(",");
      Serial.print(rms_avg_s3);
      Serial.print(",");
      Serial.println(rms_avg_s4);
    } else {
      String toPrint = String(String(rms_avg_s1, 2) + "," + String(rms_avg_s2, 2) + "," + String(rms_avg_s3, 2) + "," + String(rms_avg_s4, 2));
      Serial.println(toPrint);
    }
  }

  // *** Manipulating 4-sensor signal ***
  // signal strength and difference norms
  double rms_radius_norm = sqrt(sq(rms_avg_s1) + sq(rms_avg_s2) + sq(rms_avg_s3) + sq(rms_avg_s4));
  double rms_diff_norm = sqrt(sq(rms_avg_s2 - rms_avg_s1) + sq(rms_avg_s3 - rms_avg_s1) + sq(rms_avg_s4 - rms_avg_s1) + sq(rms_avg_s4 - rms_avg_s2) + sq(rms_avg_s3 - rms_avg_s2) + sq(rms_avg_s4 - rms_avg_s3)) + 1;

  // Capture and amplify / manipulate differences between channels:

  // distance from avg:
  double rms_s1_diff = 3 * rms_avg_s1 - rms_avg_s2 + rms_avg_s3 + rms_avg_s4;
  double rms_s2_diff = 3 * rms_avg_s2 - rms_avg_s3 + rms_avg_s4 + rms_avg_s1;
  double rms_s3_diff = 3 * rms_avg_s3 - rms_avg_s4 + rms_avg_s1 + rms_avg_s2;
  double rms_s4_diff = 3 * rms_avg_s4 - rms_avg_s1 + rms_avg_s2 + rms_avg_s3;
  // ~sign of distance from avg (avoiding division by zero):
  rms_s1_diff = rms_s1_diff / (abs(rms_s1_diff) + 1);
  rms_s2_diff = rms_s2_diff / (abs(rms_s2_diff) + 1);
  rms_s3_diff = rms_s3_diff / (abs(rms_s3_diff) + 1);
  rms_s4_diff = rms_s4_diff / (abs(rms_s4_diff) + 1);
  // capture relevant (signed) radius of distance:
  rms_s1_diff = rms_s1_diff * sqrt(sq(rms_avg_s2 - rms_avg_s1) + sq(rms_avg_s3 - rms_avg_s1) + sq(rms_avg_s4 - rms_avg_s1));
  rms_s2_diff = rms_s2_diff * sqrt(sq(rms_avg_s3 - rms_avg_s2) + sq(rms_avg_s4 - rms_avg_s2) + sq(rms_avg_s1 - rms_avg_s2));
  rms_s3_diff = rms_s3_diff * sqrt(sq(rms_avg_s4 - rms_avg_s3) + sq(rms_avg_s1 - rms_avg_s3) + sq(rms_avg_s2 - rms_avg_s3));
  rms_s4_diff = rms_s4_diff * sqrt(sq(rms_avg_s1 - rms_avg_s4) + sq(rms_avg_s2 - rms_avg_s4) + sq(rms_avg_s3 - rms_avg_s4));
  // normalize relative to others:
  rms_s1_diff = rms_s1_diff / rms_diff_norm;
  rms_s2_diff = rms_s2_diff / rms_diff_norm;
  rms_s3_diff = rms_s3_diff / rms_diff_norm;
  rms_s4_diff = rms_s4_diff / rms_diff_norm;
  // shift these differences to make them positive:
  double rms_diff_shift_norm = abs(rms_s1_diff) + abs(rms_s2_diff) + abs(rms_s3_diff) + abs(rms_s4_diff);
  rms_s1_diff = rms_diff_shift_norm + rms_s1_diff;
  rms_s2_diff = rms_diff_shift_norm + rms_s2_diff;
  rms_s3_diff = rms_diff_shift_norm + rms_s3_diff;
  rms_s4_diff = rms_diff_shift_norm + rms_s4_diff;
  // amplify signal with this difference, as well as when there is some overall sensor activity:
  rms_s1_diff = (1 + rms_radius_norm * AMPLIFY_DIFF_RADIUS) * AMPLIFY_DIFF * rms_s1_diff;
  rms_s2_diff = (1 + rms_radius_norm * AMPLIFY_DIFF_RADIUS) * AMPLIFY_DIFF * rms_s2_diff;
  rms_s3_diff = (1 + rms_radius_norm * AMPLIFY_DIFF_RADIUS) * AMPLIFY_DIFF * rms_s3_diff;
  rms_s4_diff = (1 + rms_radius_norm * AMPLIFY_DIFF_RADIUS) * AMPLIFY_DIFF * rms_s4_diff;
  // print them:
  if (PRINT_RMS_DIFF) {
    if (SEE_WAVEFORM) {
      Serial.print(rms_s1_diff); //a2
      Serial.print(",");
      Serial.print(rms_s2_diff); //a3
      Serial.print(",");
      Serial.print(rms_s3_diff); //a4
      Serial.print(",");
      Serial.println(rms_s4_diff); //a5
    } else {
      String toPrint = String(String(rms_s1_diff, 2) + "," + String(rms_s2_diff, 2) + "," + String(rms_s3_diff, 2) + "," + String(rms_s4_diff, 2));
      Serial.println(toPrint);
    }
  }

  // Modulate signal between average rms and amplified difference
  double rms_s1_mod = 2 * (RMS_AVG_AMP_MOD * rms_avg_s1  + (1 - RMS_AVG_AMP_MOD) * rms_s1_diff);
  double rms_s2_mod = 2 * (RMS_AVG_AMP_MOD * rms_avg_s2  + (1 - RMS_AVG_AMP_MOD) * rms_s2_diff);
  double rms_s3_mod = 2 * (RMS_AVG_AMP_MOD * rms_avg_s3  + (1 - RMS_AVG_AMP_MOD) * rms_s3_diff);
  double rms_s4_mod = 2 * (RMS_AVG_AMP_MOD * rms_avg_s4  + (1 - RMS_AVG_AMP_MOD) * rms_s4_diff);
  // print them
  if (PRINT_RMS_MOD) {
    if (SEE_WAVEFORM) {
      Serial.print(rms_s1_mod); //a2
      Serial.print(",");
      Serial.print(rms_s2_mod); //a3
      Serial.print(",");
      Serial.print(rms_s3_mod); //a4
      Serial.print(",");
      Serial.println(rms_s4_mod); //a5
    } else {
      String toPrint = String(String(rms_s1_mod, 2) + "," + String(rms_s2_mod, 2) + "," + String(rms_s3_mod, 2) + "," + String(rms_s4_mod, 2));
      Serial.println(toPrint);
    }
  }

  // take log of signals, making sure to avoid zero-input errors
  if (rms_s1_mod < 0.001) rms_s1_mod = 0.001;
  if (rms_s2_mod < 0.001) rms_s2_mod = 0.001;
  if (rms_s3_mod < 0.001) rms_s3_mod = 0.001;
  if (rms_s4_mod < 0.001) rms_s4_mod = 0.001;
  double logrms_s1_mod = log(rms_s1_mod);
  double logrms_s2_mod = log(rms_s2_mod);
  double logrms_s3_mod = log(rms_s3_mod);
  double logrms_s4_mod = log(rms_s4_mod);
  // limit upper range to a fixed number
  if (logrms_s1_mod > log_max_range) {
    logrms_s1_mod = log_max_range;
  }
  if (logrms_s2_mod > log_max_range) {
    logrms_s2_mod = log_max_range;
  }
  if (logrms_s3_mod > log_max_range) {
    logrms_s3_mod = log_max_range;
  }
  if (logrms_s4_mod > log_max_range) {
    logrms_s4_mod = log_max_range;
  }
  // print them
  if (PRINT_RMS_LOG) {
    if (SEE_WAVEFORM) {
      Serial.print(logrms_s1_mod);
      Serial.print(",");
      Serial.print(logrms_s2_mod);
      Serial.print(",");
      Serial.print(logrms_s3_mod);
      Serial.print(",");
      Serial.println(logrms_s4_mod);
    } else {
      String toPrint = String(String(logrms_s1_mod, 2) + "," + String(logrms_s2_mod, 2) + "," + String(logrms_s3_mod, 2) + "," + String(logrms_s4_mod, 2));
      Serial.println(toPrint);
    }
  }

  // increase counter for window
  counterArray++;
  if (counterArray >= AVG_WINDOW_SIZE) {
    counterArray = 0;
  }
}
