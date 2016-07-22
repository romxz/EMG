#include <ffft.h>
#include <suart.h>

#include <stdio.h>
#include <math.h>
#define SIN_2PI_16 0.38268343236508978
#define SIN_4PI_16 0.707106781186547460
#define SIN_6PI_16 0.923879532511286740
#define C_P_S_2PI_16 1.30656296487637660
#define C_M_S_2PI_16 0.54119610014619690
#define C_P_S_6PI_16 1.3065629648763766
#define C_M_S_6PI_16 -0.54119610014619690

void R16SRFFT(float input[16], float output[16] ) {
  float temp, out0, out1, out2, out3, out4, out5, out6, out7, out8;
  float out9, out10, out11, out12, out13, out14, out15;

  out0 = input[0] + input[8]; /* output[0 through 7] is the data that we */
  out1 = input[1] + input[9]; /* take the 8 point real FFT of. */
  out2 = input[2] + input[10];
  out3 = input[3] + input[11];
  out4 = input[4] + input[12];
  out5 = input[5] + input[13];
  out6 = input[6] + input[14];
  out7 = input[7] + input[15];



  out8 = input[0] - input[8]; /* inputs 8,9,10,11 are */
  out9 = input[1] - input[9]; /* the Real part of the */
  out10 = input[2] - input[10]; /* 4 point Complex FFT inputs.*/
  out11 = input[3] - input[11];
  out12 = input[12] - input[4]; /* outputs 12,13,14,15 are */
  out13 = input[13] - input[5]; /* the Imaginary pars of  */
  out14 = input[14] - input[6]; /* the 4 point Complex FFT inputs.*/
  out15 = input[15] - input[7];

  /*First we do the "twiddle factor" multiplies for the 4 point CFFT */
  /*Note that we use the following handy trick for doing a complex */
  /*multiply:  (e+jf)=(a+jb)*(c+jd) */
  /*   e=(a-b)*d + a*(c-d)   and    f=(a-b)*d + b*(c+d)  */

  /* C_M_S_2PI/16=cos(2pi/16)-sin(2pi/16) when replaced by macroexpansion */
  /* C_P_S_2PI/16=cos(2pi/16)+sin(2pi/16) when replaced by macroexpansion */
  /* (SIN_2PI_16)=sin(2pi/16) when replaced by macroexpansion */

  temp = (out13 - out9) * (SIN_2PI_16);
  out9 = out9 * (C_P_S_2PI_16) + temp;
  out13 = out13 * (C_M_S_2PI_16) + temp;

  out14 *= (SIN_4PI_16);
  out10 *= (SIN_4PI_16);
  out14 = out14 - out10;
  out10 = out14 + out10 + out10;

  temp = (out15 - out11) * (SIN_6PI_16);
  out11 = out11 * (C_P_S_6PI_16) + temp;
  out15 = out15 * (C_M_S_6PI_16) + temp;

  /* The following are the first set of two point butterfiles */
  /* for the 4 point CFFT */

  out8 += out10;
  out10 = out8 - out10 - out10;

  out12 += out14;
  out14 = out12 - out14 - out14;

  out9 += out11;
  out11 = out9 - out11 - out11;

  out13 += out15;
  out15 = out13 - out15 - out15;

  /*The followin are the final set of two point butterflies */
  output[1] = out8 + out9;
  output[7] = out8 - out9;

  output[9] = out12 + out13;
  output[15] = out13 - out12;

  output[5] = out10 + out15;    /* implicit multiplies by */
  output[13] = out14 - out11;    /* a twiddle factor of -j */
  output[3] = out10 - out15; /* implicit multiplies by */
  output[11] = -out14 - out11; /* a twiddle factor of -j */


  /* What follows is the 8-point FFT of points output[0-7] */
  /* This 8-point FFT is basically a Decimation in Frequency FFT */
  /* where we take advantage of the fact that the initial data is real*/

  /* First set of 2-point butterflies */

  out0 = out0 + out4;
  out4 = out0 - out4 - out4;
  out1 = out1 + out5;
  out5 = out1 - out5 - out5;
  out2 += out6;
  out6 = out2 - out6 - out6;
  out3 += out7;
  out7 = out3 - out7 - out7;

  /* Computations to find X[0], X[4], X[6] */

  output[0] = out0 + out2;
  output[4] = out0 - out2;
  out1 += out3;
  output[12] = out3 + out3 - out1;

  output[0] += out1; /* Real Part of X[0] */
  output[8] = output[0] - out1 - out1; /*Real Part of X[4] */
  /* out2 = Real Part of X[6] */
  /* out3 = Imag Part of X[6] */

  /* Computations to find X[5], X[7] */

  out5 *= SIN_4PI_16;
  out7 *= SIN_4PI_16;
  out5 = out5 - out7;
  out7 = out5 + out7 + out7;

  output[14] = out6 - out7; /* Imag Part of X[5] */
  output[2] = out5 + out4; /* Real Part of X[7] */
  output[6] = out4 - out5; /*Real Part of X[5] */
  output[10] = -out7 - out6; /* Imag Part of X[7] */

}

float sqrtsqr(float a, float b)
{
  return (sqrt(a * a + b * b));
}

