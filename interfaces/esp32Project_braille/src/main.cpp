#include <Arduino.h>                                        // Biblioteca padrão para uso do Arduino na IDE PlatformIO
#include "Crc16.h"                                          // Biblioteca para cálculo de CRC16
#include "Control.h"                                        // Biblioteca para controle dos acionamentos dos pontos 
#include <DFRobotDFPlayerMini.h>

DFRobotDFPlayerMini player;

#define ADDRESS                   1                         // Endereço padrão para comunicação Interface/Dispositivo
#define LED_BOARD                 2                         // LED indicador do dispositivo
Crc16 crc;                                                  // Instância da classe CRC16

/*
 * Mapeamento de Hardware
 */

#define SR_COM                    5                         // Pino de controle de envio/recepção de dados
#define POINT_1                   13                        // Pino para acionamento do ponto 1 (LED 1)
#define POINT_2                   12                        // Pino para acionamento do ponto 2 (LED 2)
#define POINT_3                   14                        // Pino para acionamento do ponto 3 (LED 3)
#define POINT_4                   17                        // Pino para acionamento do ponto 4 (LED 4)
#define POINT_5                   16                        // Pino para acionamento do ponto 5 (LED 5)
#define POINT_6                   15                        // Pino para acionamento do ponto 6 (LED 6)
#define PIN_MP3_TX 26                                       // Connects to module's RX 
#define PIN_MP3_RX 27                                       // Connects to module's TX 

unsigned short pins[6] = {
  POINT_1,
  POINT_2,
  POINT_3,
  POINT_4,
  POINT_5,
  POINT_6
};                                                          // Lista para controle dos pontos

/*
 * Mapeamento de software/comunicação RS485
 */
#define CODE_TRANSLATE_MESSAGE    'T'                       // Código ASCII para traduzir a mensagem recebida
#define CODE_EXECUTE_MESSAGE      'E'                       // Código ASCII para executar a mensagem recebida 
#define CODE_CHANGE_SPEED         'C'                       // Código ASCII para alterar a velocidade de execução da mensagem
#define CODE_CURRENT_SPEED        'G'                       // Código ASCII para obter a velocidade atual
#define CODE_CURRENT_MESSAGE      'M'                       // Código ASCII para obter a mensagem traduzida

String address_received;                                    // Armazena o endereço recebido
String function_received;                                   // Armazena a função recebida
String data_received;                                       // Armazena os dados recebidos
String data_backup = "ola";                                 // Cópia da mensagem recebida
unsigned short data_length;                                 // Comprimento da mensagem recebida
unsigned int crc_received;                                  // Valor do CRC recebido
bool enable_program;                                        // Flag para controle de fluxo do programa
bool crc_check;                                             // Flag para verificar o CRC
bool trigger_program =            false;                    // Flag para controle da execução do programa
bool translation_ok =             false;                    // Flag que indica se a tradução foi bem-sucedida
long time_slap =                  500;                      // Intervalo entre caracteres durante a exibição

/*
 * Declaração de escopo das funções auxiliares
 */
void checkDFPlayer(void);
void checkSerial(void);                                     // Função para checar recebimento de dados pela serial
void comunication_mode(String mode);                        // Função para alternar entre modos de comunicação
void setPinout(void);                                       // Função para configurar os pinos de saída
void execute_program(void);                                 // Função para executar as tarefas do dispositivo
void clearBuffer(void);                                     // Função para limpar o buffer de entrada serial
void exibe_caractere(void);                                 // Exibe um caractere em Braille
void compile_translation(void);                             // Compila a tradução dos dados recebidos
void execute_translation(void);                             // Executa a tradução já compilada
void change_speed(void);                                    // Altera a velocidade da execução
void obtain_speed(void);                                    // Obtém a velocidade atual
void obtain_message(void);                                  // Obtém a mensagem traduzida atual

void setup() {
  Serial.begin(9600);                                       // Inicializa a comunicação serial com baudrate 9600
  Serial1.begin(9600, SERIAL_8N1, PIN_MP3_RX, PIN_MP3_TX);
  digitalWrite(LED_BOARD, 1);

  setPinout();                                              // Configura os pinos como saídas
  reset_output();                                           // Reseta o estado dos pinos
  exibe_caractere();                                        // Inicializa os pinos em estado baixo (nenhum ponto ativado)
  comunication_mode("RECEIVE");                             // Habilita a recepção de dados da interface
  digitalWrite(LED_BOARD, 1);
  checkDFPlayer();
}

