#include <math.h>
#include <Servo.h>

Servo legA;  // create servo object to control a servo
Servo legA1;  // create servo object to control a servo
Servo legB;  // create servo object to control a servo
Servo legB1;
// twelve servo objects can be created on most boards

int posA = 0;    // variable to store the servo position
int posA1 = 0; 
int posB = 0;    // variable to store the servo position
int posB1 = 0; 
// Configuration
const float f = 1.0;          // Frequency in Hz
const float A00 = 23*PI/180;         // Amplitude of sine wave 1
const float A11 = 25*PI/180;         // Amplitude of sine wave 2
const float b1 = 33*PI/180;         // Offset for sine wave 1
const float b2 = 55*PI/180;         // Offset for sine wave 2
const float t0_1 = 0.75;       // Phase offset for wave 1 (0)
const float t0_2 = 0.5;      // Phase offset for wave 2 (0.25)
const float t0_3 = 0.25;       // Phase offset for wave 3 (0.5)
const float t0_4 = 0;      // Phase offset for wave 4 (0.75)

// Sampling parameters
const float samplingRate = 100.0; // Samples per second (adjust as needed)
const float deltaT = 1.0 / samplingRate; // Time step between samples

// Internal counter for sample steps
unsigned long stepCounter = 0;

void setup() {
  Serial.begin(9600);
  legA.attach(7);
  legA1.attach(8);
  legB.attach(12);
  legB1.attach(13);
}

void loop() {
  // Calculate "time" based on step counter
  float t = stepCounter * deltaT;

  // Generate sine wave values
  int j1 = (A00 * sin(2 * PI * f * (t - t0_1)) + b1)*57.296;
  int j2 = (A11 * sin(2 * PI * f * (t - t0_2)) + b2)*57.296;
  int j3 = (A00 * sin(2 * PI * f * (t - t0_3)) + b1)*57.296;
  int j4 = (A11 * sin(2 * PI * f * (t - t0_4)) + b2)*57.296;
  posA = j1;
  posA1 = 90-j2;
  posB = 90-j3;
  posB1 = j4;
  legA.write(posA); 
  legB.write(posB); 
  legA1.write(posA1); 
  legB1.write(posB1);
  // Print the sine wave values
  Serial.print(posA);
  Serial.print(",");
  Serial.print(posA1);
  Serial.print(",");
  Serial.print(posB);
  Serial.print(",");
  Serial.println(posB1);

  // Increment the step counter
  stepCounter++;

  // Delay to maintain the sampling rate
  //delay((int)(1000 / samplingRate));
  //delay(10);
}
