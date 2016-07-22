/*
  #include <SoftwareSerial.h>
  #include <math.h>
  For more info, see: http://arduino.cc/en/Reference/Define
*/
// Sensors
#define NUM_SENSORS 4
const int SENSOR_PIN[] = {A2, A3, A4, A5}; // Input pin aliases
const double BIAS_S[] = {1.0, 1.0, 1.0, 1.0}; // Bias for each raw channel

// Array to store input reads from analog
double sensorVal[NUM_SENSORS];
#define DELAY_TIME_ANALOG 0.1 // time delay between analog samples in microseconds

// Windowed Sampling parameters
#define NUM_SAMPLES 150 // number of samples in a window of (0.1 second)
#define AVG_WINDOW_SIZE 50 //
double array_rms_s[NUM_SENSORS][AVG_WINDOW_SIZE];
int counterArray = 0;

// Decaying Max parameters
#define DECAY_MIN 0.001
double decaying_max[] = {DECAY_MIN, DECAY_MIN, DECAY_MIN, DECAY_MIN};
long decay_cnt = 0;
#define DECAY_MAX_CONST 2
#define DECAY_MAX_LIN 0
#define DECAY_MAX_LINLOG 0.15
#define DECAY_MAX_SQ 0
#define DECAY_MAX_ROOT 0
#define DECAY_MAX_LOG 0
#define DECAY_MAX_AMP 0.005

// Averaged window memory shape factors:
#define AVG_MEM_CONST 0
#define AVG_MEM_LIN 1.0
#define AVG_MEM_SQ 1.0
#define AVG_MEM_ROOT 1.0

// Variables for 4 sensor signal manipulation:
#define NEW_DIFF 1
#define AMP_DIFF_OLD 1.0
#define AMP_DIFF_OLD_RADIUS 0.1
#define RMS_AVG_AMP_MOD 0.5

// Print Modes and Parameters
#define PRINT_RMS_RAW 0
#define PRINT_RMS_AVG 0
#define USE_DECAY_MAX 1
#define PRINT_RMS_MAX_DECAY 0
#define PRINT_RMS_DIFF 0
#define PRINT_RMS_MOD 0
#define PRINT_RMS_LOG 1
#define PRINT_NUM_DECIMALS 2
#define PRINT_DELAY 2
#define SEE_WAVEFORM_OLD 0
int PRINT_CHANNEL_S[] = {1, 1, 1, 1};

// Fake Input Parameters
#define FAKE_INPUT true
const double FAKE_BIAS_S[] = {5.0, 3.11, 8.52, 10.71};
const double FAKE_CROSSTALK_S[] = {0.12, 0.1, 0.05, 0.001};
int cntFakeTime = 0;
const double SPEED_ACT_MOD[] = {0.05, 0.056, 0.04, 0.045};
#define SPEED_CNST_HELD 0.08
#define ANGLE_PHASE 0.7
#define ANGLE_PHASE_SLOW 0.001
#define CHANNEL_SWITCH_INTERVAL 200
#define CHANNEL_SWITCHING 1

// Log Output parameters
#define RMS_MOD_MIN_RANGE 0.05 // Keep modulated rms output above this value
#define LOG_MAX_RANGE 6 // Keep log output below this value

