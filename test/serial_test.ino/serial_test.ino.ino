void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

#define SENSOR_1_READ 40.1
#define SENSOR_2_READ 5000.1112
#define SENSOR_3_READ 3.14159
#define SENSOR_4_READ 2.71
int counterTime = 0;
#define SPEED_CONSTANT 0.0001
#define ANGLE_PHASE 0.7
#define SEE_WAVEFORM true

void loop() {
  // put your main code here, to run repeatedly:
  double wave1 = sq(sin(SPEED_CONSTANT * counterTime));
  double wave2 = sq(sin(SPEED_CONSTANT * counterTime + ANGLE_PHASE));
  double wave3 = sq(sin(SPEED_CONSTANT * counterTime + 2 * ANGLE_PHASE));
  double wave4 = sq(sin(SPEED_CONSTANT * counterTime + 3 * ANGLE_PHASE));
  double sensorInput1 = SENSOR_1_READ * wave1 + SENSOR_2_READ * wave2 + SENSOR_3_READ * wave3 + SENSOR_4_READ * wave4;
  double sensorInput2 = SENSOR_2_READ * wave1 + SENSOR_3_READ * wave2 + SENSOR_4_READ * wave3 + SENSOR_1_READ * wave4;
  double sensorInput3 = SENSOR_3_READ * wave1 + SENSOR_4_READ * wave2 + SENSOR_1_READ * wave3 + SENSOR_2_READ * wave4;
  double sensorInput4 = SENSOR_4_READ * wave1 + SENSOR_1_READ * wave2 + SENSOR_2_READ * wave3 + SENSOR_3_READ * wave4;

  if (SEE_WAVEFORM) {
    Serial.print(String(sensorInput1, 2));
    Serial.print(",");
    Serial.print(String(sensorInput2, 2));
    Serial.print(",");
    Serial.print(String(sensorInput3, 2));
    Serial.print(",");
    Serial.println(String(sensorInput4, 2));
  } else {
    String toPrint = String(String(sensorInput1, 2) + "," + String(sensorInput2, 2) + "," + String(sensorInput3, 2) + "," + String(sensorInput4, 2));
    Serial.println(toPrint);
  }
  counterTime++;
  if (counterTime > 62830) {
    counterTime = 0;
  }
}
