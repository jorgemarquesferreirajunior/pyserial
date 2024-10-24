#include <AccelStepper.h>
#include <Arduino.h>
/*
#define dir 2
#define step 3
#define motorInterfaceType 1 
*/
AccelStepper Stepper(1,3,2);

int passos = 0;
bool sensor_start = 1;

void MoveEsteira(int steps);

void setup() {
  pinMode(step, OUTPUT);
  pinMode(dir, OUTPUT);

  Stepper.setMaxSpeed(1000);   // Velocidade máxima
  Stepper.setAcceleration(50); // Aceleração
  Stepper.setSpeed(500);       // Velocidade regular
  //Stepper.moveTo(200);         // Passos que serão movidos
    
}

void loop() {
  Stepper.run();
  delay(1000);
}
/*
void MoveEsteira(int steps) {
  for (unsigned int i = 0; i < steps; i++) {
    Stepper.run();
    delayMicroseconds(20);
  }
}
*/
