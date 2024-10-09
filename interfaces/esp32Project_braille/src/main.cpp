#include <Arduino.h>                                        // Biblioteca padrao para uso do arduino na IDE PLatformIO
#include "Crc16.h"                                          // Bibliteca para calculo de CRC16
#include "Control.h"                                        // Bibliteca para controle dos acionamentos dos pontos 
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
//String frame_received;                                      // Quadro recebido
String address_received;                                    // Endereco recebido
String function_received;                                   // Funcao recebida
String data_received;                                       // Mensagem recebida
unsigned short data_length;                                 // Tamanho da mensage recebida
unsigned int crc_received;                                  // Crc recebido
bool enable_program;                                        // Flag para controle de fluxo
bool crc_check;                                             // Flag para verificacao do crc
bool trigger_program =            false;                    // Flag para travamento de execucao de programa
bool translation_ok =             false;                    // Flag para controle da traducao
long time_slap =                  500;                      // Tempo de intervalo entre cada troca de caractere             
/*
 * Declaracao escope de funcoes auxiliares
 */
void checkSerial(void);                                     // Funcao para checar o recebimento de dados
void comunication_mode(String mode);                        // Funcao para controle envio/recepcao de dados
void setPinout(void);                                       // Funcao para configuracao do pinMode
void execute_program(void);                                 // Funcao para ececucao das tarefas do Dispositivo
void clearBuffer(void);                                     // Funcao para limar o buffer de entrada do Dispositivo                                                           
void exibe_caractere(void);
void compile_translation(void);
void execute_translation(void);
void change_speed(void);
void obtain_speed(void);

void setup() {
  Serial.begin(9600);                                       // Velocidade de comunicacao
  setPinout();                                              // configuracao do pinMode 
  reset_output();                                           // Zera o buffer para controle dos pontos
  exibe_caractere();                                    // Set de todos pontos abaixados
  comunication_mode("RECEIVE");                             // Habilita a recepcao de dados da interface 
}

void loop() {
  comunication_mode("RECEIVE");                             // Habilita a recepcao de dados da interface 
  checkSerial();
  //delay(200);
  execute_program();
  //delay(200);
}

/* FUNCOES AUXILIARES*/

void checkSerial(void){
  if (Serial.available()) {
    String frame_received = Serial.readStringUntil('\n');          // Obtem o quadro de dados recebido

    if (frame_received.length() > 0) {
      // Separar o frame nas suas partes
      address_received = frame_received.substring(0, 1);    // Endereço
      function_received = frame_received.substring(1, 2);   // Funcao
      String lengthOfData = frame_received.substring(2, 4); // Comprimento dos dados
      data_length = lengthOfData.toInt();                   // Converte comprimento para inteiro
      data_received = frame_received.substring(4, 4 + data_length);                                     // Pega os dados
      String crcReceived = frame_received.substring(4 + data_length);                                   // CRC recebido como string
      crc_received = crcReceived.toInt();                   // Converte o CRC recebido para inteiro
      String crcMessage = address_received + function_received + lengthOfData + data_received;          // Montagem da mensagem recebida
      unsigned short crc_calculated = crc.XModemCrc((byte*)crcMessage.c_str(), 0, crcMessage.length()); // Calculo do CRC 
      crc_check = (crc_calculated == crc_received);         // Verifica o crc recebido e o crc calculado
      enable_program = address_received.equals(String(ADDRESS));                                        // Verifica o endereco para recepcao da mensagem
    }
  }
}

void comunication_mode(String mode){
  delay(200);
  if (mode == "SEND") {
    digitalWrite(SR_COM, HIGH);                             // Habilita o envio de dados para a interface
  }
  else if (mode == "RECEIVE") {                             // Habilita a recepcao de dados da interface
    digitalWrite(SR_COM, LOW);
  }
  delay(200);
}

void setPinout(void){
  for (size_t i = 0; i < 6; i++) {
    pinMode(pins[i], OUTPUT);                               // configuracao do pinMode  do pontos
  }
  pinMode(SR_COM, OUTPUT);
  pinMode(_LED, OUTPUT);
} 

void execute_program(void){
  // Endereco recebido == Endereco do Dispositivo
  clearBuffer();
  if (enable_program) {
    
    // CRC calculado != CRC recebido
    if (!crc_check) {
      comunication_mode("SEND");
      Serial.println("CRC INCORRECT");
      delay(200);
      comunication_mode("RECEIVE");
    }
    // CRC calculado == CRC recebido
    else {

      switch (function_received.charAt(0)) {
        case CODE_TRANSLATE_MESSAGE:
          compile_translation(); 
          break;

        case CODE_EXECUTE_MESSAGE:
          execute_translation(); 
          break;

        case CODE_CHANGE_SPEED:
          change_speed(); 
          break;

        case CODE_CURRENT_SPEED:
          obtain_speed(); 
          break;

        default:
          break;
      }
      function_received = "#";
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

void exibe_caractere(void) {
  
  digitalWrite(POINT_1, output[0]);
  digitalWrite(POINT_2, output[1]);
  digitalWrite(POINT_3, output[2]);
  digitalWrite(POINT_4, output[3]);
  digitalWrite(POINT_5, output[4]);
  digitalWrite(POINT_6, output[5]);
}


void compile_translation(void) {
  if (data_length > 0) {
    comunication_mode("SEND");
    Serial.print("Executing translation...");
    delay(200);
    comunication_mode("RECEIVE");
    for (size_t i = 0; i < data_length; i++) {
      define_caractere(data_received[i]);
    }
    digitalWrite(_LED, HIGH);
    translation_ok = true;
  }
  else {
    comunication_mode("SEND");
    Serial.println("No message found to translation...");
    delay(200);
    comunication_mode("RECEIVE");
    digitalWrite(_LED, LOW);
  }
}
void execute_translation(void) {
  comunication_mode("SEND");
  Serial.println("Executing program :)");
  delay(200);
  comunication_mode("RECEIVE");
  reset_output();
  exibe_caractere();
  for (size_t i = 0; i < data_length; i++) {
    define_caractere(data_received[i]);
    exibe_caractere();
    digitalWrite(_LED, HIGH);
    delay(time_slap);
    reset_output();
    exibe_caractere();
    digitalWrite(_LED, LOW);
    delay(time_slap);
  }
  reset_output();
  exibe_caractere();
  digitalWrite(_LED, LOW);
  translation_ok = false;
}

void change_speed(void) {
  comunication_mode("SEND");
  Serial.print("Change speed ... ");
  Serial.print(time_slap);
  Serial.print(" -->> ");
  Serial.println(data_received);
  delay(200);
  comunication_mode("RECEIVE");
  time_slap = data_received.toInt();
  delay(1000);
  for (size_t i = 0; i < 6; i++) {
    digitalWrite(_LED, !digitalRead(_LED));
    delay(500);
  }
}

void obtain_speed(void) {
  comunication_mode("SEND");
  Serial.print("Getting current speed: ");
  Serial.println(time_slap);
  delay(200);
  comunication_mode("RECEIVE");
}
