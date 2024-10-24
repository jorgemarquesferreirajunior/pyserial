#include <AccelStepper.h>
#include <Arduino.h>
#include <Servo.h>

#define dir 2
#define step 3
#define _led 13

Servo myservo;
AccelStepper Stepper;

char camera = 'g', camera_ant = 'r';
int passos = 0;
bool sensor_start = 1;
void blink(int blinks);

void MoveEsteira(int steps);

void setup() {
  Serial.begin(9600);
  pinMode(step, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(_led, OUTPUT);

  Stepper.setMaxSpeed(1000);   // Velocidade máxima
  Stepper.setAcceleration(50); // Aceleração
  Stepper.setSpeed(200);       // Velocidade regular
  Stepper.moveTo(200);         // Passos que serão movidos
    
  myservo.attach(5);
  myservo.write(90);
  digitalWrite(_led, 1);
  delay(2000);
  digitalWrite(_led, 0);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'a') {
      blink(1);
      for (size_t i = 0; i < 90; i++) {
        myservo.write(i);
        delayMicroseconds(100);

      }
    }

    else if (command == 'b') {
      blink(2);
      for (size_t i = 90; i < 180; i++) {
        myservo.write(i);
        delayMicroseconds(100);

      }
    }
    else if (command == 'c') {
      blink(2);
      for (size_t i = 90; i > 0; i--) {
        myservo.write(i);
        delayMicroseconds(100);

      }
    }

  }




  /*
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
  */
}

void MoveEsteira(int steps) {
  for (unsigned int i = 0; i < steps; i++) {
    Stepper.run();
    delayMicroseconds(20);
  }
}

void blink(int blinks) {
  for (size_t i = 0; i < blinks; i++) {
    digitalWrite(_led, 1);
    delay(500);
    digitalWrite(_led, 0);
    delay(500);
    
  }
}