void randWave(double a[]) {
  double sqwave_s[NUM_SENSORS];
  long randNoise;
  int channel_ON;
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    randNoise = random(11);
    sqwave_s[sensorNum] = (sensorNum + 1) * ANGLE_PHASE * (1 + randNoise / 50.0);
    randNoise = random(11);
    sqwave_s[sensorNum] = sq(sin(sqwave_s[sensorNum] + SPEED_CNST_HELD * cntFakeTime * (1 + randNoise / 20.0)));
    randNoise = random(11);
    sqwave_s[sensorNum] = (randNoise / 10.0) * sqwave_s[sensorNum];
    randNoise = random(11);
    sqwave_s[sensorNum] = sqwave_s[sensorNum] * FAKE_BIAS_S[sensorNum] * sq(sin(cntFakeTime * (SPEED_ACT_MOD[sensorNum] * (1 + randNoise / 50) + ANGLE_PHASE_SLOW) + sensorNum * ANGLE_PHASE * (1 + randNoise / 60.0)));
  }
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    if (CHANNEL_SWITCHING) {
      if ((((int)((cntFakeTime % (NUM_SENSORS * CHANNEL_SWITCH_INTERVAL)) / (CHANNEL_SWITCH_INTERVAL + 0.0))) % NUM_SENSORS) == sensorNum) {
        channel_ON = 1;
      } else {
        channel_ON = 0;
      }
    } else {
      channel_ON = 1;
    }
    a[sensorNum] = channel_ON * sqwave_s[sensorNum];
    for (int sensorNumOther = 1; sensorNumOther < NUM_SENSORS - 1; sensorNumOther++) {
      a[sensorNum] = a[sensorNum] + FAKE_CROSSTALK_S[sensorNum] * sqwave_s[(sensorNum + sensorNumOther) % NUM_SENSORS];
    }
  }
  cntFakeTime++;
}

void setup() {
  Serial.begin(9600); //This line tells the Serial port to begin communicating at 9600 bauds
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    pinMode(SENSOR_PIN[sensorNum], INPUT);
    digitalWrite(SENSOR_PIN[sensorNum], LOW);
  }
  //randomSeed(SENSOR_PIN[0]);
}

// Takes weighted average, weight shape depending on factors defined at the top
double window_weighted_avg(double a[], int index) {
  double array_weighted_avg = a[index] * (AVG_MEM_CONST + AVG_MEM_ROOT * sqrt(AVG_WINDOW_SIZE) + AVG_MEM_LIN * AVG_WINDOW_SIZE + AVG_MEM_SQ * sq(AVG_WINDOW_SIZE));
  for (int ishift = 1; ishift < AVG_WINDOW_SIZE; ishift++) {
    index = index - 1;
    if (index < 0) {
      index = AVG_WINDOW_SIZE - 1;
    }
    array_weighted_avg = array_weighted_avg + a[index] * (AVG_MEM_CONST + AVG_MEM_ROOT * sqrt(AVG_WINDOW_SIZE - ishift) + AVG_MEM_LIN * (AVG_WINDOW_SIZE - ishift) + AVG_MEM_SQ * sq(AVG_WINDOW_SIZE - ishift));
  }
  array_weighted_avg = array_weighted_avg / (AVG_WINDOW_SIZE * (AVG_MEM_CONST + 0.6 * AVG_MEM_ROOT * sqrt(AVG_WINDOW_SIZE) + 0.5 * AVG_MEM_LIN * AVG_WINDOW_SIZE + 0.3 * AVG_MEM_SQ * sq(AVG_WINDOW_SIZE)));
  return array_weighted_avg;
}

// Returns max value of input array
double array_max(double a[]) {
  double max_value = 0.0;
  for (int i = 0; i < AVG_WINDOW_SIZE; i++) {
    max_value = max(max_value, a[i]);
  }
  return max_value;
}

// Prints data contents of array holding sensor input
void printArray(double a[]) {
  if (SEE_WAVEFORM_OLD) {
    if (NUM_SENSORS > 1) {
      for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
        if (PRINT_CHANNEL_S[sensorNum]) {
          Serial.print(a[sensorNum]);
          delay(PRINT_DELAY);
          Serial.print(" ");
          delay(PRINT_DELAY);
        }
      }
    }
    Serial.println();
    delay(PRINT_DELAY);
  } else {
    String toPrint;
    if (PRINT_CHANNEL_S[0]) {
      toPrint = String(a[0], PRINT_NUM_DECIMALS);
    }

    for (int sensorNum = 1; sensorNum < NUM_SENSORS; sensorNum++) {
      if (PRINT_CHANNEL_S[sensorNum]) {
        /*if (toPrint.length() > 0) {
          toPrint = toPrint + " ";
          }*/
        toPrint = toPrint + " " + String(a[sensorNum], PRINT_NUM_DECIMALS);
      }
    }
    Serial.print(toPrint);
    delay(PRINT_DELAY);
    Serial.println();
    delay(PRINT_DELAY);
  }
}

