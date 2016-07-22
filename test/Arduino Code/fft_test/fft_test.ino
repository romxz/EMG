#include <PlainFFT.h>


/* Printing function options */
#define SCL_INDEX 0x00
#define SCL_TIME 0x01
#define SCL_FREQUENCY 0x02
PlainFFT FFT = PlainFFT(); /* Create FFT object */

/* User defined variables */
const uint16_t samples = 128;
uint16_t frequency = 20000;
uint8_t channel = 0;

/* Data vectors */
uint8_t vData[samples];
double vReal[samples];
double vImag[samples];

void setup() {
  /* Initialize serial comm port */
  Serial.begin(9600); //
  /* Set acquisition parameters */
}
#define SCALER 10
void loop() {
  /* Acquire data and store them in a vector of bytes */
  /* Convert 8 bits unsigned data in 32 bits floats */

  for (uint16_t i = 0; i < samples; i++) {
    vReal[i] = SCALER + 2 * SCALER * sin(2 * PI * i / samples) + 3 * SCALER * sin(4 * PI * i / samples) + 4 * SCALER * sin(8 * PI * i / samples) + 5 * SCALER * sin(16 * PI * i / samples) + 6 * SCALER * sin(PI * i / samples);
  }
  /* Weigh data */
  FFT.windowing(vReal, samples);
  /* Compute FFT: vReal and vImag vectors contain the source data
    and will contain the result data on completion of executing the function*/
  FFT.compute(vReal, vImag, samples, FFT_FORWARD);
  /* Compute magnitudes: the resulting data can be read from the vReal vector */
  FFT.complexToMagnitude(vReal, vImag, samples);
  /* Upload frequency spectrum */
  printVector(vReal, (samples >> 1), SCL_FREQUENCY);
  /* Pause */
  Serial.println(-1);
  delay(1000);

}

void printVector(double *vD, uint8_t n, uint8_t scaleType) {
  /* Mulitpurpose printing function */
  double timeInterval = (1.0 / frequency);
  for (uint16_t i = 0; i < n; i++) {
    /* Print abscissa value */
    switch (scaleType) {
        //case SCL_INDEX: Serial.print(i, DEC);   break;
        //case SCL_TIME: Serial.print((i * timeInterval), 6); break;
        //case SCL_FREQUENCY: Serial.print((i / (timeInterval * (samples - 1))), 6); break;
    }
    Serial.print(" ");
    /* Print ordinate value */
    Serial.print(vD[i], 6);
    Serial.println();

  }

  Serial.println();

}

