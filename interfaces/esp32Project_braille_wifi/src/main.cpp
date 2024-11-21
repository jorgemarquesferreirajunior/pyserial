#include "Btn.h"
#include "Control.h" // Biblioteca para controle dos acionamentos dos pontos
#include "DFRobotDFPlayerMini.h"
#include <Arduino.h>
#include <ESPmDNS.h>
#include <SPIFFS.h>
#include <WebServer.h>
#include <WiFi.h>
#include <ctype.h>

#define PIN_MP3_TX 26    // Connects to module's RX
#define PIN_MP3_RX 27    // Connects to module's TX
#define PIN_START_BOX 25 // Pino para execucao da mensagem
#define PIN_AUDIO_ON 33  // Pino para execucao da mensagem + audio
#define LED_BOARD 2
#define POINT_1 15 // Pino para acionamento do ponto 1 (LED 1)
#define POINT_2 4  // Pino para acionamento do ponto 2 (LED 2)
#define POINT_3 16 // Pino para acionamento do ponto 3 (LED 3)
#define POINT_4 17 // Pino para acionamento do ponto 4 (LED 4)
#define POINT_5 5  // Pino para acionamento do ponto 5 (LED 5)
#define POINT_6 18 // Pino para acionamento do ponto 6 (LED 6)
unsigned short pins[6] = {POINT_1, POINT_2, POINT_3, POINT_4,
                          POINT_5, POINT_6}; // Lista para controle dos pontos
const char *ssid = "ESP32_AP";
const char *password = "12345678";
const char *mymDNS = "afadev-iot";

// Create the Player object
DFRobotDFPlayerMini player;

IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

Btn btn_play_box(PIN_START_BOX, false);
Btn btn_play_audio(PIN_AUDIO_ON, false);

// Variáveis
int intervalo = 1000; // Valor inicial do intervalo (em milissegundos)
String savedMessage = "banana";
long connect_dfplayer;
long result_dfplayer;

// Funções de manipulação de rotas
void handleRoot(void);
void handleJS(void);
void handleCSS(void);
void handleGetMessage(void);
void handleSetMessage(void);
void handleGetIntervalo(void);
void handleSetIntervalo(void);
void beginSPIFFS(void);
void beginWiFi(void);
void beginmDNS(void);
void beginRoutes(void);
void beginWebServer(void);
void beginDFPlayer(void);
void setPinout(void);
void resetOutput(void);
void showChars(void);

void setup() {
  Serial.begin(115200);
  setPinout(); // Configura os pinos como saídas
  beginWebServer();
  resetOutput(); // Reseta o estado dos pinos
  showChars();   // Inicializa os pinos em estado baixo (nenhum ponto ativado)
  beginDFPlayer();
}

void loop() {
  server.handleClient();
  if (btn_play_box.press()) {
    for (int c = 0; c < savedMessage.length(); c++) {
      define_caractere(savedMessage[c]);
      showChars();
      if (btn_play_audio.get_state())
        player.play(savedMessage[c] - 96);
      digitalWrite(LED_BOARD, HIGH); // Ativa o LED de status durante a execução
      delay(intervalo);              // Pausa entre cada caractere
      player.pause();
      resetOutput(); // Reseta os pontos
      showChars();   // Atualiza para não mostrar nenhum ponto ativo
      digitalWrite(LED_BOARD, LOW); // Desativa o LED de status
      delay(intervalo); // Pausa antes de passar para o próximo caractere
    }
    delay(intervalo); // Pausa antes de passar para o próximo caractere
    player.play(27);
    delay(500);
    player.pause();
    resetOutput(); // Reseta os pontos
    showChars();   // Atualiza para não mostrar nenhum ponto ativo
    digitalWrite(LED_BOARD, LOW); // Desativa o LED de status
  }
}

/*
 * SubFunções
 */

// Função para servir a página HTML principal
void handleRoot() {
  File file = SPIFFS.open("/index.html", "r");
  if (!file) {
    server.send(500, "text/plain", "Erro ao abrir o arquivo HTML.");
    return;
  }

  String html = file.readString();
  file.close();

  server.send(200, "text/html", html);
}

// Função para servir o arquivo CSS
void handleCSS() {
  File file = SPIFFS.open("/style.css", "r");
  if (!file) {
    server.send(500, "text/plain", "Erro ao abrir o arquivo CSS.");
    return;
  }
  String css = file.readString();
  file.close();
  server.send(200, "text/css", css);
}

// Função para servir o arquivo JavaScript
void handleJS() {
  File file = SPIFFS.open("/script.js", "r");
  if (!file) {
    server.send(500, "text/plain", "Erro ao abrir o arquivo JavaScript.");
    return;
  }
  String js = file.readString();
  file.close();
  server.send(200, "application/javascript", js);
}

