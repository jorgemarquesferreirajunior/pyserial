#include <AccelStepper.h>

// Define pinos para o driver do motor de passo
#define stepPin 5
#define dirPin 2
#define enPin 8

// Cria um objeto AccelStepper
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);

void setup() {
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);  // Habilita o motor

  // Define a velocidade máxima e a aceleração
  stepper.setMaxSpeed(500);  // Velocidade máxima (ajuste para testar)
  stepper.setAcceleration(3000);  // Aceleração (ajuste para testar)
  
  // Define a direção inicial e o número de passos por rotação
  stepper.moveTo(8000);  // Move para 800 passos (ajuste conforme necessário)
}

void loop() {
  // Continua movendo até alcançar a posição alvo
  if (stepper.distanceToGo() == 0) {
    // Inverte a direção do movimento após alcançar o destino
    stepper.moveTo(-stepper.currentPosition());
  }
  
  // Executa o movimento com a aceleração e velocidade configuradas
  stepper.run();
}

