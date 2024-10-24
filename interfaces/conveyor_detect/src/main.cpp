#include <Arduino.h>
#include "Buttons.h"
#define _led 13
#define RELE 10
#define SAIDA_AZ 4 // PECA AZUL
#define SAIDA_VD 5 // PECA VERDE
#define SAIDA_VM 6 // PECA VERMELHA
#define EN1 2
#define EN2 3
#define SENSOR_INICIO 8

bool flag_run_code = false;

void blink(int pin, int reps, long delay_rep);
void blinkError(int reps, long delay_rep);
void run_motor(int l, int r);
void start_conveyor(void);
void detect_color(void);
void reset_outputs(void);

void setup() {
  Serial.begin(9600);
  pinMode(SENSOR_INICIO, INPUT_PULLUP);
  pinMode(_led, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(RELE, OUTPUT);
  pinMode(SAIDA_AZ, OUTPUT);
  pinMode(SAIDA_VD, OUTPUT);
  pinMode(SAIDA_VM, OUTPUT);
  digitalWrite(RELE, 1);

}
int cont = 0;
void loop(){

  flag_run_code = !digitalRead(SENSOR_INICIO);

  if (flag_run_code) {
    digitalWrite(RELE, 0);
    delay(700);
    digitalWrite(RELE, 1);
    detect_color();
    
  }
 }

void blink(int pin, int reps, long delay_rep) {
  for (size_t i = 0; i < reps; i++) {
    digitalWrite(pin, 1);
    delay(delay_rep/2);
    digitalWrite(pin, 0);
    delay(delay_rep/2);
  }
}
void run_motor(int l, int r) {
  digitalWrite(EN1, l);
  digitalWrite(EN2, r);
}
void start_conveyor(void) {
  flag_run_code = !digitalRead(SENSOR_INICIO);
}
void detect_color(void) {
  Serial.print("detectar\n");
  delay(200);
  if (Serial.available() > 0) {
    String resultado = Serial.readStringUntil('\n');
    if (resultado == "azul") {
      reset_outputs();
      digitalWrite(RELE, 0);
      blink(SAIDA_AZ, 3, 1000);
      delay(1000);
      digitalWrite(RELE, 1);
    }
    else if (resultado == "verde") {
      //run_motor(0,1);
      digitalWrite(RELE, 0);
      blink(SAIDA_VD, 3, 1000);
      delay(1000);
      digitalWrite(RELE, 1);
    }
    else if (resultado == "vermelho") {
      //run_motor(0,1);
      digitalWrite(RELE, 0);
      blink(SAIDA_VM, 3, 1000);
      delay(1000);
      digitalWrite(RELE, 1);
    }
    else {
      blinkError(10, 250);
    }

    delay(1000);
    digitalWrite(RELE, 1);
  }

}
void blinkError(int reps, long delay_rep) {
  reset_outputs();
  for (size_t i = 0; i < reps; i++) {
    digitalWrite(SAIDA_AZ, 1);
    digitalWrite(SAIDA_VD, 1);
    digitalWrite(SAIDA_VM, 1);
    delay(delay_rep);
    digitalWrite(SAIDA_AZ, 0);
    digitalWrite(SAIDA_VD, 0);
    digitalWrite(SAIDA_VM, 0);
    delay(delay_rep);

   
  }
}
void reset_outputs(void) {
  digitalWrite(SAIDA_VD, 0);
  digitalWrite(SAIDA_VM, 0);
  digitalWrite(SAIDA_AZ, 0);
}
