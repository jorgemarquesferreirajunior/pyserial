#include <Arduino.h>

#define stepPin 5 
#define dirPin 2 
#define enPin 8

// Define o tempo de atraso entre os pulsos (em microssegundos)
int delayTime = 500;  // Ajuste este valor para controlar a velocidade do motor

void setup() {
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);  // Habilita o motor
}

void loop() {
  // Define a direção do motor
  digitalWrite(dirPin, HIGH); // Gira o motor em uma direção
  
  // Gira o motor por 800 passos
  for (int x = 0; x < 800; x++) {
    digitalWrite(stepPin, HIGH); 
    delayMicroseconds(delayTime);  // Reduzi o tempo para aumentar a velocidade
    digitalWrite(stepPin, LOW); 
    delayMicroseconds(delayTime);
  }

  // Pequena pausa antes da próxima rotação
  delay(500);  // Diminui o tempo de espera entre as rotações
}