/*
  void main() {
  float data[16];
  float output[16];
  float zero=0;

  printf("\ntype 16 point input vector\n");
  scanf("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f",&data[0],&data[1],&data[2],&data[3],&data[4],&data[5],&data[6],&data[7],&data[8],&data[9],&data[10],&data[11],&data[12],&data[13],&data[14],&data[15]);

  R16SRFFT(data,output);
  printf("\nresult is:\n");
  printf("k,\t\tReal Part\t\tImaginary Part\n");
    printf("0\t\t%.9f\t\t%.9f\t\t%.9f\n",output[0],zero, sqrtsqr(output[0],zero));
  printf("1\t\t%.9f\t\t%.9f\t\t%.9f\n",output[1],output[9],sqrtsqr(output[1],output[9]));
  printf("2\t\t%.9f\t\t%.9f\t\t%.9f\n",output[2],output[10],sqrtsqr(output[2],output[10]));
  printf("3\t\t%.9f\t\t%.9f\t\t%.9f\n",output[3],output[11],sqrtsqr(output[3],output[11]));
  printf("4\t\t%.9f\t\t%.9f\t\t%.9f\n",output[4],output[12],sqrtsqr(output[4],output[12]));
  printf("5\t\t%.9f\t\t%.9f\t\t%.9f\n",output[5],output[13],sqrtsqr(output[5],output[13]));
  printf("6\t\t%.9f\t\t%.9f\t\t%.9f\n",output[6],output[14],sqrtsqr(output[6],output[14]));
  printf("7\t\t%.9f\t\t%.9f\t\t%.9f\n",output[7],output[15],sqrtsqr(output[7],output[15]));
  printf("8\t\t%.9f\t\t%.9f\t\t%.9f\n",output[8],zero, sqrtsqr(output[8],zero));
  printf("9\t\t%.9f\t\t%.9f\t\t%.9f\n",output[7],-output[15],sqrtsqr(output[7],output[15]));
  printf("10\t\t%.9f\t\t%.9f\t\t%.9f\n",output[6],-output[14],sqrtsqr(output[6],output[14]));
  printf("11\t\t%.9f\t\t%.9f\t\t%.9f\n",output[5],-output[13],sqrtsqr(output[5],output[13]));
  printf("12\t\t%.9f\t\t%.9f\t\t%.9f\n",output[4],-output[12],sqrtsqr(output[4],output[12]));
  printf("13\t\t%.9f\t\t%.9f\t\t%.9f\n",output[3],-output[11],sqrtsqr(output[3],output[11]));
  printf("14\t\t%.9f\t\t%.9f\t\t%.9f\n",output[2],-output[9],sqrtsqr(output[2],output[9]));
  printf("15\t\t%.9f\t\t%.9f\t\t%.9f\n",output[1],-output[8],sqrtsqr(output[1],output[8]));
  }
*/

float data[16];
float output[16];
float zero = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

#define PRINT_DELAY 50

int x = 0;
void loop() {
  // put your main code here, to run repeatedly:
  //double y = sin(2*x+180)+sin(3*x+15)+2*sin(10*x+50)+sin(86*x+16) + sin(9*x+150)+sin(4*x+30);
  //float y = sin(2 * PI * x / 4) + sin(2 * PI * x / 8) + sin(2 * PI * x / 16) + sin(2 * PI * x / 32) + sin(2 * PI * x / 64);
  float y = 3 + sin(2 * PI * (x + 1) / 16) + 2 * sin(2 * PI * 2 * (x + 1) / 16) + 0.5 * sin(2 * PI * 3 * (x + 1) / 16) + sin(2 * PI * 4 * (x + 1) / 16);
  y = y + 0.25 * sin(2 * PI * 5 * (x + 1) / 16) + 2 * sin(2 * PI * 6 * (x + 1) / 16) + sin(2 * PI * 7 * (x + 1) / 16) + 3 * sin(2 * PI * 8 * (x + 1) / 16);
  //Serial.println(y);
  //Serial.print(",");
  data[x % 16] = y;
  if (x >= 15)
  {
    R16SRFFT(data, output);
    for (int j = 1; j <= 10; j++)
    {

      Serial.println(sqrtsqr(output[0], zero));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[1], output[9]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[2], output[10]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[3], output[11]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[4], output[12]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[5], output[13]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[6], output[14]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[7], output[15]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[8], zero));
      delay(PRINT_DELAY);
      /*
        Serial.println(sqrtsqr(output[8], zero));
        delay(PRINT_DELAY);
        Serial.println(sqrtsqr(output[8], zero));
        delay(PRINT_DELAY);
        Serial.println(sqrtsqr(output[8], zero));
        delay(PRINT_DELAY);*/

      Serial.println(sqrtsqr(output[7], output[15]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[6], output[14]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[5], output[13]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[4], output[12]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[3], output[11]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[2], output[10]));
      delay(PRINT_DELAY);
      Serial.println(sqrtsqr(output[1], output[9]));
      delay(PRINT_DELAY);

      Serial.println(-5);
      delay(10 * PRINT_DELAY);
    }

  }
  if (x == 15)
  {
    x = 0;
  }
  else
  {
    x += 1;
  }
  //x += 1;

}
