#include <AccelStepper.h>
#include <Arduino.h>
#include <Servo.h>

#define dir 2
#define step 3

Servo myservo;
AccelStepper Stepper;

char camera = 'g', camera_ant = 'r';
int passos = 0;
bool sensor_start = 1;

void MoveEsteira(int steps);

void setup() {
  pinMode(step, OUTPUT);
  pinMode(dir, OUTPUT);

  Stepper.setMaxSpeed(1000);   // Velocidade máxima
  Stepper.setAcceleration(50); // Aceleração
  Stepper.setSpeed(200);       // Velocidade regular
  Stepper.moveTo(200);         // Passos que serão movidos
    
  myservo.attach(5);
  myservo.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    camera_ant = camera;
    camera = Serial.read();
  }
  if (sensor_start) {

    MoveEsteira(500);

    delay(50);
  }
  if (camera == 'r') {
    if (camera_ant == 'r') {
      passos = 90;
    } else if (camera_ant == 'g') {
      passos = 0;
      for (passos; passos < 90; passos++) {
        myservo.write(passos);
        delayMicroseconds(10);
      }
    } else if (camera_ant == 'b') {
      passos = 180;
      for (passos; passos > 90; passos--) {
        myservo.write(passos);
        delayMicroseconds(10);
      }
    }

    delay(1000);
    MoveEsteira(4500);
  }
  if (camera == 'g') {
    if (camera_ant == 'g') {
      passos = 0;
    } else if (camera_ant == 'r') {
      for (passos; passos > 0; passos--) {
        myservo.write(passos);
        delayMicroseconds(10);
      }
    } else if (camera_ant == 'b') {
      passos = 180;
      for (passos; passos > 0; passos--) {
        myservo.write(passos);
        delayMicroseconds(10);
      }
    }
    delay(1000);
    MoveEsteira(4500);
  }
  if (camera == 'b') {
    if (camera_ant == 'b') {
      passos = 180;
    } else if (camera_ant == 'r') {
      passos = 90;
      for (passos; passos < 180; passos++) {
        myservo.write(passos);
        delayMicroseconds(10);
      }
    } else if (camera_ant == 'g') {
      passos = 0;
      for (passos; passos < 180; passos++) {
        myservo.write(passos);
        delayMicroseconds(10);
      }
    }
    delay(1000);
    MoveEsteira(4500);
  }
}

void MoveEsteira(int steps) {
  for (unsigned int i = 0; i < steps; i++) {
    Stepper.run();
    delayMicroseconds(20);
  }
}