void loop() {
  // *** Raw RMS Signal ***
  // get rms over a sample window of size NUM_SAMPLES
  double sumSquares_s[NUM_SENSORS];
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    sumSquares_s[sensorNum] = 0.0;
  }
  for (int counterRMS = 0; counterRMS < NUM_SAMPLES; counterRMS++)
  {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      sensorVal[sensorNum] = analogRead(SENSOR_PIN[sensorNum]);
      sumSquares_s[sensorNum] = sumSquares_s[sensorNum] + sq(sensorVal[sensorNum]);
      delay(DELAY_TIME_ANALOG);
    }
  }
  // obtain raw rms
  double rms_raw_s[NUM_SENSORS];
  if (FAKE_INPUT) {
    randWave(rms_raw_s);
  } else {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      rms_raw_s[sensorNum] = BIAS_S[sensorNum] * sqrt(sumSquares_s[sensorNum] / NUM_SAMPLES);
    }
  }
  // print raw rms
  if (PRINT_RMS_RAW) printArray(rms_raw_s);

  // *** Averaged RMS Signal ***
  // obtain weighted rms over a time window of size AVG_WINDOW_SIZE
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    array_rms_s[sensorNum][counterArray] = rms_raw_s[sensorNum];
  }
  double rms_avg_s[NUM_SENSORS];
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    rms_avg_s[sensorNum] = window_weighted_avg(array_rms_s[sensorNum], counterArray);
  }
  // print averaged rms
  if (PRINT_RMS_AVG) printArray(rms_avg_s);

  // *** Manipulating 4-sensor signal ***
  // decaying max
  double decay_rate;
  if (USE_DECAY_MAX) {
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      if (rms_avg_s[sensorNum] > decaying_max[sensorNum]) {
        decaying_max[sensorNum] = rms_avg_s[sensorNum];
        decay_cnt = 0;
      }
      rms_avg_s[sensorNum] = decaying_max[sensorNum];
      decay_rate = DECAY_MAX_CONST +  (DECAY_MAX_LIN + DECAY_MAX_LINLOG * log(decay_cnt + 1)) * decay_cnt + DECAY_MAX_SQ * sq(decay_cnt) +  DECAY_MAX_ROOT * sqrt(decay_cnt) + DECAY_MAX_LOG * log(decay_cnt + 1);
      decay_rate = decay_rate * DECAY_MAX_AMP;
      decaying_max[sensorNum] = decaying_max[sensorNum] * (1.001 - min(decay_rate, 1));
      decaying_max[sensorNum] = max(decaying_max[sensorNum], DECAY_MIN);
    }
    decay_cnt++;
    // print decaying max
    if (PRINT_RMS_MAX_DECAY) printArray(decaying_max);
  }

  // getting and amplifying differences
  double rms_diff_s[NUM_SENSORS];
  double rms_radius_norm = 0.0; // signal strength norm
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    rms_radius_norm = rms_radius_norm + sq(rms_avg_s[sensorNum]);
  }
  rms_radius_norm = sqrt(rms_radius_norm) / NUM_SENSORS;
  if (NEW_DIFF) {
    int rank[NUM_SENSORS] = {1, 1, 1, 1};
    // get rank of signals in terms of size
    for (int sensorNum = 0; sensorNum < NUM_SENSORS - 1; sensorNum++) {
      for (int sensorNumOther = sensorNum + 1; sensorNumOther < NUM_SENSORS; sensorNumOther++) {
        if (rms_avg_s[sensorNum] < rms_avg_s[sensorNumOther]) {
          rank[sensorNumOther] = rank[sensorNumOther] + 1;
        } else {
          rank[sensorNum] = rank[sensorNum] + 1;
        }
      }
    }
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      rms_diff_s[sensorNum] = rms_radius_norm * rms_avg_s[sensorNum] * rank[sensorNum] / NUM_SENSORS;
    }
  } else {
    double rms_diff_norm = 1.0; // signal difference norm
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      for (int sensorNumOther = sensorNum + 1; sensorNumOther < NUM_SENSORS; sensorNumOther++) {
        rms_diff_norm = rms_diff_norm + sq(rms_avg_s[sensorNumOther] - rms_avg_s[sensorNum]);
      }
    }
    rms_diff_norm = sqrt(rms_diff_norm);
    // relative distance of a channel relative to the other's average
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      rms_diff_s[sensorNum] = 4 * rms_avg_s[sensorNum];
      for (int sensorNumOther = 0; sensorNumOther < NUM_SENSORS; sensorNumOther++) {
        rms_diff_s[sensorNum] = rms_diff_s[sensorNum] - rms_avg_s[sensorNumOther];
      }
    }
    // ~sign of distance from avg (& avoiding division by zero):
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      rms_diff_s[sensorNum] = rms_diff_s[sensorNum] / (abs(rms_diff_s[sensorNum]) + 1.0);
    }
    // capture relevant (signed & normalized) radius of distances:
    double rms_diff_shift_norm = 0.0;
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      double square_of_diff_sum = 0.0;
      for (int sensorNumOtherDummy = 1; sensorNumOtherDummy < NUM_SENSORS; sensorNumOtherDummy++) {
        int sensorNumOther = sensorNum + sensorNumOtherDummy;
        if (sensorNumOther >= NUM_SENSORS) sensorNumOther = sensorNumOther - NUM_SENSORS; // correct index overflow
        square_of_diff_sum = square_of_diff_sum + sq(rms_avg_s[sensorNumOther] - rms_avg_s[sensorNum]);
      }
      rms_diff_s[sensorNum] = (rms_diff_s[sensorNum] * sqrt(square_of_diff_sum)) / rms_diff_norm;
      rms_diff_shift_norm = rms_diff_shift_norm + abs(rms_diff_s[sensorNum]);
    }
    for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
      // shift differences relative to norm to make them positive
      rms_diff_s[sensorNum] = rms_diff_s[sensorNum] + rms_diff_shift_norm;
      // amplify original averaged signal with this difference, including a factor for when there is more overall sensor activity
      rms_diff_s[sensorNum] = (1 + rms_radius_norm * AMP_DIFF_OLD_RADIUS) * AMP_DIFF_OLD * rms_diff_s[sensorNum];
    }
  }
  // print differences:
  if (PRINT_RMS_DIFF) printArray(rms_diff_s);

  // Modulate signal between average rms and amplified difference
  double rms_mod_s[NUM_SENSORS];
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    rms_mod_s[sensorNum] = 2 * (RMS_AVG_AMP_MOD * rms_avg_s[sensorNum]  + (1 - RMS_AVG_AMP_MOD) * rms_diff_s[sensorNum]);
  }
  // print them
  if (PRINT_RMS_MOD) printArray(rms_mod_s);

  // take log of signals
  double logrms_mod_s[NUM_SENSORS];
  for (int sensorNum = 0; sensorNum < NUM_SENSORS; sensorNum++) {
    if (rms_mod_s[sensorNum] < RMS_MOD_MIN_RANGE) rms_mod_s[sensorNum] = RMS_MOD_MIN_RANGE; // truncate to avoid zero-input errors
    logrms_mod_s[sensorNum] = log(rms_mod_s[sensorNum]);
    if (logrms_mod_s[sensorNum] > LOG_MAX_RANGE) logrms_mod_s[sensorNum] = LOG_MAX_RANGE; // limit upper range to a fixed number
  }
  // print them
  if (PRINT_RMS_LOG) printArray(logrms_mod_s);

  // increase counter for window
  counterArray++;
  if (counterArray >= AVG_WINDOW_SIZE) {
    counterArray = 0;
  }
}