void loop() {
  /*
   * Teste comunicacao serial - controle player
  if (Serial.available() > 0) {
    String buffer = Serial.readStringUntil('\n');
    int buffer_length = buffer.length();
    String data = buffer.substring(0,buffer_length);
    int index = data.toInt();
    player.play(index);
    delay(200);
  }
  */
  comunication_mode("RECEIVE");                             // Habilita a recepção de dados continuamente
  checkSerial();                                            // Verifica se dados foram recebidos
  execute_program();                                        // Executa o programa se os dados forem válidos
}

/* FUNÇÕES AUXILIARES */

void checkSerial(void) {
  if (Serial.available()) {                                 // Se houver dados disponíveis na serial
    String frame_received = Serial.readStringUntil('\n');    // Lê o quadro de dados até encontrar uma nova linha

    if (frame_received.length() > 0) {                      // Se o quadro tiver dados
      // Divide o quadro recebido em partes (endereço, função, dados e CRC)
      address_received = frame_received.substring(0, 1);    // Extrai o endereço
      function_received = frame_received.substring(1, 2);   // Extrai a função
      String lengthOfData = frame_received.substring(2, 4); // Extrai o comprimento dos dados
      data_length = lengthOfData.toInt();                   // Converte o comprimento para inteiro
      data_received = frame_received.substring(4, 4 + data_length);  // Extrai os dados
      String crcReceived = frame_received.substring(4 + data_length); // Extrai o CRC recebido
      crc_received = crcReceived.toInt();                   // Converte o CRC para inteiro

      // Calcula o CRC da mensagem recebida
      String crcMessage = address_received + function_received + lengthOfData + data_received;
      unsigned short crc_calculated = crc.XModemCrc((byte*)crcMessage.c_str(), 0, crcMessage.length());

      // Verifica se o CRC calculado é igual ao recebido
      crc_check = (crc_calculated == crc_received);
      enable_program = address_received.equals(String(ADDRESS));  // Habilita o programa se o endereço for válido
    }
  }
}

void comunication_mode(String mode) {
  delay(200);                                               // Adiciona um pequeno atraso para sincronização
  if (mode == "SEND") {                                     // Se o modo for envio de dados
    digitalWrite(SR_COM, HIGH);                             // Ativa o envio de dados para a interface
  } else if (mode == "RECEIVE") {                           // Se o modo for recepção de dados
    digitalWrite(SR_COM, LOW);                              // Ativa a recepção de dados da interface
  }
  delay(200);                                               // Adiciona um pequeno atraso para estabilização
}

void setPinout(void) {
  for (size_t i = 0; i < 6; i++) {                          // Para cada pino de controle
    pinMode(pins[i], OUTPUT);                               // Configura como saída
  }
  pinMode(SR_COM, OUTPUT);                                  // Configura o pino de controle de comunicação como saída
  //pinMode(TX_1, OUTPUT);                                  // Configura o pino de controle de comunicação como saída
  //pinMode(RX_1, OUTPUT);                                  // Configura o pino de controle de comunicação como saída
  pinMode(LED_BOARD, OUTPUT);                                    // Configura o pino do LED indicador como saída
}

void execute_program(void) {
  clearBuffer();                                            // Limpa o buffer de entrada serial
  if (enable_program) {                                     // Se o programa está habilitado para execução
    if (!crc_check) {                                       // Se o CRC não é válido
      comunication_mode("SEND");                            // Alterna para modo de envio
      Serial.println("CRC INCORRECT");                      // Envia uma mensagem de erro
      delay(200);
      comunication_mode("RECEIVE");                         // Retorna ao modo de recepção
    } else {                                                // Se o CRC é válido
      // Verifica qual função foi recebida e chama a função correspondente
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
        case CODE_CURRENT_MESSAGE:
          obtain_message();
        default:
          break;
      }
      function_received = "#";                              // Reseta a função recebida após o processamento
    }
  } else {
    comunication_mode("SEND");                              // Alterna para modo de envio
    Serial.println("ADDRESS NOT FOUND!");                   // Envia mensagem de erro caso o endereço não seja encontrado
    delay(200);
    comunication_mode("RECEIVE");                           // Retorna ao modo de recepção
  }
}

void clearBuffer(void) {
  while (Serial.available() > 0) {                          // Enquanto houver dados no buffer
    Serial.read();                                          // Lê e descarta os dados (limpa o buffer)
  }
}

void exibe_caractere(void) {
  // Exibe o caractere traduzido nos pontos de Braille
  digitalWrite(POINT_1, output[0]);
  digitalWrite(POINT_2, output[1]);
  digitalWrite(POINT_3, output[2]);
  digitalWrite(POINT_4, output[3]);
  digitalWrite(POINT_5, output[4]);
  digitalWrite(POINT_6, output[5]);
}

