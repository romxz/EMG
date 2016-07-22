/*
  fft_adc_serial.pde
  guest openmusiclabs.com 7.7.14
  example sketch for testing the fft library.
  it takes in data on ADC0 (Analog0) and processes them
  with the fft. the data is sent out over the serial
  port at 115.2kb.
*/

// changesi

#define TAU 3.14
#define FAKE true


#define LIN_OUT 1 // use the log output function
#define FFT_N 256 // set to 256 point fft

#include <FFT.h> // include the library
#define f 32
#define fs 1000

void setup() {
  Serial.begin(9600); // use the serial port
  TIMSK0 = 0; // turn off timer0 for lower jitter
  //ADCSRA = 0xe5; // set the adc to free running mode
  //ADMUX = 0x40; // use adc0
  //DIDR0 = 0x01; // turn off the digital input for adc0
}
void loop() {
  //while (1) { // reduces jitter
  double sum = 0, ksum = 0;
  cli();  // UDRE interrupt slows this way down on arduino1.0
  for (int i = 0 ; i < 2 * FFT_N ; i += 2) { // save 256 samples
    if (FAKE) {
      double wave1 = 100 * sin(2 * PI * f / fs * i / 2) ;//+ 200 * sin(2 * PI * 2 * f / fs * i / 2);
      //Serial.println(wave1);

      int k = (int) wave1 ;
      //Serial.println(k);
      fft_input[i] = k; // put real data into even bins
      fft_input[i + 1] = 0; // set odd bins to 0
    } else {
      while (!(ADCSRA & 0x10)); // wait for adc to be ready
      ADCSRA = 0xf5; // restart adc
      byte m = ADCL; // fetch adc data
      byte j = ADCH;
      int k = (j << 8) | m; // form into an int
      k -= 0x0200; // form into a signed int
      k <<= 6; // form into a 16b signed int
    }

  }
  fft_window(); // window the data for better frequency response
  fft_reorder(); // reorder the data before doing the fft
  fft_run(); // process the data in the fft
  fft_mag_lin(); // take the output of the fft
  sei();
  //Serial.println("start");

  for (byte i = 0 ; i < FFT_N / 2 ; i++) {
    //double wave1 = 100*sin(i);
    //Serial.println(wave1);

    //int k = (int) wave1 ;
    //Serial.print(k);
    //Serial.print(",");
    Serial.println(fft_lin_out[i]);
    sum = sum + fft_lin_out[i];
    ksum = ksum + i * fft_lin_out[i];
    //Serial.print(",");
    //Serial.println(fft_input[2*i]);// send out the data
  }
  double expected = ksum / sum;
  Serial.print("sum = \t");
  Serial.println(expected);
  int frequency = 1000.0 / FFT_N * expected;
  Serial.print("Frequency = \t");
  Serial.println(frequency);

  while (1) {
    ;
  }
}
