#include <Arduino.h>                                        // Biblioteca padrao para uso do arduino na IDE PLatformIO
#include <Crc16.h> >                                        // Bibliteca para calculo de CRC16
#define ADDRESS                   '1'                       // Endereco padrao para comunicacao Interface/Dispositivo
Crc16                             crc16;                    // Instância da classe CRC16
                                                            
 * Mapeamento de Hardware
*/
#define SR_COM                    5                         // Pino de controle envio/recepcao de dados
#define POINT_1                   13                        // Pino acionamento ponto 1 (led 1)
#define POINT_2                   12                        // Pino acionamento ponto 2 (led 2)
#define POINT_3                   14                        // Pino acionamento ponto 3 (led 3)
#define POINT_4                   27                        // Pino acionamento ponto 4 (led 4)
#define POINT_5                   26                        // Pino acionamento ponto 5 (led 5)
#define POINT_6                   25                        // Pino acionamento ponto 6 (led 6)
unsigned short pins[7] = {
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
bool enable_program                                         // FLag para controle de fluxo

/*
 * Declaracao escope de funcoes auxiliares
 */
void checkSerial(void);                                     // Funcao para checar o recebimento de dados
void comunication_mode(String mode);                        // Funcao para controle envio/recepcao de dados
void setPinout(void);                                       // Funcao para configuracao do pinMode

void setup() {
  Serial.begin(9600);                                       // Velocidade de comunicacao
  Serial.flush();                                           // Limpa o buffer de dados do Dispositivo
  setPinout();                                              // configuracao do pinMode 
}

void loop() {

  if (Serial.available()) {
    String frame = Serial.readStringUntil('\n');  // Lê até nova linha ou fim de string

    if (frame.length() > 0) {
      // Separar o frame nas suas partes
      String address = frame.substring(0, 1);       // Endereço
      String func = frame.substring(1, 2);          // Funcao
      String lengthOfData = frame.substring(2, 3);  // Comprimento dos dados
      int dataLength = lengthOfData.toInt();        // Converte comprimento para inteiro

      String data = frame.substring(3, 3 + dataLength);  // Pega os dados
      String crcReceived = frame.substring(3 + dataLength);  // CRC recebido como string
      int crcSent = crcReceived.toInt();  // Converte o CRC recebido para inteiro

      /*
      // Mostrar informações na serial
      Serial.print("Endereço: ");
      Serial.println(address);
      Serial.print("Tamanho dos dados: ");
      Serial.println(dataLength);
      Serial.print("Dados: ");
      Serial.println(data);
      Serial.print("CRC recebido: ");
      Serial.println(crcSent);

    
      // Calcular o CRC16 sobre os dados recebidos
      crc16.clearCrc();  // Limpa o valor anterior do CRC
      for (int i = 0; i < dataLength; i++) {
        crc16.updateCrc(data[i]);  // Atualiza o CRC com cada byte de dados
      }
      unsigned short crcCalculated = crc16.getCrc();  // Obtém o CRC calculado
      */
      //unsigned short crcCalculated = crc16.XModemCrc((byte*)data.c_str(), 0, dataLength);
        

      // Calcular o CRC16 sobre o frame completo (endereço + tamanho dos dados + dados)
      String crcMessage = address + func + lengthOfData + data;
      unsigned short crcCalculated = crc16.XModemCrc((byte*)crcMessage.c_str(), 0, crcMessage.length());


      Serial.print("[address, func, len_data, data, crc] : ");
      Serial.print(address);
      Serial.print(", ");
      Serial.print(func);
      Serial.print(", ");
      Serial.print(dataLength);
      Serial.print(", ");
      Serial.print(data);
      Serial.print(", ");
      /*
      for (int i = 0; i < dataLength; i++) {
        Serial.print((byte)data[i], HEX);
        Serial.print(" ");
      }
      */
      Serial.print(crcSent, DEC);


      /*
      Serial.print("CRC calculated: ");
      Serial.print(crcCalculated, DEC);
      Serial.print(" (int)");
      Serial.print(" = ");
      */
      //Serial.print(crcCalculated, HEX);
      //Serial.println(" (hex)");

      // Comparar CRC calculado com o CRC enviado
      Serial.print(" - ");
      if (crcCalculated == crcSent) {
        Serial.println("CRC OK");
      } else {
        Serial.println("CRC NOK");
      }
    }
  }
}


/* FUNCOES AUXILIARES*/

void checkSerial(void){
  if (Serial.available()) {
    frame_received = Serial.readStringUntil('\n');          // Obtem o quadro de dados recebido

    if (frame.length() > 0) {
      // Separar o frame nas suas partes
      address_received = frame.substring(0, 1);             // Endereço
      function_received = frame.substring(1, 2);            // Funcao
      String lengthOfData = frame.substring(2, 3);          // Comprimento dos dados
      data_length = lengthOfData.toInt();                   // Converte comprimento para inteiro
      data_received = frame.substring(3, 3 + dataLength);   // Pega os dados
      String crcReceived = frame.substring(3 + dataLength); // CRC recebido como string
      crc_received = crcReceived.toInt();                   // Converte o CRC recebido para inteiro

      // Verifica o endereco para recepcao da mensagem
      address_received == ADDRESS ? enable_program = true : enable_program = false;
      
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
    pinMode(pins[i], OUTPUT);
  }
} 