// Função para definir o valor de savedMessage
void handleSetMessage() {
  if (server.hasArg("message")) {
    savedMessage = server.arg("message");
    for (int i = 0; i < savedMessage.length(); i++) {
      savedMessage[i] = tolower(savedMessage[i]);
    }
    Serial.print("Nova mensagem: ");
    Serial.println(savedMessage);
    Serial.print("Len: ");
    Serial.println(savedMessage.length());
    server.send(200, "text/plain", "Mensagem atualizada");
  } else {
    server.send(400, "text/plain", "Parâmetro 'message' não encontrado");
  }
}

// Função para retornar o valor da variável savedMessage
void handleGetMessage() {
  server.send(200, "text/plain",
              String(savedMessage)); // Retorna o valor de savedMessage
  Serial.print("Mensagem enviada para web: ");
  Serial.println(savedMessage);
  Serial.print("Len: ");
  Serial.println(savedMessage.length());
}

// Função para retornar o valor da variável intervalo
void handleGetIntervalo() {
  server.send(200, "text/plain",
              String(intervalo)); // Retorna o valor de intervalo
}
// Função para configurar o SPIFFS
void beginSPIFFS(void) {
  if (!SPIFFS.begin(true)) {
    Serial.println("Erro ao montar o SPIFFS");
    return;
  }
}

// Função para configurar o Wi-Fi
void beginWiFi(void) {
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.println("Ponto de acesso criado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.softAPIP());
}

// Função para configurar o mDNS
void beginmDNS(void) {
  if (!MDNS.begin(mymDNS)) {
    Serial.println("Erro ao configurar mDNS");
  } else {
    Serial.println("mDNS configurado: esp32-webserver.local");
  }
}

// Função para configurar as rotas do servidor
void beginRoutes(void) {
  server.on("/", handleRoot);         // Página principal
  server.on("/style.css", handleCSS); // Arquivo CSS
  server.on("/script.js", handleJS);  // Arquivo JavaScript
  server.on("/getMessage",
            handleGetMessage); // Rota para retornar a variável intervalo
  server.on("/getIntervalo",
            handleGetIntervalo); // Rota para retornar o intervalo
  server.on("/setIntervalo", HTTP_POST,
            handleSetIntervalo); // Rota para atualizar o valor de intervalo
  server.on("/setMessage", HTTP_POST,
            handleSetMessage); // Rota para atualizar a mensagem
}

// Função para iniciar o servidor web
void beginWebServer(void) {
  beginSPIFFS();
  beginWiFi();
  beginRoutes();
  server.begin();
  Serial.println("Servidor iniciado!");
  beginmDNS();
}

// Função para configurar o valor de intervalo
void handleSetIntervalo() {
  if (server.hasArg("intervalo")) {
    intervalo = server.arg("intervalo").toInt();
    Serial.print("Novo intervalo: ");
    Serial.println(intervalo);
    server.send(200, "text/plain", "Intervalo atualizado");
  } else {
    server.send(400, "text/plain", "Parâmetro 'intervalo' não encontrado");
  }
}

void beginDFPlayer(void) {
  // Init Serial1 for DFPlayer Mini
  Serial1.begin(9600, SERIAL_8N1, PIN_MP3_RX, PIN_MP3_TX);
  digitalWrite(LED_BOARD, HIGH);

  // Start communication with DFPlayer Mini
  if (!player.begin(Serial1)) {
    Serial.println("Connecting to DFPlayer Mini failed!");
    connect_dfplayer = millis();
    result_dfplayer = millis();
    while (result_dfplayer - connect_dfplayer <= 5000) {
      result_dfplayer = millis();
    }
    for (int j = 0; j < 6; j++) {
      digitalWrite(LED_BOARD, !digitalRead(LED_BOARD));
      delay(1000);
    }
    if (!player.begin(Serial1))
      Serial.println("Connecting to DFPlayer Mini failed after 5 seconds!");
  } else {
    digitalWrite(LED_BOARD, LOW);
    Serial.println("Connection OK");

    // Set volume to maximum (0 to 30).
    player.volume(30);
    // Play the first MP3 file on the SD card
    // player.play(1);
  }
}

void setPinout(void) {
  for (size_t i = 0; i < 6; i++) { // Para cada pino de controle
    pinMode(pins[i], OUTPUT);      // Configura como saída
  }
  pinMode(LED_BOARD, OUTPUT); // Configura o pino do LED indicador como saída
  pinMode(PIN_AUDIO_ON, INPUT_PULLUP);
  pinMode(PIN_START_BOX,
          INPUT_PULLUP); // Configura o pino de execucao da mensagem como
                         // entrada de nivel logico alto
}

void showChars(void) {
  // Exibe o caractere traduzido nos pontos de Braille
  digitalWrite(POINT_1, output[0]);
  digitalWrite(POINT_2, output[1]);
  digitalWrite(POINT_3, output[2]);
  digitalWrite(POINT_4, output[3]);
  digitalWrite(POINT_5, output[4]);
  digitalWrite(POINT_6, output[5]);
}