void compile_translation(void) {
  if (data_length > 0) {
    comunication_mode("SEND");                             // Configura para enviar dados pela serial
    Serial.print("Executing translation...");              // Exibe mensagem indicando execução da tradução
    delay(200);                                            // Pequena pausa para garantir sincronização
    comunication_mode("RECEIVE");                          // Volta a receber dados pela serial
    data_backup = data_received;                           // Armazena a mensagem recebida para futuras execuções
  }
  else {                                                   // Caso não tenha mensagem a ser traduzida
    comunication_mode("SEND");                             // Configura para enviar dados pela serial
    Serial.println("No message found to translation...");  // Exibe mensagem de erro
    delay(200);                                            // Pequena pausa para garantir sincronização
    comunication_mode("RECEIVE");                          // Volta a receber dados pela serial
    digitalWrite(LED_BOARD, LOW);                               // Desativa o LED de status
  }
}

void execute_translation(void) {
  comunication_mode("SEND");                               // Configura para enviar dados pela serial
  Serial.println("Executing program :)");                  // Exibe mensagem indicando início da execução do programa
  delay(200);                                              // Pequena pausa para garantir sincronização
  comunication_mode("RECEIVE");                            // Volta a receber dados pela serial
  reset_output();                                          // Reseta os pinos de controle (desativa todos os pontos do caractere)
  exibe_caractere();                                       // Exibe o caractere atual

  // Percorre cada caractere armazenado na mensagem recebida
  for (size_t i = 0; i < data_backup.length(); i++) {
    define_caractere(data_backup[i]);                      // Define o padrão dos pontos para o caractere atual
    exibe_caractere();                                     // Atualiza a exibição do caractere
    player.play(data_backup[i] - 96);
    digitalWrite(LED_BOARD, HIGH);                              // Ativa o LED de status durante a execução
    delay(time_slap);                                      // Pausa entre cada caractere
    player.pause();
    reset_output();                                        // Reseta os pontos
    exibe_caractere();                                     // Atualiza para não mostrar nenhum ponto ativo
    digitalWrite(LED_BOARD, LOW);                               // Desativa o LED de status
    delay(time_slap);                                      // Pausa antes de passar para o próximo caractere
  }
  reset_output();                                          // Reseta todos os pontos ao final da execução
  exibe_caractere();                                       // Atualiza para não mostrar nenhum ponto ativo
  digitalWrite(LED_BOARD, LOW);                                 // Garante que o LED de status está desativado
  translation_ok = false;                                  // Reseta o flag de tradução bem-sucedida
}

void change_speed(void) {
  comunication_mode("SEND");                               // Configura para enviar dados pela serial
  Serial.print("Change speed ... ");                       // Exibe mensagem indicando alteração da velocidade
  Serial.print(time_slap);                                 // Exibe a velocidade atual
  Serial.print(" -->> ");                                  // Exibe seta para indicar alteração
  Serial.println(data_received);                           // Exibe a nova velocidade recebida
  delay(200);                                              // Pausa para garantir a sincronização
  comunication_mode("RECEIVE");                            // Volta a receber dados pela serial
  time_slap = data_received.toInt();                       // Converte e armazena o novo tempo de intervalo
  delay(1000);                                             // Pausa antes de executar o próximo bloco

  // Faz o LED piscar 6 vezes para indicar a mudança de velocidade
  for (size_t i = 0; i < 6; i++) {
    digitalWrite(LED_BOARD, !digitalRead(LED_BOARD));                // Alterna o estado do LED (pisca)
    delay(500);                                            // Pausa entre piscadas
  }
}

void obtain_speed(void) {
  comunication_mode("SEND");                               // Configura para enviar dados pela serial
  Serial.print("Getting current speed: ");                 // Exibe mensagem de obtenção da velocidade
  Serial.println(time_slap);                               // Exibe a velocidade atual
  delay(200);                                              // Pausa para garantir a sincronização
  comunication_mode("RECEIVE");                            // Volta a receber dados pela serial
}

void obtain_message(void) {
  comunication_mode("SEND");                               // Configura para enviar dados pela serial
  Serial.print("Current message translated: ");            // Exibe mensagem indicando a mensagem atual traduzida
  Serial.println(data_backup);                             // Exibe a mensagem traduzida armazenada
  delay(200);                                              // Pausa para garantir a sincronização
  comunication_mode("RECEIVE");                            // Volta a receber dados pela serial
}

void checkDFPlayer(void) {

  // Start communication with DFPlayer Mini
  if (!player.begin(Serial1)) {
    //Serial.println("Connecting to DFPlayer Mini failed!");
    while (true);
  } 
  else {
    digitalWrite(LED_BOARD, 0);
    //Serial.println("Connection OK");

    // Set volume to maximum (0 to 30).
    player.volume(30);
    // Play the first MP3 file on the SD card
    player.play(1);
  } 
}
