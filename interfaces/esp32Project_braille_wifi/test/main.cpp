#include <Arduino.h>
#include <ESPmDNS.h>
#include <SPIFFS.h>
#include <WebServer.h>
#include <WiFi.h>

const char *ssid = "ESP32_AP";
const char *password = "12345678";
const char *mymDNS = "afadev-iot";

IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

// Variável para armazenar a mensagem
String savedMessage = "banana";

// Funções de manipulação de rotas
void handleRoot(void);
void handleJS(void);
void handleCSS(void);
void handleGetMessage(void);
void beginSPIFFS(void);
void beginWiFi(void);
void beginmDNS(void);
void beginRoutes(void);
void beginWebServer(void);

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT); // Define a GPIO 2 como saída para o LED
  beginWebServer();
}

void loop() { server.handleClient(); }

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

// Função para retornar o valor da variável savedMessage
void handleGetMessage() {
  server.send(200, "text/plain",
              savedMessage); // Retorna o valor de savedMessage
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
  server.on("/", handleRoot);                 // Página principal
  server.on("/style.css", handleCSS);         // Arquivo CSS
  server.on("/script.js", handleJS);          // Arquivo JavaScript
  server.on("/getMessage", handleGetMessage); // Rota para retornar a mensagem
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
