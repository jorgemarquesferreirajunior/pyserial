#include <Arduino.h>                                        // Biblioteca padrao para uso do arduino na IDE PLatformIO
#include "Crc16.h"                                          // Bibliteca para calculo de CRC16
#define ADDRESS                   1                         // Endereco padrao para comunicacao Interface/Dispositivo
#define _LED                      2                         // Led indicador do Dispositivo 
Crc16 crc;                                                  // Instância da classe CRC16

/*                                                            
 * Mapeamento de Hardware
*/

#define SR_COM                    5                         // Pino de controle envio/recepcao de dados
#define POINT_1                   13                        // Pino acionamento ponto 1 (led 1)
#define POINT_2                   12                        // Pino acionamento ponto 2 (led 2)
#define POINT_3                   14                        // Pino acionamento ponto 3 (led 3)
#define POINT_4                   27                        // Pino acionamento ponto 4 (led 4)
#define POINT_5                   26                        // Pino acionamento ponto 5 (led 5)
#define POINT_6                   25                        // Pino acionamento ponto 6 (led 6)
unsigned short pins[6] = {
  POINT_1,
  POINT_2,
  POINT_3,
  POINT_4,
  POINT_5,
  POINT_6
};                                                          // Lista para coontrole dos pontos

/*
 * Mapeamento de software/comunicacao rs 485
*/
#define CODE_TRANSLATE_MESSAGE    'T'                       // Codigo ASCII para traduzir a mensagem recebida 
#define CODE_EXECUTE_MESSAGE      'E'                       // Codigo ASCII para executar a mensagem recebida 
#define CODE_CHANGE_SPEED         'C'                       // Codigo ASCII para alterar a velocidade de execucao da mensagem
#define CODE_CURRENT_SPEED        'G'                       // Codigo ASCII para obter a velocidade atual de execucao da mensagem
String frame_received;                                      // Quadro recebido
String address_received;                                    // Endereco recebido
String function_received;                                   // Funcao recebida
String data_received;                                       // Mensagem recebida
unsigned short data_length;                                 // Tamanho da mensage recebida
unsigned int crc_received;                                  // Crc recebido
bool enable_program;                                        // Flag para controle de fluxo
bool crc_check;                                             // Flag para verificacao do crc
/*
 * Declaracao escope de funcoes auxiliares
 */
void checkSerial(void);                                     // Funcao para checar o recebimento de dados
void comunication_mode(String mode);                        // Funcao para controle envio/recepcao de dados
void setPinout(void);                                       // Funcao para configuracao do pinMode
void execute_program(void);                                 // Funcao para ececucao das tarefas do Dispositivo
void clearBuffer(void);                                     // Funcao para limar o buffer de entrada do Dispositivo                                                           
void setup() {
  Serial.begin(9600);                                       // Velocidade de comunicacao
  clearBuffer();                                            // Limpa o buffer de dados do Dispositivo
  setPinout();                                              // configuracao do pinMode 
  comunication_mode("RECEIVE");                             // Habilita a recepcao de dados da interface 
}

void loop() {
  checkSerial();
  execute_program();
}

/* FUNCOES AUXILIARES*/

void checkSerial(void){
  if (Serial.available()) {
    frame_received = Serial.readStringUntil('\n');          // Obtem o quadro de dados recebido

    if (frame_received.length() > 0) {
      // Separar o frame nas suas partes
      address_received = frame_received.substring(0, 1);    // Endereço
      function_received = frame_received.substring(1, 2);   // Funcao
      String lengthOfData = frame_received.substring(2, 3); // Comprimento dos dados
      data_length = lengthOfData.toInt();                   // Converte comprimento para inteiro
      data_received = frame_received.substring(3, 3 + data_length);                                     // Pega os dados
      String crcReceived = frame_received.substring(3 + data_length);                                   // CRC recebido como string
      crc_received = crcReceived.toInt();                   // Converte o CRC recebido para inteiro
      String crcMessage = address_received + function_received + lengthOfData + data_received;          // Montagem da mensagem recebida
      unsigned short crc_calculated = crc.XModemCrc((byte*)crcMessage.c_str(), 0, crcMessage.length()); // Calculo do CRC 
      
      crc_check = (crc_calculated == crc_received);         // Verifica o crc recebido e o crc calculado
      enable_program = address_received.equals(String(ADDRESS));                                        // Verifica o endereco para recepcao da mensagem
      
    }
  }
}

void comunication_mode(String mode){
  if (mode == "SEND") {
    digitalWrite(SR_COM, HIGH);                             // Habilita o envio de dados para a interface
  }
  else if (mode == "RECEIVE") {                             // Habilita a recepcao de dados da interface
    digitalWrite(SR_COM, LOW);
  }
}

void setPinout(void){
  for (size_t i = 0; i < 6; i++) {
    pinMode(pins[i], OUTPUT);                               // configuracao do pinMode  do pontos
  }
  pinMode(SR_COM, OUTPUT);
  pinMode(_LED, OUTPUT);
} 

void execute_program(void){
  if (enable_program) {
    comunication_mode("SEND");
    if (!crc_check) {
      Serial.println("CRC INCORRECT");
      delay(200);
      comunication_mode("RECEIVE");
    }
    else {
      if (function_received.equals(String(CODE_TRANSLATE_MESSAGE))) {
        digitalWrite(_LED, HIGH);
      }
      else if (function_received.equals(String(CODE_EXECUTE_MESSAGE))) {
        digitalWrite(_LED, LOW);
      }
      else if (function_received.equals(String(CODE_CHANGE_SPEED))) {
        digitalWrite(_LED, LOW);
        delay(1000);
        for (size_t i = 0; i < 6; i++) {
          digitalWrite(_LED, !digitalRead(_LED));
          delay(500);
        }
      }
      else if (function_received.equals(String(CODE_CURRENT_SPEED))) {
        digitalWrite(_LED, LOW);
        delay(1000);
        for (size_t i = 0; i < 6; i++) {
          digitalWrite(_LED, !digitalRead(_LED));
          delay(250);
        }
      }
    }
  }
  else {
    comunication_mode("SEND");
    Serial.println("ADDRESS NOT FOUND!");                   // Retorna mensagem indicando erro de endereco para comunicaco de dados
    delay(200);
    comunication_mode("RECEIVE");
  }
}                               

void clearBuffer(void){
  while (Serial.available() > 0) {
    Serial.read();
  }
}
